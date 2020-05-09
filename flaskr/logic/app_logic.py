import os
import asyncio
import aiohttp
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError

from .parser import Parser, FileEndReached
from .worker_funcs import executor


def main():
    import sys
    import json

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."

    # This paths are with respect to app.py
    path_read_config = '../configs/read_config.json'
    path_parse_config = '../configs/parse_config.json'
    path_data = '../data/technical_challenge_data.csv'

    with open(path_read_config, 'r') as config:
        data = json.load(config).get("items")
    file_formatting = data.get("file_formatting")
    custom_formatting = data.get("custom_formatting")


    with open(path_parse_config, 'r') as config:
        chunk_size = json.load(config).get("chunk_size")

    parser = Parser(path_data, file_formatting, custom_formatting, chunk_size)

    while True:
        try:
            asyncio.run(executor(parser=parser))
        except FileEndReached:
            print("Done parsing.")
            break

    return "All is good."
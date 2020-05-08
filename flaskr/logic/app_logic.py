import asyncio
import aiohttp
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError

from parser import Parser, FileEndReached
from worker_funcs import executor


def main():
    import pathlib
    import sys
    import json

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent

    with open("read_config.json", 'r') as config:
        data = json.load(config).get("items")
    file_formatting = data.get("file_formatting")
    custom_formatting = data.get("custom_formatting")

    with open("parse_config.json", 'r') as config:
        chunk_size = json.load(config).get("chunk_size")

    parser = Parser("mock_data.csv", file_formatting, custom_formatting, chunk_size)

    while True:
        try:
            asyncio.run(executor("database_placeholder", urls="placeholder_string", parser=parser))
        except FileEndReached:
            print("Done parsing.")
            break

if __name__ == "__main__":
    main()

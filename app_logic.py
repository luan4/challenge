import asyncio
import aiohttp
from aiohttp import ClientSession

from parser import Parser
import json
from itertools import islice


async def fetch_fields(url: str, session: ClientSession, **kwargs) -> str:
    """GET request wrapper to fetch page JSON.

    kwargs are passed to `session.request()`.
    """

    resp = await session.request(method="GET", url=url, **kwargs)
    resp.raise_for_status()
    #logger.info("Got response [%s] for URL: %s", resp.status, url)
    json = await resp.json()
    return json

async def write_one(file_path: str, url: str, **kwargs) -> None:
    """Write the requested fields to database: 
    
    site_id, id, price, start_time, name(categories), description(currency), nickname(users)
    """
    try:
        res = await fetch_fields(url=url, **kwargs)
    except:
        errors.append(f"Error getting item: {url}")
        return

    category_id = res.get("category_id")
    url_category = urlmaker_category(category_id)
    category_name = await getfield_category(url_category, **kwargs)
    #print(category_name)

    currency_id = res.get("currency_id")
    url_currency = urlmaker_currency(currency_id)
    currency_description = await getfield_currency(url_currency, **kwargs)
    #print(currency_description)

    seller_id = res.get("seller_id")
    url_user = urlmaker_user(seller_id)
    nickname = await getfield_user(url_user, **kwargs)
    print(nickname)
    #if not res:
    #    return None
    #async with aiofiles.open(file, "a") as f:
    #    for p in res:
    #        await f.write(f"{url}\t{p}\n")
    #    #logger.info("Wrote results for source URL: %s", url)


async def bulk_crawl_and_write(file_path: str, urls: set, **kwargs) -> None:
    """Crawl & write to database for multiple API requests."""
    async with ClientSession() as session:
        tasks = []
        chunk = parser.read_chunk()
        urls = urlmaker_items(chunk)
        for url in urls:
            tasks.append(
                write_one(file_path=file_path, url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)


async def getfield_category(url_category: str, **kwargs) -> str:
    try:
       res = await fetch_fields(url=url_category, **kwargs)
    except:
        errors.append(f"Error getting category_id in url: {url_category}")
        return
    return res.get("name")

async def getfield_currency(url_currency: str, **kwargs) -> str:
    try:
       res = await fetch_fields(url=url_currency, **kwargs)
    except:
        errors.append(f"Error getting currency_id in url: {url_currency}")
        return
    return res.get("description")

async def getfield_user(url_user: str, **kwargs) -> str:
    try:
       res = await fetch_fields(url=url_user, **kwargs)
    except:
        errors.append(f"Error getting nickname in url: {url_user}")
        return
    return res.get("nickname")

def urlmaker_items(items: list) -> str:
    """ Takes a list of items (from parser.read_chunk) and returns a list of urls for item API request """
    urls = []
    for item in items:
        id = item[1].rstrip("\n")
        url = f"https://api.mercadolibre.com/items/{item[0]}{id}?attributes="
        url += "{,price,start_time,currency_id,category_id,seller_id,}"
        urls.append(url)
    return urls

def urlmaker_category(category_id: str) -> str:
    url = f"https://api.mercadolibre.com/categories/{category_id}?attributes="
    url += "{,name,}"
    return url

def urlmaker_currency(currency_id: str) -> str:
    url = f"https://api.mercadolibre.com/currencies/{currency_id}?attributes="
    url += "{,description,}"
    return url

def urlmaker_user(seller_id: str) -> str:
    url = f"https://api.mercadolibre.com/users/{seller_id}?attributes="
    url += "{,nickname,}"
    return url

if __name__ == "__main__":
    import pathlib
    import sys

    assert sys.version_info >= (3, 7), "Script requires Python 3.7+."
    here = pathlib.Path(__file__).parent

    #with open(here.joinpath("urls.txt")) as infile:
    #    urls = set(map(str.strip, infile))

    outpath = here.joinpath("foundurls.txt")
    #with open(outpath, "w") as outfile:
    #    outfile.write("source_url\tparsed_url\n")

    with open("read_config.json", 'r') as config:
        data = json.load(config).get("items")

    with open("parse_config.json", 'r') as config:
        chunk_size = json.load(config).get("chunk_size")

    file_formatting = data.get("file_formatting")
    custom_formatting = data.get("custom_formatting")

    chunk_size = 2

    parser = Parser("technical_challenge_data.csv", file_formatting, custom_formatting, chunk_size)

    errors = []

    for _ in range(3):
        asyncio.run(bulk_crawl_and_write(outpath, urls="placeholder_string"))
    print(errors)

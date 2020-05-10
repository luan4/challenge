import asyncio
from aiohttp import ClientSession
from aiohttp.client_exceptions import ClientResponseError

import flask_sqlalchemy

from .urlmakers import urlmaker_items, urlmaker_category, urlmaker_currency, urlmaker_user
from .parser import Parser, FileEndReached
from .models import Items_MELI, db

async def fetch_fields(url: str, session: ClientSession, req_field=None, **kwargs) -> str:
    """GET request wrapper to fetch page JSON.

    kwargs are passed to `session.request()`.
    """
    resp = await session.request(method="GET", url=url, **kwargs)
    try: 
        resp.raise_for_status()
    except ClientResponseError as error:
        print(error)
    else:
        # is this await necessary??
        json = await resp.json()
        if json and req_field:
            return json.get(req_field)
        return json

async def writer(url: str, **kwargs) -> None:
    """Write the requested fields to database: 
    
    site_id, id, price, start_time, name(categories), description(currency), nickname(users)
    """
    item = await fetch_fields(url=url, **kwargs)
    if not item:
        return

    category_id = item.get("category_id")
    url_category = urlmaker_category(category_id)
    category_name = await fetch_fields(url_category, req_field="name", **kwargs)

    currency_id = item.get("currency_id")
    url_currency = urlmaker_currency(currency_id)
    currency_description = await fetch_fields(url_currency, req_field="description", **kwargs)

    seller_id = item.get("seller_id")
    url_user = urlmaker_user(seller_id)
    user_nickname = await fetch_fields(url_user, req_field="nickname", **kwargs)

    uploadable = Items_MELI(id=item["id"], price=price, start_time=item["start_time"],
            name=category_name, description=currency_description, nickname=user_nickname
            )

    db.session.add(uploadable)
    db.session.commit()


async def executor(parser: Parser, **kwargs) -> None:
    """Crawl & write to database for multiple API requests."""
    async with ClientSession() as session:
        tasks = []
        chunk = parser.read_chunk()
        urls = urlmaker_items(chunk)
        for url in urls:
            #print(url)
            tasks.append(
                writer(url=url, session=session, **kwargs)
            )
        await asyncio.gather(*tasks)

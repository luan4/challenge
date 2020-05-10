def urlmaker_items(items: list) -> str:
    """ Takes a list of items (from parser.read_chunk) and returns a list of urls for item API request """
    urls = []
    for item in items:
        url = f"https://api.mercadolibre.com/items/{item[0]}{item[1]}?attributes="
        url += "{,id,price,start_time,currency_id,category_id,seller_id,}"
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


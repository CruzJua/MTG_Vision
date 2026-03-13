# import asyncio
import httpx
import json

from typing import Literal
# from rich import print

"""
API endpoints I'm likley to use:
GET /cards/named
    use fuzzy query param for flexible name search
    returns all details of the card

GET /cards/autocomplete
    use q query param with at least 2 chars
    returns list of top 20 most likly names starting with q

GET /cards/search
    use q query param
    This uses the scryfall advanced Regex search
    return a list of all cards they pattern explains

GET /cards/:id
    Use the scryfall UUID
    returns a single card which has that UUID
"""

headers = {
        "User-Agent": "MTGVIsionShowcase/1.0 (tonocruz9000@gmail.com)",
        "Accept": "application/json"
    }
url_base = "https://api.scryfall.com/"




async def get_card_data(card_name: str):
    url = f"{url_base}cards/named?fuzzy={card_name}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()


async def get_image_by_name(
card_name: str, 
image_type: Literal["small", "normal", "large", "png", "art_crop", "border_crop"] = "normal"):
    url = f"{url_base}cards/named?fuzzy={card_name}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        image_url = json.load(response)['image_uris'][image_type]
        return image_url


async def autocomplete(text: str):
    url = f"{url_base}cards/autocomplete?q={text}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()

async def get_card_by_id(id: str):
    url = f"{url_base}cards/{id}"
    
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response.json()


if __name__ == "__main__":
    pass
    # card_info = asyncio.run(get_card_by_id("56ebc372-aabd-4174-a943-c7bf59e5028d"))
    # print(card_info)
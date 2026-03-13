from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path
import scryfall_api

app = FastAPI()

# Get the path to the Frontend folder (one directory up from Backend)
BASE_DIR = Path(__file__).resolve().parent.parent
FRONTEND_DIR = BASE_DIR / "Frontend"

# Mount the Frontend folder to serve assets like app.js and style.css
app.mount("/static", StaticFiles(directory=str(FRONTEND_DIR)), name="static")

@app.get("/")
async def serve_frontend():
    """Serve the main index.html file"""
    return FileResponse(str(FRONTEND_DIR / "index.html"))

@app.get("/api/card/{card_name}")
async def fetch_card(card_name: str):
    return await scryfall_api.get_card_data(card_name)

@app.get("/api/autocomplete")
async def autocomplete(q: str):
    return await scryfall_api.autocomplete(q)

@app.get("/api/card/id/{card_id}")
async def get_card_by_id(card_id: str):
    return await scryfall_api.get_card_by_id(card_id)


if __name__ == "__main__":
    import asyncio

    async def test():
        print("Testing Scryfall API...")
        card = await fetch_card("Sol Ring")
        if card:
            print(f"Success! Found: {card['name']} - Price: {card['prices']['usd']}")
        else:
            print("Failed to find card.")

    asyncio.run(test())
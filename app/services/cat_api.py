import httpx

THE_CAT_API_URL = "https://api.thecatapi.com/v1/breeds"


async def is_valid_breed(breed_name: str) -> bool:
    async with httpx.AsyncClient(timeout=5) as client:
        response = await client.get(THE_CAT_API_URL)
        response.raise_for_status()

        breeds = response.json()
        return any(breed["name"].lower() == breed_name.lower() for breed in breeds)

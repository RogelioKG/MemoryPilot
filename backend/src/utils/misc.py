import logging
from typing import Any

import requests


def geocode(location: str) -> dict[str, Any] | None:
    """Geocode location name to lat/lon via Open-Meteo."""
    try:
        response = requests.get(
            "https://geocoding-api.open-meteo.com/v1/search",
            params={"name": location, "count": 1},
            timeout=5,
        )
        logging.info(f"Geocode request: {response.url}")
        data: dict = response.json()
        if not data.get("results"):
            return None
        return data["results"][0]
    except Exception:
        return None

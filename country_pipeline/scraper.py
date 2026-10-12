from __future__ import annotations

from typing import Final

import requests
from bs4 import BeautifulSoup

from .models import Country

SOURCE_URL: Final[str] = "https://www.scrapethissite.com/pages/simple/"


def _clean_text(value: str) -> str:
    return " ".join(value.split())


def scrape_countries(limit: int = 20) -> list[Country]:
    response = requests.get(SOURCE_URL, timeout=30)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")
    country_cards = soup.select("div.country")
    countries: list[Country] = []

    for card in country_cards[:limit]:
        name = _clean_text(card.select_one("h3.country-name").get_text())
        capital = _clean_text(card.select_one("span.country-capital").get_text())
        population = int(_clean_text(card.select_one("span.country-population").get_text()))
        area = float(_clean_text(card.select_one("span.country-area").get_text()))
        countries.append(
            Country(
                name=name,
                capital=capital,
                population=population,
                area=area,
            )
        )

    return countries

from __future__ import annotations

from country_pipeline.database import CountryDatabaseManager
from country_pipeline.scraper import scrape_countries


def main() -> None:
    countries = scrape_countries(limit=20)
    manager = CountryDatabaseManager()
    manager.upsert_countries(countries)
    print(f"Seeded {len(countries)} countries into {manager.db_path}")


if __name__ == "__main__":
    main()

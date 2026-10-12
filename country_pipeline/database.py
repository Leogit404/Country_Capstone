from __future__ import annotations

import sqlite3
from pathlib import Path

from .models import Country


class CountryDatabaseManager:
    def __init__(self, db_path: str | Path = "countries.db") -> None:
        self.db_path = Path(db_path)
        self._initialize_database()

    def _connect(self) -> sqlite3.Connection:
        connection = sqlite3.connect(self.db_path)
        connection.row_factory = sqlite3.Row
        return connection

    def _initialize_database(self) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                CREATE TABLE IF NOT EXISTS countries (
                    name TEXT PRIMARY KEY,
                    capital TEXT NOT NULL,
                    population INTEGER NOT NULL,
                    area REAL NOT NULL
                )
                """
            )

    def create_country(self, country: Country) -> None:
        with self._connect() as connection:
            connection.execute(
                """
                INSERT INTO countries (name, capital, population, area)
                VALUES (?, ?, ?, ?)
                """,
                (country.name, country.capital, country.population, country.area),
            )

    def upsert_countries(self, countries: list[Country]) -> None:
        with self._connect() as connection:
            connection.executemany(
                """
                INSERT INTO countries (name, capital, population, area)
                VALUES (?, ?, ?, ?)
                ON CONFLICT(name) DO UPDATE SET
                    capital = excluded.capital,
                    population = excluded.population,
                    area = excluded.area
                """,
                [(country.name, country.capital, country.population, country.area) for country in countries],
            )

    def get_all_countries(self) -> list[Country]:
        with self._connect() as connection:
            rows = connection.execute(
                "SELECT name, capital, population, area FROM countries ORDER BY name"
            ).fetchall()
        return [Country(**dict(row)) for row in rows]

    def get_country_by_name(self, country_name: str) -> Country | None:
        with self._connect() as connection:
            row = connection.execute(
                "SELECT name, capital, population, area FROM countries WHERE name = ?",
                (country_name,),
            ).fetchone()
        return Country(**dict(row)) if row else None

    def update_country(self, country_name: str, country: Country) -> bool:
        with self._connect() as connection:
            cursor = connection.execute(
                """
                UPDATE countries
                SET name = ?, capital = ?, population = ?, area = ?
                WHERE name = ?
                """,
                (country.name, country.capital, country.population, country.area, country_name),
            )
        return cursor.rowcount > 0

    def delete_country(self, country_name: str) -> bool:
        with self._connect() as connection:
            cursor = connection.execute("DELETE FROM countries WHERE name = ?", (country_name,))
        return cursor.rowcount > 0

from __future__ import annotations

from dataclasses import dataclass


@dataclass(slots=True)
class Country:
    name: str
    capital: str
    population: int
    area: float

    def to_dict(self) -> dict[str, str | int | float]:
        return {
            "name": self.name,
            "capital": self.capital,
            "population": self.population,
            "area": self.area,
        }

from __future__ import annotations

from dataclasses import asdict

from fastapi import FastAPI, HTTPException, Response, status
from pydantic import BaseModel, Field

from .database import CountryDatabaseManager
from .models import Country

app = FastAPI(title="Country Data Pipeline API")
db_manager = CountryDatabaseManager()


class CountryPayload(BaseModel):
    name: str = Field(min_length=1)
    capital: str = Field(min_length=1)
    population: int = Field(ge=0)
    area: float = Field(ge=0)


@app.get("/countries")
def get_countries() -> list[dict[str, str | int | float]]:
    return [country.to_dict() for country in db_manager.get_all_countries()]


@app.get("/countries/{country_name}")
def get_country(country_name: str) -> dict[str, str | int | float]:
    country = db_manager.get_country_by_name(country_name)
    if country is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return country.to_dict()


@app.post("/countries", status_code=status.HTTP_201_CREATED)
def create_country(payload: CountryPayload) -> dict[str, str | int | float]:
    country = Country(**payload.model_dump())
    try:
        db_manager.create_country(country)
    except Exception as exc:
        if "UNIQUE constraint failed" in str(exc):
            raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="Country already exists") from exc
        raise
    return country.to_dict()


@app.put("/countries/{country_name}")
def update_country(country_name: str, payload: CountryPayload) -> dict[str, str | int | float]:
    country = Country(**payload.model_dump())
    updated = db_manager.update_country(country_name, country)
    if not updated:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return country.to_dict()


@app.delete("/countries/{country_name}", status_code=status.HTTP_204_NO_CONTENT)
def delete_country(country_name: str) -> Response:
    deleted = db_manager.delete_country(country_name)
    if not deleted:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Country not found")
    return Response(status_code=status.HTTP_204_NO_CONTENT)

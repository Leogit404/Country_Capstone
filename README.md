# Capstone Project

## Setup

1. Activate the virtual environment.
2. Install dependencies with `pip install -r requirements.txt`.
3. Seed the database with `python seed_database.py`.
4. Run the API with `uvicorn country_pipeline.api:app --reload`.
5. Run the client with `python client.py`.

## Deliverables

- `countries.db`: SQLite database with country name as the primary key.
- `client.py`: Requests data from the API, prints a DataFrame, exports CSV, and saves a scatter plot.
- `population_vs_area.png`: Scatter plot saved by the client.
- `exported_countries.csv`: CSV export saved by the client.
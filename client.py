
from __future__ import annotations

import pandas as pd
import requests
from matplotlib import pyplot as plt

API_URL = "http://127.0.0.1:8000/countries"
CSV_OUTPUT = "exported_countries.csv"
PLOT_OUTPUT = "population_vs_area.png"


def main() -> None:
    response = requests.get(API_URL, timeout=30)
    response.raise_for_status()

    dataframe = pd.DataFrame(response.json())
    print(dataframe)

    dataframe.to_csv(CSV_OUTPUT, index=False)

    plt.figure(figsize=(10, 6))
    plt.scatter(dataframe["population"], dataframe["area"], color="teal", alpha=0.75)
    plt.title("Population vs Area for First 20 Countries")
    plt.xlabel("Population")
    plt.ylabel("Area (sq. km)")
    plt.grid(True, linestyle="--", linewidth=0.5, alpha=0.7)
    plt.tight_layout()
    plt.savefig(PLOT_OUTPUT)
    plt.close()

    print(f"CSV exported to {CSV_OUTPUT}")
    print(f"Scatter plot saved to {PLOT_OUTPUT}")


if __name__ == "__main__":
    main()

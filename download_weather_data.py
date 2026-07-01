import os
import requests
import pandas as pd


CITIES = {
    "Yangon": {
        "country": "Myanmar",
        "latitude": 16.8409,
        "longitude": 96.1735,
    },
    "Mandalay": {
        "country": "Myanmar",
        "latitude": 21.9588,
        "longitude": 96.0891,
    },
    "Naypyidaw": {
        "country": "Myanmar",
        "latitude": 19.7633,
        "longitude": 96.0785,
    },
    "Singapore": {
        "country": "Singapore",
        "latitude": 1.3521,
        "longitude": 103.8198,
    },
}


PARAMETERS = [
    "T2M",
    "T2M_MAX",
    "T2M_MIN",
    "PRECTOTCORR",
    "RH2M",
    "WS10M",
    "ALLSKY_SFC_SW_DWN",
]


def download_city_weather(city_name, city_info, start_date="20200101", end_date="20251231"):
    """Download daily weather data from NASA POWER API for one city."""

    url = "https://power.larc.nasa.gov/api/temporal/daily/point"

    params = {
        "parameters": ",".join(PARAMETERS),
        "community": "AG",
        "longitude": city_info["longitude"],
        "latitude": city_info["latitude"],
        "start": start_date,
        "end": end_date,
        "format": "JSON",
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    data = response.json()
    parameter_data = data["properties"]["parameter"]

    df = pd.DataFrame(parameter_data)
    df.index.name = "date"
    df = df.reset_index()

    df["date"] = pd.to_datetime(df["date"], format="%Y%m%d")
    df["city"] = city_name
    df["country"] = city_info["country"]
    df["latitude"] = city_info["latitude"]
    df["longitude"] = city_info["longitude"]

    df = df.rename(
        columns={
            "T2M": "temperature_avg",
            "T2M_MAX": "temperature_max",
            "T2M_MIN": "temperature_min",
            "PRECTOTCORR": "rainfall",
            "RH2M": "humidity",
            "WS10M": "wind_speed",
            "ALLSKY_SFC_SW_DWN": "solar_radiation",
        }
    )

    return df


def main():
    os.makedirs("data/raw", exist_ok=True)

    all_city_data = []

    for city_name, city_info in CITIES.items():
        print(f"Downloading data for {city_name}...")

        city_df = download_city_weather(city_name, city_info)

        file_name = city_name.lower().replace(" ", "_")
        city_df.to_csv(f"data/raw/{file_name}_weather_raw.csv", index=False)

        all_city_data.append(city_df)

    combined_df = pd.concat(all_city_data, ignore_index=True)
    combined_df.to_csv("data/raw/climate_weather_raw_combined.csv", index=False)

    print("Download completed!")
    print(combined_df.head())
    print(f"Total rows: {len(combined_df)}")


if __name__ == "__main__":
    main()
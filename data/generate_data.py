"""
Generate synthetic wildlife health surveillance data for Kenya.
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random

# Set seed for reproducibility
np.random.seed(42)
random.seed(42)

# Kenya wildlife regions and coordinates
REGIONS = {
    "Maasai Mara": (-1.4833, 35.1333),
    "Amboseli": (-2.6527, 37.2606),
    "Tsavo East": (-2.6857, 38.7578),
    "Tsavo West": (-3.0167, 38.0667),
    "Samburu": (0.5833, 37.5333),
    "Lake Nakuru": (-0.3667, 36.0833),
    "Nairobi NP": (-1.3733, 36.8581),
    "Meru": (0.0500, 38.1833),
}

# Wildlife species
SPECIES = [
    "African Elephant",
    "Lion",
    "Zebra",
    "Giraffe",
    "Buffalo",
    "Wildebeest",
    "Hippopotamus",
    "Rhino",
    "Cheetah",
    "Hyena",
]

# Syndromic categories
SYNDROMES = [
    "Respiratory",
    "Gastrointestinal",
    "Neurological",
    "Dermatological",
    "Musculoskeletal",
    "Sudden Death",
    "Reproductive",
    "Ocular",
]

# Severity levels
SEVERITY = ["Low", "Moderate", "High", "Critical"]

# Status
STATUS = ["Active", "Resolved", "Under Investigation"]


def generate_surveillance_data(n_records=500):
    """Generate synthetic surveillance records."""

    # Date range: last 12 months
    end_date = datetime.now()
    start_date = end_date - timedelta(days=365)

    data = []

    for i in range(n_records):
        region = random.choice(list(REGIONS.keys()))
        lat, lon = REGIONS[region]

        # Add some randomness to coordinates
        lat += np.random.normal(0, 0.1)
        lon += np.random.normal(0, 0.1)

        # Random date within range
        days_offset = random.randint(0, 365)
        report_date = start_date + timedelta(days=days_offset)

        # Species with weighted probability (some more common)
        species = random.choices(
            SPECIES,
            weights=[15, 8, 20, 12, 18, 15, 5, 2, 3, 7],
            k=1
        )[0]

        # Syndrome with seasonal variation
        month = report_date.month
        if month in [6, 7, 8]:  # Dry season - more respiratory
            syndrome_weights = [25, 15, 10, 15, 10, 10, 5, 10]
        elif month in [3, 4, 5, 11]:  # Wet season - more GI
            syndrome_weights = [15, 25, 10, 10, 10, 15, 10, 5]
        else:
            syndrome_weights = [15, 15, 15, 15, 10, 15, 10, 5]

        syndrome = random.choices(SYNDROMES, weights=syndrome_weights, k=1)[0]

        # Severity
        severity = random.choices(
            SEVERITY,
            weights=[40, 35, 20, 5],
            k=1
        )[0]

        # Status based on date
        days_ago = (end_date - report_date).days
        if days_ago < 14:
            status = random.choices(STATUS, weights=[60, 20, 20], k=1)[0]
        elif days_ago < 60:
            status = random.choices(STATUS, weights=[30, 50, 20], k=1)[0]
        else:
            status = random.choices(STATUS, weights=[10, 80, 10], k=1)[0]

        # Number of animals affected
        if severity == "Critical":
            n_affected = random.randint(5, 20)
        elif severity == "High":
            n_affected = random.randint(3, 10)
        elif severity == "Moderate":
            n_affected = random.randint(1, 5)
        else:
            n_affected = random.randint(1, 3)

        record = {
            "case_id": f"WHW-{2024}-{i+1:04d}",
            "report_date": report_date.strftime("%Y-%m-%d"),
            "region": region,
            "latitude": round(lat, 4),
            "longitude": round(lon, 4),
            "species": species,
            "syndrome": syndrome,
            "severity": severity,
            "status": status,
            "animals_affected": n_affected,
        }

        data.append(record)

    df = pd.DataFrame(data)
    df["report_date"] = pd.to_datetime(df["report_date"])
    df = df.sort_values("report_date").reset_index(drop=True)

    return df


if __name__ == "__main__":
    df = generate_surveillance_data(500)
    df.to_csv("wildlife_health_data.csv", index=False)
    print(f"Generated {len(df)} records")
    print(df.head())



import pandas as pd
import numpy as np
from pathlib import Path

# Find project folder
project_path = Path(__file__).resolve().parent.parent

# Raw and Silver folder paths
raw_path = project_path / "data" / "raw"
silver_path = project_path / "data" / "silver"

# Create Silver folder if it does not exist
silver_path.mkdir(parents=True, exist_ok=True)

print("Project path:", project_path)
print("Raw folder:", raw_path)
print("Silver folder:", silver_path)

print("\nData cleaning setup completed!")






# Define data folder paths
raw_path = project_path / "data" / "raw"
bronze_path = project_path / "data" / "bronze"
silver_path = project_path / "data" / "silver"

# Create folders if they don't exist
bronze_path.mkdir(parents=True, exist_ok=True)
silver_path.mkdir(parents=True, exist_ok=True)

print("Folder setup completed successfully!")


#  Load Bronze datasets

rainfall = pd.read_csv(bronze_path / "01_historical_rainfall.csv")
flood = pd.read_csv(bronze_path / "02_flood_affected_areas.csv")
road = pd.read_csv(bronze_path / "03_road_damage_complaints.csv")
traffic = pd.read_json(bronze_path / "04_traffic_congestion.json")
grievance = pd.read_excel(bronze_path / "05_public_grievances.xlsx")
waterlogging = pd.read_csv(bronze_path / "06_waterlogging_locations.csv")
population = pd.read_excel(bronze_path / "07_population_density_by_zone.xlsx")
emergency = pd.read_json(bronze_path / "08_emergency_response_rescue.json")

print("All 8 Bronze datasets loaded successfully!")

datasets = {
    "Rainfall": rainfall,
    "Flood": flood,
    "Road Complaints": road,
    "Traffic": traffic,
    "Public Grievances": grievance,
    "Waterlogging": waterlogging,
    "Population": population,
    "Emergency Response": emergency
}

for name, df in datasets.items():
    print(name, ":", df.shape)


#  Check Missing Values in Bronze Datasets

print("\n========== MISSING VALUE ANALYSIS ==========")

for name, df in datasets.items():

    print("\nDataset:", name)

    missing_values = df.isnull().sum()

    print(missing_values)



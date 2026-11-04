import pandas as pd
import numpy as np
import os
from pathlib import Path

# load datasets

rainfall = pd.read_csv("data/raw/01_historical_rainfall.csv")

flood = pd.read_csv("data/raw/02_flood_affected_areas.csv")

road = pd.read_csv("data/raw/03_road_damage_complaints.csv")

traffic = pd.read_json("data/raw/04_traffic_congestion.json")

grievance = pd.read_excel("data/raw/05_public_grievances.xlsx")

waterlogging = pd.read_csv("data/raw/06_waterlogging_locations.csv")

population = pd.read_excel("data/raw/07_population_density_by_zone.xlsx")

emergency = pd.read_json("data/raw/08_emergency_response_rescue.json")


# check dataset shapes

print("Rainfall:", rainfall.shape)
print("Flood:", flood.shape)
print("Road:", road.shape)
print("Traffic:", traffic.shape)
print("Grievance:", grievance.shape)
print("Waterlogging:", waterlogging.shape)
print("Population:", population.shape)
print("Emergency:", emergency.shape)

# get project root directory

project_path = Path(__file__).resolve().parent.parent

# define raw data folder

raw_path = project_path / "data" / "raw"

print("Project Path:", project_path)
print("Raw Data Path:", raw_path)


# load csv datasets

rainfall = pd.read_csv(raw_path / "01_historical_rainfall.csv")

flood = pd.read_csv(raw_path / "02_flood_affected_areas.csv")

road = pd.read_csv(raw_path / "03_road_damage_complaints.csv")

waterlogging = pd.read_csv(raw_path / "06_waterlogging_locations.csv")


# load json datasets

traffic = pd.read_json(raw_path / "04_traffic_congestion.json")

emergency = pd.read_json(raw_path / "08_emergency_response_rescue.json")


# load excel datasets

grievance = pd.read_excel(raw_path / "05_public_grievances.xlsx")

population = pd.read_excel(raw_path / "07_population_density_by_zone.xlsx")


print("All 8 datasets loaded successfully!")


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


def explore_dataset(df, name):

    print("\n================================")
    print("DATASET:", name)
    print("================================")

    print("\n1. Dataset Shape:")
    print(df.shape)

    print("\n2. Column Names:")
    print(df.columns.tolist())

    print("\n3. First 5 Records:")
    print(df.head())

    print("\n4. Data Types:")
    print(df.dtypes)

    print("\n5. Missing Values:")
    print(df.isnull().sum())

    print("\n6. Duplicate Records:")
    print(df.duplicated().sum())
#Calling the function
for name, df in datasets.items():

    explore_dataset(df, name)

# Data Quality Summary

quality_report = []

for name, df in datasets.items():

    quality_report.append({
        "Dataset": name,
        "Total_Rows": df.shape[0],
        "Total_Columns": df.shape[1],
        "Total_Null_Values": df.isnull().sum().sum(),
        "Total_Duplicate_Rows": df.duplicated().sum()
    })

quality_df = pd.DataFrame(quality_report)

print("\n========== DATA QUALITY SUMMARY ==========")
print(quality_df)

# Save report
report_path = project_path / "reports" / "data_quality_summary.csv"

quality_df.to_csv(report_path, index=False)

print("\nData quality report saved successfully!")

print(quality_df)

print(quality_df.to_string(index=False))


#Check null values

for name, df in datasets.items():

    print("\nDataset:", name)

    print(df.isnull().sum())

#  Check duplicate records

for name, df in datasets.items():

    print("\nDataset:", name)

    duplicate_count = df.duplicated().sum()

    print("Total Duplicate Rows:", duplicate_count)

# Check abnormal rainfall values

print("\n========== RAINFALL CHECK ==========")

print("Minimum Rainfall:")
print(rainfall["rainfall_mm"].min())

print("\nMaximum Rainfall:")
print(rainfall["rainfall_mm"].max())

print("\nRainfall values greater than 300 mm:")

abnormal_rainfall = rainfall[
    rainfall["rainfall_mm"] > 300
]

print(abnormal_rainfall)
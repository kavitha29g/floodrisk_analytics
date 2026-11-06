

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


#  Rainfall Dataset Column Analysis

print("\n========== RAINFALL COLUMN ANALYSIS ==========")

print("\n1. Column Names:")
print(rainfall.columns.tolist())

print("\n2. Data Types:")
print(rainfall.dtypes)

print("\n3. Missing Values:")
print(rainfall.isnull().sum())

print("\n4. Duplicate Records:")
print(rainfall.duplicated().sum())

print("\n5. Basic Statistics:")
print(rainfall.describe())


#  Check Unique Values

print("\n========== UNIQUE VALUE ANALYSIS ==========")

print("\n1. Zone Names:")
print(rainfall["zone_name"].unique())

print("\n2. Units:")
print(rainfall["unit"].unique())

print("\n3. Sources:")
print(rainfall["source"].unique())


# Investigate Abnormal Rainfall Values

print("\n========== ABNORMAL RAINFALL ANALYSIS ==========")

abnormal_rainfall = rainfall[rainfall["rainfall_mm"] > 300]

print(abnormal_rainfall)

print("\nTotal abnormal rainfall records:")
print(len(abnormal_rainfall))


# Display abnormal rainfall values

abnormal_rainfall = rainfall[rainfall["rainfall_mm"] > 300]

print("\nAbnormal Rainfall Records:")

print(
    abnormal_rainfall[
        ["observation_date", "zone_id", "zone_name", "rainfall_mm"]
    ].to_string(index=False)
)

print("\nTotal abnormal records:", len(abnormal_rainfall))

#  - Investigate Missing Rainfall Values

missing_rainfall = rainfall[rainfall["rainfall_mm"].isnull()]

print("\n========== MISSING RAINFALL DETAILS ==========")

print(
    missing_rainfall[
        ["observation_date", "zone_id", "zone_name", "rainfall_mm"]
    ].head(20).to_string(index=False)
)

print("\nTotal missing rainfall records:", len(missing_rainfall))

print("\nMissing records by zone:")
print(missing_rainfall["zone_name"].value_counts())

# Clean Rainfall Dataset

# 1. Create a copy of the original dataset
rainfall_clean = rainfall.copy()

# 2. Convert observation_date into date format
rainfall_clean["observation_date"] = pd.to_datetime(
    rainfall_clean["observation_date"]
)

# 3. Replace 999 with missing value
rainfall_clean["rainfall_mm"] = rainfall_clean["rainfall_mm"].replace(999, np.nan)

# 4. Create a quality flag column
rainfall_clean["rainfall_quality_flag"] = "valid"

# 5. Mark missing rainfall values
rainfall_clean.loc[rainfall_clean["rainfall_mm"].isnull(), "rainfall_quality_flag"] = "missing"

print("\n========== RAINFALL CLEANING SUMMARY ==========")

print("Original records:", len(rainfall))
print("Cleaned records:", len(rainfall_clean))

print("\nMissing rainfall values:")
print(rainfall_clean["rainfall_mm"].isnull().sum())

print("\nQuality flag counts:")
print(rainfall_clean["rainfall_quality_flag"].value_counts())

print("\nDate data type:")
print(rainfall_clean["observation_date"].dtype)

#- Save Cleaned Rainfall Dataset

silver_file = silver_path / "rainfall_cleaned.csv"

rainfall_clean.to_csv(silver_file, index=False)

print("\nRainfall dataset saved successfully!")
print("Saved location:", silver_file)



#  Load Cleaned Rainfall Dataset

rainfall_silver = pd.read_csv(
    silver_path / "rainfall_cleaned.csv"
)

print("\n========== SILVER DATA VERIFICATION ==========")

print("Total rows:", rainfall_silver.shape[0])

print("Total columns:", rainfall_silver.shape[1])

print("\nFirst 5 records:")
print(rainfall_silver.head())

# Check missing values

print(rainfall_silver.isnull().sum())

# Check duplicate records

print("\nDuplicate Records:")
print(rainfall_silver.duplicated().sum())

#  Create Flood Dataset Copy

flood_clean = flood.copy()

print("\nFlood dataset copy created successfully!")

# Check Flood Columns

print("\nFlood Dataset Columns:")
print(flood_clean.columns.tolist())

#  Check Data Types

print("\nFlood Dataset Data Types:")
print(flood_clean.dtypes)

# Check Missing Values

print("\nFlood Dataset Missing Values:")
print(flood_clean.isnull().sum())

#  Check Duplicate Records

print("\nTotal Duplicate Records:")
print(flood_clean.duplicated().sum())

# Display First 5 Records

print("\nFirst 5 Flood Records:")
print(flood_clean.head())


#Check Unique Values

print("\n========== FLOOD UNIQUE VALUE ANALYSIS ==========")

print("\n1. Flood Types:")
print(flood_clean["flood_type"].unique())

print("\n2. Severity Levels:")
print(flood_clean["severity"].unique())

print("\n3. Zone Names:")
print(flood_clean["zone_name"].unique())

print("\n4. Data Sources:")
print(flood_clean["source"].unique())

#  Check Numerical Values

print("\n========== FLOOD NUMERICAL ANALYSIS ==========")

print("\n1. Latitude:")
print(flood_clean["latitude"].describe())

print("\n2. Longitude:")
print(flood_clean["longitude"].describe())

print("\n3. Estimated Affected People:")
print(flood_clean["estimated_affected_people"].describe())

print("\n4. Event Rainfall:")
print(flood_clean["event_rainfall_mm"].describe())

#Check Flood Dates and IDs

print("\n========== FLOOD DATE AND ID CHECK ==========")

# 1. Check event date
print("\nEvent Date Details:")
print("Earliest Date:", flood_clean["event_date"].min())
print("Latest Date:", flood_clean["event_date"].max())

# 2. Check event ID duplicates
print("\nDuplicate Flood Event IDs:")
print(flood_clean["flood_event_id"].duplicated().sum())

# 3. Check location ID duplicates
print("\nDuplicate Location IDs:")
print(flood_clean["location_id"].duplicated().sum())

# Convert Event Date

flood_clean["event_date"] = pd.to_datetime(
    flood_clean["event_date"]
)

print("\nEvent date converted successfully!")

print(flood_clean["event_date"].dtype)

# Save Flood Dataset

flood_file = silver_path / "flood_cleaned.csv"

flood_clean.to_csv(flood_file, index=False)

print("\nFlood dataset saved successfully!")
print("Saved location:", flood_file)


# ==========================================
# ROAD DAMAGE COMPLAINTS ANALYSIS
# ==========================================

# 1. Create a copy of the original dataset
road_clean = road.copy()

# 2. Check dataset shape
print("\n========== ROAD COMPLAINTS ANALYSIS ==========")

print("\n1. Dataset Shape:")
print(road_clean.shape)

# 3. Check column names
print("\n2. Column Names:")
print(road_clean.columns.tolist())

# 4. Check data types
print("\n3. Data Types:")
print(road_clean.dtypes)

# 5. Check missing values
print("\n4. Missing Values:")
print(road_clean.isnull().sum())

# 6. Check duplicate rows
print("\n5. Duplicate Rows:")
print(road_clean.duplicated().sum())

# 7. Display first 5 records
print("\n6. First 5 Records:")
print(road_clean.head())

# ==========================================
#DISPLAY DUPLICATE COMPLAINT IDS
# ==========================================

duplicate_ids = road_clean[
    road_clean["road_complaint_id"].duplicated(keep=False)
]

print("\nDuplicate Complaint Records:")
print(duplicate_ids.sort_values("road_complaint_id"))

# ==========================================
#VERIFY EXACT DUPLICATES
# ==========================================

print("\n========== EXACT DUPLICATE CHECK ==========")

# Check whether all duplicate records are identical
print("\nExact Duplicate Rows:")
print(road_clean.duplicated().sum())

# Check duplicate complaint IDs
print("\nDuplicate Complaint IDs:")
print(road_clean["road_complaint_id"].duplicated().sum())


#  REMOVE DUPLICATE RECORDS


# Remove duplicate rows
road_clean = road_clean.drop_duplicates()

# Check dataset shape after removing duplicates
print("\n========== AFTER DUPLICATE REMOVAL ==========")

print("\nDataset Shape:")
print(road_clean.shape)

# Check remaining duplicate rows
print("\nRemaining Duplicate Rows:")
print(road_clean.duplicated().sum())

# Check remaining duplicate complaint IDs
print("\nRemaining Duplicate Complaint IDs:")
print(road_clean["road_complaint_id"].duplicated().sum())


# UNIQUE VALUE ANALYSIS


print("\n========== ROAD COMPLAINTS UNIQUE VALUE ANALYSIS ==========")

columns = [
    "zone_name",
    "damage_type",
    "severity",
    "status",
    "reported_channel",
    "probable_cause"
]

for col in columns:
    print(f"\n{col}:")
    print(road_clean[col].unique())


#  CHECK TEXT INCONSISTENCIES


print("\n========== TEXT QUALITY CHECK ==========")

columns = [
    "zone_name",
    "damage_type",
    "severity",
    "status",
    "reported_channel",
    "probable_cause"
]

for col in columns:

    # Check leading and trailing spaces
    spaces = (road_clean[col] != road_clean[col].str.strip()).sum()

    # Check unique values without considering uppercase/lowercase
    case_values = road_clean[col].str.lower().nunique()

    print(f"\nColumn: {col}")
    print("Values with extra spaces:", spaces)
    print("Unique values ignoring case:", case_values)


# COMPLAINT DATE ANALYSIS


print("\n========== COMPLAINT DATE ANALYSIS ==========")

# 1. Display first 10 dates
print("\nFirst 10 Complaint Dates:")
print(road_clean["complaint_date"].head(10))

# 2. Display last 10 dates
print("\nLast 10 Complaint Dates:")
print(road_clean["complaint_date"].tail(10))

# 3. Check date column data type
print("\nComplaint Date Data Type:")
print(road_clean["complaint_date"].dtype)

# 4. Check unique date formats (sample)
print("\nSample Date Values:")
print(road_clean["complaint_date"].unique()[:10])


# Convert string to datetime
road_clean["complaint_date"] = pd.to_datetime(
    road_clean["complaint_date"],
    errors="coerce")


# Check data type
print(road_clean["complaint_date"].dtype)

# Check missing dates
print(road_clean["complaint_date"].isnull().sum())



#LOCATION ID ANALYSIS


print("\n========== LOCATION ID ANALYSIS ==========")

print("Total Unique Location IDs:")
print(road_clean["location_id"].nunique())

print("\nDuplicate Location IDs:")
print(road_clean["location_id"].duplicated().sum())

# Check latitude and longitude

print("Latitude:")
print(road_clean["latitude"].min(), road_clean["latitude"].max())

print("\nLongitude:")
print(road_clean["longitude"].min(), road_clean["longitude"].max())

print("\nMissing Coordinates:")
print(road_clean[["latitude", "longitude"]].isnull().sum())



# SEVERITY ANALYSIS
print("\n========== SEVERITY ANALYSIS ==========")

print(road_clean["severity"].value_counts())


# DAMAGE TYPE ANALYSIS
print("\n========== DAMAGE TYPE ANALYSIS ==========")

print(road_clean["damage_type"].value_counts())


# REPORTED CHANNEL ANALYSIS
print("\n========== REPORTED CHANNEL ANALYSIS ==========")

print(road_clean["reported_channel"].value_counts())

 
#  PROBABLE CAUSE ANALYSIS

print("\n========== PROBABLE CAUSE ANALYSIS ==========")

print(road_clean["probable_cause"].value_counts())

#  COMPLAINT STATUS ANALYSIS


print("\n========== COMPLAINT STATUS ANALYSIS ==========")

print(road_clean["status"].value_counts())


# ZONE-WISE COMPLAINT ANALYSIS

print("\n========== ZONE-WISE COMPLAINT ANALYSIS ==========")

print(road_clean["zone_name"].value_counts())


# LOCATION AND ZONE CHECK

print("\n========== LOCATION AND ZONE CHECK ==========")

print("Unique Locations:")
print(road_clean["location_id"].nunique())

print("\nUnique Location-Zone Combinations:")
print(road_clean[["location_id", "zone_id"]].drop_duplicates().shape[0])


# SEVERITY AND STATUS CHECK

print("\n========== SEVERITY AND STATUS CHECK ==========")

print(pd.crosstab(road_clean["severity"], road_clean["status"]))

# ==========================================
# FINAL DATA QUALITY CHECK
# ==========================================

print("\n========== FINAL DATA QUALITY SUMMARY ==========")

print("\nDataset Shape:")
print(road_clean.shape)

print("\nMissing Values:")
print(road_clean.isnull().sum())

print("\nDuplicate Rows:")
print(road_clean.duplicated().sum())

print("\nData Types:")
print(road_clean.dtypes)


# Save Cleaned Road Complaints Dataset

road_file = silver_path / "road_complaints_cleaned.csv"

road_clean.to_csv(road_file, index=False)

print("\nRoad Complaints dataset saved successfully!")
print("Saved location:", road_file)




# Create a copy
traffic_clean = traffic.copy()



# BASIC DATASET ANALYSIS


print("\n========== TRAFFIC DATASET ANALYSIS ==========")

print("\n1. Dataset Shape:")
print(traffic_clean.shape)

print("\n2. Column Names:")
print(traffic_clean.columns.tolist())

print("\n3. Data Types:")
print(traffic_clean.dtypes)

print("\n4. Missing Values:")
print(traffic_clean.isnull().sum())

print("\n5. Duplicate Rows:")
print(traffic_clean.duplicated().sum())

print("\n6. First 5 Records:")
print(traffic_clean.head())


# CHECK DUPLICATE RECORDS
print("\n========== DUPLICATE ANALYSIS ==========")

print("\nTotal Duplicate Rows:")
print(traffic_clean.duplicated().sum())

print("\nDuplicate Records:")
print(traffic_clean[traffic_clean.duplicated()])


#STEP 4 - CHECK DUPLICATE TRAFFIC IDs

print("\nDuplicate Traffic Record IDs:")

print(
    traffic_clean["traffic_record_id"].duplicated().sum()
)

print("\nDuplicate ID Records:")

duplicate_ids = traffic_clean[
    traffic_clean["traffic_record_id"].duplicated(keep=False)
]

print(duplicate_ids.sort_values("traffic_record_id"))

#  UNIQUE VALUE ANALYSIS

print("\n========== TRAFFIC UNIQUE VALUE ANALYSIS ==========")

columns = [
    "zone_name",
    "location_name",
    "congestion_level",
    "data_source"
]

for col in columns:
    print(f"\n{col}:")
    print(traffic_clean[col].unique())

# STEP 7 - CHECK TEXT INCONSISTENCIES


print("\n========== TEXT QUALITY CHECK ==========")

columns = [
    "zone_name",
    "location_name",
    "congestion_level",
    "data_source"
]

for col in columns:

    print(f"\nColumn: {col}")

    print(
        "Values with extra spaces:",
        (traffic_clean[col] != traffic_clean[col].str.strip()).sum()
    )

    print(
        "Unique values ignoring case:",
        traffic_clean[col].str.lower().nunique()
    )

for col in columns:
    traffic_clean[col] = traffic_clean[col].str.strip()


# STEP 9 - TIMESTAMP ANALYSIS
print("\n========== TIMESTAMP ANALYSIS ==========")

print("\nFirst 10 Records:")
print(traffic_clean["recorded_at"].head(10))

print("\nLast 10 Records:")
print(traffic_clean["recorded_at"].tail(10))

print("\nTimestamp Data Type:")
print(traffic_clean["recorded_at"].dtype)



# CONVERT TIMESTAMP


traffic_clean["recorded_at"] = pd.to_datetime(
    traffic_clean["recorded_at"],
    errors="coerce"
)

print("\nTimestamp Data Type:")
print(traffic_clean["recorded_at"].dtype)

print("\nInvalid Timestamps:")
print(traffic_clean["recorded_at"].isnull().sum())

print("\n========== LOCATION ID ANALYSIS ==========")

print("\nTotal Unique Location IDs:")
print(traffic_clean["location_id"].nunique())

print("\nDuplicate Location IDs:")
print(traffic_clean["location_id"].duplicated().sum())


#STEP 13 - LOCATION NAME ANALYSIS


print("\n========== LOCATION NAME ANALYSIS ==========")

print("\nTotal Unique Location Names:")
print(traffic_clean["location_name"].nunique())

print("\nSample Location Names:")
print(traffic_clean["location_name"].unique()[:20])

# LATITUDE AND LONGITUDE CHECK
print("\n========== COORDINATE ANALYSIS ==========")

print("\nLatitude:")
print(traffic_clean["latitude"].min(),
      traffic_clean["latitude"].max())

print("\nLongitude:")
print(traffic_clean["longitude"].min(),
      traffic_clean["longitude"].max())

print("\nMissing Coordinates:")
print(
    traffic_clean[["latitude", "longitude"]].isnull().sum()
)


#  CHECK INVALID COORDINATES


print("\n========== INVALID COORDINATE CHECK ==========")

print("\nInvalid Latitude:")
print(
    ((traffic_clean["latitude"] < -90) |
     (traffic_clean["latitude"] > 90)).sum()
)

print("\nInvalid Longitude:")
print(
    ((traffic_clean["longitude"] < -180) |
     (traffic_clean["longitude"] > 180)).sum()
)

#  AVERAGE SPEED ANALYSIS
print("\n========== AVERAGE SPEED ANALYSIS ==========")

print("\nMinimum Average Speed:")
print(traffic_clean["avg_speed_kmph"].min())

print("\nMaximum Average Speed:")
print(traffic_clean["avg_speed_kmph"].max())

print("\nNegative Average Speed Values:")
print((traffic_clean["avg_speed_kmph"] < 0).sum())

#  FINAL DATA QUALITY CHECK


print("\n========== FINAL TRAFFIC DATA QUALITY ==========")

print("\n1. Dataset Shape:")
print(traffic_clean.shape)

print("\n2. Missing Values:")
print(traffic_clean.isnull().sum())

print("\n3. Duplicate Rows:")
print(traffic_clean.duplicated().sum())

print("\n4. Duplicate Traffic IDs:")
print(traffic_clean["traffic_record_id"].duplicated().sum())

print("\n5. Data Types:")
print(traffic_clean.dtypes)

print("\n6. First 5 Records:")
print(traffic_clean.head())

# SAVE CLEANED TRAFFIC DATASET
traffic_file = silver_path / "traffic_cleaned.csv"

traffic_clean.to_csv(traffic_file, index=False)

print("\nTraffic dataset saved successfully!")
print("Saved location:", traffic_file)

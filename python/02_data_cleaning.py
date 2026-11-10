import pandas as pd
import numpy as np
from pathlib import Path

# Find project folder
project_path = Path(__file__).resolve().parent.parent

# Define data folder paths
raw_path = project_path / "data" / "raw"
bronze_path = project_path / "data" / "bronze"
silver_path = project_path / "data" / "silver"
gold_path = project_path / "data" / "gold"

# Create folders if they don't exist
bronze_path.mkdir(parents=True, exist_ok=True)
silver_path.mkdir(parents=True, exist_ok=True)
gold_path.mkdir(parents=True, exist_ok=True)

print("Project path:", project_path)
print("Raw folder:", raw_path)
print("Silver folder:", silver_path)

print("\nData cleaning setup completed!")
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
    print("\nDataset:", name)
    print("Shape:", df.shape)
    print("Columns:", df.columns.tolist())

for name, df in datasets.items():
    print(name, ":", df.shape)


#  Check Missing Values in Bronze Datasets

print("\n========== MISSING VALUE ANALYSIS ==========")

for name, df in datasets.items():

    print("\nDataset:", name)

    missing_values = df.isnull().sum()

    print(missing_values)


# STEP 2 - RAINFALL COLUMN ANALYSIS

print("\n========== RAINFALL COLUMN ANALYSIS ==========")

print("\n1. Column Names:")
print(rainfall.columns.tolist())

print("\n2. Data Types:")
print(rainfall.dtypes)

print("\n3. Duplicate Records:")
print(rainfall.duplicated().sum())

print("\n4. Basic Statistics:")
print(rainfall.describe())


# STEP 3 - CHECK UNIQUE VALUES

print("\n========== UNIQUE VALUE ANALYSIS ==========")

print("\n1. Zone Names:")
print(rainfall["zone_name"].unique())

print("\n2. Units:")
print(rainfall["unit"].unique())

print("\n3. Sources:")
print(rainfall["source"].unique())


# STEP 4 - INVESTIGATE ABNORMAL RAINFALL VALUES

print("\n========== ABNORMAL RAINFALL ANALYSIS ==========")

abnormal_rainfall = rainfall[rainfall["rainfall_mm"] > 300]

print(
    abnormal_rainfall[
        ["observation_date", "zone_id", "zone_name", "rainfall_mm"]
    ].to_string(index=False)
)

print("\nTotal abnormal rainfall records:", len(abnormal_rainfall))


# STEP 5 - INVESTIGATE MISSING RAINFALL VALUES

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


# STEP 6 - CLEAN RAINFALL DATASET

rainfall_clean = rainfall.copy()

# Convert observation date into date format
rainfall_clean["observation_date"] = pd.to_datetime(
    rainfall_clean["observation_date"]
)

# Replace 999 with missing value
rainfall_clean["rainfall_mm"] = rainfall_clean["rainfall_mm"].replace(999, np.nan)

# Create quality flag
rainfall_clean["rainfall_quality_flag"] = "valid"

# Mark missing rainfall values
rainfall_clean.loc[
    rainfall_clean["rainfall_mm"].isnull(),
    "rainfall_quality_flag"
] = "missing"


# STEP 7 - RAINFALL CLEANING SUMMARY

print("\n========== RAINFALL CLEANING SUMMARY ==========")

print("Original records:", len(rainfall))
print("Cleaned records:", len(rainfall_clean))

print("\nMissing rainfall values:")
print(rainfall_clean["rainfall_mm"].isnull().sum())

print("\nQuality flag counts:")
print(rainfall_clean["rainfall_quality_flag"].value_counts())

print("\nDate data type:")
print(rainfall_clean["observation_date"].dtype)


# STEP 8 - SAVE CLEANED RAINFALL DATASET

silver_file = silver_path / "rainfall_cleaned.csv"

rainfall_clean.to_csv(silver_file, index=False)

print("\nRainfall dataset saved successfully!")
print("Saved location:", silver_file)


# STEP 9 - VERIFY SILVER DATASET

rainfall_silver = pd.read_csv(silver_file)

print("\n========== SILVER DATA VERIFICATION ==========")

print("Total rows:", rainfall_silver.shape[0])
print("Total columns:", rainfall_silver.shape[1])

print("\nFirst 5 records:")
print(rainfall_silver.head())

print("\nMissing values:")
print(rainfall_silver.isnull().sum())

print("\nDuplicate records:")
print(rainfall_silver.duplicated().sum())

#----------------------------------------------------------------------------------------

# STEP 1 - CREATE FLOOD DATASET COPY

flood_clean = flood.copy()

print("\nFlood dataset copy created successfully!")


# STEP 2 - FLOOD COLUMN ANALYSIS

print("\n========== FLOOD COLUMN ANALYSIS ==========")

print("\n1. Column Names:")
print(flood_clean.columns.tolist())

print("\n2. Data Types:")
print(flood_clean.dtypes)

print("\n3. Missing Values:")
print(flood_clean.isnull().sum())

print("\n4. Duplicate Records:")
print(flood_clean.duplicated().sum())

print("\n5. First 5 Records:")
print(flood_clean.head())


# STEP 3 - CHECK UNIQUE VALUES

print("\n========== FLOOD UNIQUE VALUE ANALYSIS ==========")

print("\n1. Flood Types:")
print(flood_clean["flood_type"].unique())

print("\n2. Severity Levels:")
print(flood_clean["severity"].unique())

print("\n3. Zone Names:")
print(flood_clean["zone_name"].unique())

print("\n4. Data Sources:")
print(flood_clean["source"].unique())


# STEP 4 - CHECK NUMERICAL VALUES

print("\n========== FLOOD NUMERICAL ANALYSIS ==========")

print("\n1. Latitude:")
print(flood_clean["latitude"].describe())

print("\n2. Longitude:")
print(flood_clean["longitude"].describe())

print("\n3. Estimated Affected People:")
print(flood_clean["estimated_affected_people"].describe())

print("\n4. Event Rainfall:")
print(flood_clean["event_rainfall_mm"].describe())


# STEP 5 - CHECK FLOOD DATES AND IDS

print("\n========== FLOOD DATE AND ID CHECK ==========")

print("\n1. Event Date Details:")
print("Earliest Date:", flood_clean["event_date"].min())
print("Latest Date:", flood_clean["event_date"].max())

print("\n2. Duplicate Flood Event IDs:")
print(flood_clean["flood_event_id"].duplicated().sum())

print("\n3. Duplicate Location IDs:")
print(flood_clean["location_id"].duplicated().sum())


# STEP 6 - CLEAN FLOOD DATASET

# Convert event date into date format
flood_clean["event_date"] = pd.to_datetime(
    flood_clean["event_date"]
)

print("\nEvent date converted successfully!")
print("Date data type:", flood_clean["event_date"].dtype)


# STEP 7 - FLOOD CLEANING SUMMARY

print("\n========== FLOOD CLEANING SUMMARY ==========")

print("Original records:", len(flood))
print("Cleaned records:", len(flood_clean))

print("\nMissing values:")
print(flood_clean.isnull().sum())

print("\nDuplicate records:")
print(flood_clean.duplicated().sum())

print("\nDuplicate Flood Event IDs:")
print(flood_clean["flood_event_id"].duplicated().sum())


# STEP 8 - SAVE CLEANED FLOOD DATASET

flood_file = silver_path / "flood_cleaned.csv"

flood_clean.to_csv(flood_file, index=False)

print("\nFlood dataset saved successfully!")
print("Saved location:", flood_file)


# STEP 9 - VERIFY SILVER DATASET

flood_silver = pd.read_csv(flood_file)

print("\n========== SILVER DATA VERIFICATION ==========")

print("Total rows:", flood_silver.shape[0])
print("Total columns:", flood_silver.shape[1])

print("\nFirst 5 records:")
print(flood_silver.head())

print("\nMissing values:")
print(flood_silver.isnull().sum())

print("\nDuplicate records:")
print(flood_silver.duplicated().sum())
#-------------------------------------------------------------------------------------------------------------------------------


# STEP 1 - CREATE ROAD DATASET COPY

road_clean = road.copy()

print("\nRoad dataset copy created successfully!")


# STEP 2 - ROAD COMPLAINTS COLUMN ANALYSIS

print("\n========== ROAD COMPLAINTS COLUMN ANALYSIS ==========")

print("\n1. Dataset Shape:")
print(road_clean.shape)

print("\n2. Column Names:")
print(road_clean.columns.tolist())

print("\n3. Data Types:")
print(road_clean.dtypes)

print("\n4. Missing Values:")
print(road_clean.isnull().sum())

print("\n5. Duplicate Rows:")
print(road_clean.duplicated().sum())

print("\n6. First 5 Records:")
print(road_clean.head())


# STEP 3 - CHECK DUPLICATE COMPLAINT RECORDS

print("\n========== DUPLICATE COMPLAINT ANALYSIS ==========")

duplicate_ids = road_clean[
    road_clean["road_complaint_id"].duplicated(keep=False)
]

print("\nDuplicate Complaint Records:")
print(duplicate_ids.sort_values("road_complaint_id"))

print("\nDuplicate Complaint IDs:")
print(road_clean["road_complaint_id"].duplicated().sum())


# STEP 4 - REMOVE DUPLICATE RECORDS

print("\n========== DUPLICATE REMOVAL ==========")

original_records = len(road_clean)

road_clean = road_clean.drop_duplicates()

print("Original records:", original_records)
print("Records after duplicate removal:", len(road_clean))
print("Records removed:", original_records - len(road_clean))

print("\nRemaining Duplicate Rows:")
print(road_clean.duplicated().sum())

print("\nRemaining Duplicate Complaint IDs:")
print(road_clean["road_complaint_id"].duplicated().sum())


# STEP 5 - CHECK UNIQUE VALUES AND TEXT QUALITY

print("\n========== ROAD COMPLAINTS UNIQUE VALUE ANALYSIS ==========")

columns = [
    "zone_name",
    "damage_type",
    "severity",
    "status",
    "reported_channel",
    "probable_cause"]

for col in columns:
    print(f"\n{col}:")
    print(road_clean[col].unique())


print("\n========== TEXT QUALITY CHECK ==========")

for col in columns:
    spaces = (road_clean[col] != road_clean[col].str.strip()).sum()
    case_values = road_clean[col].str.lower().nunique()

    print(f"\nColumn: {col}")
    print("Values with extra spaces:", spaces)
    print("Unique values ignoring case:", case_values)


# STEP 6 - DATE AND LOCATION ANALYSIS

print("\n========== COMPLAINT DATE ANALYSIS ==========")

print("\nFirst 10 Complaint Dates:")
print(road_clean["complaint_date"].head(10))

print("\nLast 10 Complaint Dates:")
print(road_clean["complaint_date"].tail(10))

print("\nComplaint Date Data Type:")
print(road_clean["complaint_date"].dtype)

# Convert complaint date into date format
road_clean["complaint_date"] = pd.to_datetime(
    road_clean["complaint_date"],
    errors="coerce"
)

print("\nConverted Date Data Type:")
print(road_clean["complaint_date"].dtype)

print("\nInvalid or Missing Dates:")
print(road_clean["complaint_date"].isnull().sum())


print("\n========== LOCATION ID ANALYSIS ==========")

print("\nTotal Unique Location IDs:")
print(road_clean["location_id"].nunique())

print("\nDuplicate Location IDs:")
print(road_clean["location_id"].duplicated().sum())

print("\nUnique Location-Zone Combinations:")
print(road_clean[["location_id", "zone_id"]].drop_duplicates().shape[0])

print("\nLatitude Range:")
print(road_clean["latitude"].min(), road_clean["latitude"].max())

print("\nLongitude Range:")
print(road_clean["longitude"].min(), road_clean["longitude"].max())

print("\nMissing Coordinates:")
print(road_clean[["latitude", "longitude"]].isnull().sum())


# STEP 7 - ROAD COMPLAINTS CATEGORY ANALYSIS

print("\n========== SEVERITY ANALYSIS ==========")
print(road_clean["severity"].value_counts())

print("\n========== DAMAGE TYPE ANALYSIS ==========")
print(road_clean["damage_type"].value_counts())

print("\n========== REPORTED CHANNEL ANALYSIS ==========")
print(road_clean["reported_channel"].value_counts())

print("\n========== PROBABLE CAUSE ANALYSIS ==========")
print(road_clean["probable_cause"].value_counts())

print("\n========== COMPLAINT STATUS ANALYSIS ==========")
print(road_clean["status"].value_counts())

print("\n========== ZONE-WISE COMPLAINT ANALYSIS ==========")
print(road_clean["zone_name"].value_counts())

print("\n========== SEVERITY AND STATUS CHECK ==========")
print(pd.crosstab(road_clean["severity"], road_clean["status"]))


# ROAD COMPLAINTS CLEANING SUMMARY

print("\n========== ROAD CLEANING SUMMARY ==========")

print("Original records:", len(road))
print("Cleaned records:", len(road_clean))

print("\nMissing Values:")
print(road_clean.isnull().sum())

print("\nDuplicate Rows:")
print(road_clean.duplicated().sum())

print("\nDuplicate Complaint IDs:")
print(road_clean["road_complaint_id"].duplicated().sum())

print("\nData Types:")
print(road_clean.dtypes)


# STEP 8 - SAVE CLEANED ROAD DATASET

road_file = silver_path / "road_complaints_cleaned.csv"

road_clean.to_csv(road_file, index=False)

print("\nRoad Complaints dataset saved successfully!")
print("Saved location:", road_file)


# STEP 9 - VERIFY SILVER DATASET

road_silver = pd.read_csv(road_file)

print("\n========== SILVER DATA VERIFICATION ==========")

print("Total rows:", road_silver.shape[0])
print("Total columns:", road_silver.shape[1])

print("\nFirst 5 Records:")
print(road_silver.head())

print("\nMissing Values:")
print(road_silver.isnull().sum())

print("\nDuplicate Records:")
print(road_silver.duplicated().sum())

#--------------------------------------------------------------------------------------------------------------

# STEP 1 - CREATE TRAFFIC DATASET COPY

traffic_clean = traffic.copy()

print("\nTraffic dataset copy created successfully!")


# STEP 2 - TRAFFIC COLUMN ANALYSIS

print("\n========== TRAFFIC COLUMN ANALYSIS ==========")

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


# STEP 3 - CHECK DUPLICATE TRAFFIC RECORDS

print("\n========== TRAFFIC DUPLICATE ANALYSIS ==========")

print("\nDuplicate Traffic Record IDs:")
print(traffic_clean["traffic_record_id"].duplicated().sum())

duplicate_ids = traffic_clean[
    traffic_clean["traffic_record_id"].duplicated(keep=False)
]

print("\nDuplicate ID Records:")
print(duplicate_ids.sort_values("traffic_record_id"))


# STEP 4 - CHECK UNIQUE VALUES

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


# STEP 5 - CHECK AND CLEAN TEXT VALUES

print("\n========== TEXT QUALITY CHECK ==========")

for col in columns:
    print(f"\nColumn: {col}")

    spaces = (
        traffic_clean[col] != traffic_clean[col].str.strip()
    ).sum()

    case_values = traffic_clean[col].str.lower().nunique()

    print("Values with extra spaces:", spaces)
    print("Unique values ignoring case:", case_values)

# Remove leading and trailing spaces
for col in columns:
    traffic_clean[col] = traffic_clean[col].str.strip()


# STEP 6 - TIMESTAMP AND LOCATION ANALYSIS

print("\n========== TIMESTAMP ANALYSIS ==========")

print("\nFirst 10 Records:")
print(traffic_clean["recorded_at"].head(10))

print("\nLast 10 Records:")
print(traffic_clean["recorded_at"].tail(10))

# Convert timestamp into datetime format
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


print("\n========== LOCATION NAME ANALYSIS ==========")

print("\nTotal Unique Location Names:")
print(traffic_clean["location_name"].nunique())

print("\nSample Location Names:")
print(traffic_clean["location_name"].unique()[:20])


# STEP 7 - COORDINATE AND SPEED ANALYSIS

print("\n========== COORDINATE ANALYSIS ==========")

print("\nLatitude Range:")
print(traffic_clean["latitude"].min(), traffic_clean["latitude"].max())

print("\nLongitude Range:")
print(traffic_clean["longitude"].min(), traffic_clean["longitude"].max())

print("\nMissing Coordinates:")
print(traffic_clean[["latitude", "longitude"]].isnull().sum())


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


print("\n========== AVERAGE SPEED ANALYSIS ==========")

print("\nMinimum Average Speed:")
print(traffic_clean["avg_speed_kmph"].min())

print("\nMaximum Average Speed:")
print(traffic_clean["avg_speed_kmph"].max())

print("\nNegative Average Speed Values:")
print((traffic_clean["avg_speed_kmph"] < 0).sum())


# STEP 8 - TRAFFIC CLEANING SUMMARY

print("\n========== TRAFFIC CLEANING SUMMARY ==========")

print("Original records:", len(traffic))
print("Cleaned records:", len(traffic_clean))

print("\nMissing Values:")
print(traffic_clean.isnull().sum())

print("\nDuplicate Rows:")
print(traffic_clean.duplicated().sum())

print("\nDuplicate Traffic IDs:")
print(traffic_clean["traffic_record_id"].duplicated().sum())

print("\nData Types:")
print(traffic_clean.dtypes)


# STEP 9 - SAVE CLEANED TRAFFIC DATASET

traffic_file = silver_path / "traffic_cleaned.csv"

traffic_clean.to_csv(traffic_file, index=False)

print("\nTraffic dataset saved successfully!")
print("Saved location:", traffic_file)


# VERIFY SILVER DATASET

traffic_silver = pd.read_csv(traffic_file)

print("\n========== SILVER DATA VERIFICATION ==========")

print("Total rows:", traffic_silver.shape[0])
print("Total columns:", traffic_silver.shape[1])

print("\nFirst 5 Records:")
print(traffic_silver.head())

print("\nMissing Values:")
print(traffic_silver.isnull().sum())

print("\nDuplicate Records:")
print(traffic_silver.duplicated().sum())
#--------------------------------------------------
# LOAD PUBLIC GRIEVANCES DATASET

grievances = pd.read_excel(raw_path / "05_public_grievances.xlsx")

# Create a copy
grievances_clean = grievances.copy()

# STEP 2 - BASIC DATASET ANALYSIS

print("\n========== PUBLIC GRIEVANCES ANALYSIS ==========")

print("\n1. Dataset Shape:")
print(grievances_clean.shape)

print("\n2. Column Names:")
print(grievances_clean.columns.tolist())

print("\n3. Data Types:")
print(grievances_clean.dtypes)

print("\n4. Missing Values:")
print(grievances_clean.isnull().sum())

print("\n5. Duplicate Rows:")
print(grievances_clean.duplicated().sum())

print("\n6. First 5 Records:")
print(grievances_clean.head())


# STEP 3 - CHECK DUPLICATE GRIEVANCE IDs
print("\nDuplicate Grievance IDs:")
print(grievances_clean["grievance_id"].duplicated().sum())

# Display duplicate records
duplicate_ids = grievances_clean[
    grievances_clean["grievance_id"].duplicated(keep=False)]

print("\nDuplicate Records:")
print(duplicate_ids.sort_values("grievance_id"))

# STEP 4 - REMOVE DUPLICATE ROWS
grievances_clean = grievances_clean.drop_duplicates()

print("\nDataset Shape:")
print(grievances_clean.shape)

print("\nRemaining Duplicate Rows:")
print(grievances_clean.duplicated().sum())

print("\nRemaining Duplicate Grievance IDs:")
print(grievances_clean["grievance_id"].duplicated().sum())


# STEP 5 - UNIQUE VALUE ANALYSIS
print("\n========== GRIEVANCE UNIQUE VALUE ANALYSIS ==========")

columns = [
    "zone_name",
    "complaint_category",
    "priority",
    "status",
    "channel"]

for col in columns:
    print(f"\n{col}:")
    print(grievances_clean[col].unique())


# STEP 6 - TEXT QUALITY CHECK
columns = [
    "zone_name",
    "location_name",
    "complaint_category",
    "priority",
    "status",
    "channel"]
for col in columns:

    print(f"\nColumn: {col}")

    print(
        "Extra Spaces:",
        (grievances_clean[col] != grievances_clean[col].str.strip()).sum())

    print(
        "Unique Values Ignoring Case:",
        grievances_clean[col].str.lower().nunique())

# STEP 7 - CLEAN TEXT COLUMNS
for col in columns:
    grievances_clean[col] = grievances_clean[col].str.strip()

# STEP 8 - COMPLAINT DATE ANALYSIS
print("\nFirst 10 Dates:")
print(grievances_clean["complaint_date"].head(10))

print("\nDate Data Type:")
print(grievances_clean["complaint_date"].dtype)


# STEP 9 - CONVERT DATE COLUMN
grievances_clean["complaint_date"] = pd.to_datetime(
    grievances_clean["complaint_date"],
    errors="coerce")

print("\nDate Data Type:")
print(grievances_clean["complaint_date"].dtype)

print("\nInvalid Dates:")
print(grievances_clean["complaint_date"].isnull().sum())


# STEP 10 - LOCATION ID ANALYSIS
print("\nUnique Location IDs:")
print(grievances_clean["location_id"].nunique())

print("\nDuplicate Location IDs:")
print(grievances_clean["location_id"].duplicated().sum())

print("\nUnique Location Names:")
print(grievances_clean["location_name"].nunique())


# STEP 11 - COORDINATE ANALYSIS
print("\nLatitude Range:")
print(grievances_clean["latitude"].min(),
      grievances_clean["latitude"].max())

print("\nLongitude Range:")
print(grievances_clean["longitude"].min(),
      grievances_clean["longitude"].max())

print("\nMissing Coordinates:")
print(grievances_clean[["latitude", "longitude"]].isnull().sum())


# STEP 12 - INVALID COORDINATE CHECK
print("\nInvalid Latitude:")
print(
    ((grievances_clean["latitude"] < -90) |
     (grievances_clean["latitude"] > 90)).sum())

print("\nInvalid Longitude:")
print(
    ((grievances_clean["longitude"] < -180) |
     (grievances_clean["longitude"] > 180)).sum())


# STEP 13 - DAYS TO CLOSE ANALYSIS
print("\n========== DAYS TO CLOSE ANALYSIS ==========")

print("\nMinimum Days:")
print(grievances_clean["days_to_close"].min())

print("\nMaximum Days:")
print(grievances_clean["days_to_close"].max())

print("\nNegative Values:")
print((grievances_clean["days_to_close"] < 0).sum())

print("\nZero Values:")
print((grievances_clean["days_to_close"] == 0).sum())


# STEP 14 - PRIORITY AND STATUS CHECK
print("\n========== PRIORITY AND STATUS CHECK ==========")

print(
    pd.crosstab(
        grievances_clean["priority"],
        grievances_clean["status"]))

# STEP 15 - FINAL DATA QUALITY CHECK
print("\n========== FINAL GRIEVANCE DATA QUALITY ==========")

print("\nDataset Shape:")
print(grievances_clean.shape)

print("\nMissing Values:")
print(grievances_clean.isnull().sum())

print("\nDuplicate Rows:")
print(grievances_clean.duplicated().sum())

print("\nDuplicate Grievance IDs:")
print(grievances_clean["grievance_id"].duplicated().sum())

print("\nData Types:")
print(grievances_clean.dtypes)

print("\nFirst 5 Records:")
print(grievances_clean.head())


# STEP 16 - SAVE CLEANED GRIEVANCES DATASET
grievances_file = silver_path / "public_grievances_cleaned.csv"

grievances_clean.to_csv(grievances_file, index=False)

print("\nPublic Grievances dataset saved successfully!")
print("Saved location:", grievances_file)

#-----------------------------------------------------------------------------------

# STEP 1 - LOAD WATERLOGGING DATASET
waterlogging = pd.read_csv(raw_path / "06_waterlogging_locations.csv")

# Create a working copy
waterlogging_clean = waterlogging.copy()


# STEP 2 - BASIC DATASET ANALYSIS
print("\n========== WATERLOGGING DATASET ANALYSIS ==========")

print("\n1. Dataset Shape:")
print(waterlogging_clean.shape)

print("\n2. Column Names:")
print(waterlogging_clean.columns.tolist())

print("\n3. Data Types:")
print(waterlogging_clean.dtypes)

print("\n4. Missing Values:")
print(waterlogging_clean.isnull().sum())

print("\n5. Duplicate Rows:")
print(waterlogging_clean.duplicated().sum())

print("\n6. First 5 Records:")
print(waterlogging_clean.head())


# STEP 3 - DUPLICATE RECORD ANALYSIS
print("\n========== DUPLICATE ANALYSIS ==========")

print("Duplicate Rows:")
print(waterlogging_clean.duplicated().sum())

print("\nDuplicate Records:")
print(waterlogging_clean[
    waterlogging_clean.duplicated(keep=False)])


# STEP 4 - UNIQUE VALUE ANALYSIS

print("\n========== UNIQUE VALUE ANALYSIS ==========")

text_columns = waterlogging_clean.select_dtypes(
    include=["object", "str"]
).columns

for col in text_columns:

    print(f"\n{col}:")

    print(waterlogging_clean[col].unique()[:30])


# STEP 5 - TEXT QUALITY CHECK
print("\n========== TEXT QUALITY CHECK ==========")

for col in text_columns:

    print("\nColumn:", col)

    print(
        "Values with extra spaces:",
        (waterlogging_clean[col] !=
         waterlogging_clean[col].str.strip()).sum())

# STEP 6 - CLEAN TEXT COLUMNS
for col in text_columns:

    waterlogging_clean[col] = (
        waterlogging_clean[col].str.strip())


# STEP 7 - DATE COLUMN ANALYSIS
print("\n========== DATE COLUMN ANALYSIS ==========")

for col in waterlogging_clean.columns:

    if "date" in col.lower() or "time" in col.lower():

        print("\nColumn:", col)
        print(waterlogging_clean[col].head(10))
        print("Data Type:", waterlogging_clean[col].dtype)


# STEP 8 - CONVERT DATE COLUMNS
for col in waterlogging_clean.columns:

    if "date" in col.lower() or "time" in col.lower():

        waterlogging_clean[col] = pd.to_datetime(
            waterlogging_clean[col],
            errors="coerce"
        )

        print("\nColumn:", col)
        print("Data Type:", waterlogging_clean[col].dtype)
        print("Invalid Dates:", waterlogging_clean[col].isnull().sum())


    
# STEP 9 - NUMERICAL VALUE ANALYSIS

print("\n========== NUMERICAL VALUE ANALYSIS ==========")

numeric_columns = waterlogging_clean.select_dtypes(
    include="number"
).columns

for col in numeric_columns:

    print("\nColumn:", col)

    print("Minimum:", waterlogging_clean[col].min())
    print("Maximum:", waterlogging_clean[col].max())
    print("Missing Values:", waterlogging_clean[col].isnull().sum())


# STEP 10 - COORDINATE ANALYSIS
if "latitude" in waterlogging_clean.columns and "longitude" in waterlogging_clean.columns:

    print("\nLatitude Range:")
    print(waterlogging_clean["latitude"].min(),
          waterlogging_clean["latitude"].max())

    print("\nLongitude Range:")
    print(waterlogging_clean["longitude"].min(),
          waterlogging_clean["longitude"].max())

    print("\nMissing Coordinates:")
    print(waterlogging_clean[["latitude", "longitude"]].isnull().sum())

    print("\nInvalid Latitude:")
    print(((waterlogging_clean["latitude"] < -90) |
           (waterlogging_clean["latitude"] > 90)).sum())

    print("\nInvalid Longitude:")
    print(((waterlogging_clean["longitude"] < -180) |
           (waterlogging_clean["longitude"] > 180)).sum())



# STEP 11 - FINAL DATA QUALITY CHECK

print("\n========== FINAL WATERLOGGING DATA QUALITY ==========")

print("\nDataset Shape:")
print(waterlogging_clean.shape)

print("\nMissing Values:")
print(waterlogging_clean.isnull().sum())

print("\nDuplicate Rows:")
print(waterlogging_clean.duplicated().sum())

print("\nData Types:")
print(waterlogging_clean.dtypes)

print("\nFirst 5 Records:")
print(waterlogging_clean.head())


# STEP 12 - SAVE CLEANED WATERLOGGING DATASET


waterlogging_file = silver_path / "waterlogging_locations_cleaned.csv"

waterlogging_clean.to_csv(
    waterlogging_file,
    index=False
)

print("\nWaterlogging dataset saved successfully!")
print("Saved location:", waterlogging_file)


#---------------------------------------------------------------
# POPULATION DENSITY DATA CLEANING

# STEP 1 - CREATE A COPY
population_clean = population.copy()

# STEP 2 - BASIC DATASET ANALYSIS
print("\n========== POPULATION DATASET ANALYSIS ==========")

print("\n1. Dataset Shape:")
print(population_clean.shape)

print("\n2. Column Names:")
print(population_clean.columns.tolist())

print("\n3. Data Types:")
print(population_clean.dtypes)

print("\n4. Missing Values:")
print(population_clean.isnull().sum())

print("\n5. Duplicate Rows:")
print(population_clean.duplicated().sum())

print("\n6. First 5 Records:")
print(population_clean.head())

# STEP 3 - CHECK DUPLICATE RECORDS
print("\n========== DUPLICATE RECORD CHECK ==========")

print("Duplicate Rows:")
print(population_clean.duplicated().sum())

population_clean = population_clean.drop_duplicates()

print("Shape After Removing Duplicates:")
print(population_clean.shape)

# STEP 4 - CHECK MISSING VALUES
print("\n========== MISSING VALUE CHECK ==========")

print(population_clean.isnull().sum())

print("\nTotal Missing Values:")
print(population_clean.isnull().sum().sum())

# STEP 5 - CHECK MISSING VALUE PERCENTAGE
print("\n========== MISSING VALUE PERCENTAGE ==========")
missing_percentage = (
    population_clean.isnull().sum() / len(population_clean)
) * 100

print(missing_percentage)

# STEP 6 - CHECK DUPLICATE IDs
print("\n========== DUPLICATE ID CHECK ==========")

for column in population_clean.columns:
    if "id" in column.lower():
        print(f"\nDuplicate values in {column}:")
        print(population_clean[column].duplicated().sum())

# STEP 7 - CHECK TEXT COLUMNS
print("\n========== TEXT QUALITY CHECK ==========")

text_columns = population_clean.select_dtypes(
    include=["object", "string"]
).columns

for column in text_columns:
    print(f"\nColumn: {column}")
    print("Unique Values:")
    print(population_clean[column].unique()[:30])

    if population_clean[column].dtype == "object":
        population_clean[column] = population_clean[column].str.strip()

# STEP 8 - CHECK NUMERIC COLUMNS
print("\n========== NUMERIC VALUE CHECK ==========")

numeric_columns = population_clean.select_dtypes(
    include=["int64", "float64"]
).columns

print(population_clean[numeric_columns].describe())

# STEP 9 - CHECK ABNORMAL VALUES

print("\n========== ABNORMAL VALUE CHECK ==========")

for column in numeric_columns:
    print(f"\nColumn: {column}")
    print("Minimum Value:", population_clean[column].min())
    print("Maximum Value:", population_clean[column].max())


# STEP 10 - CHECK ZERO AND NEGATIVE VALUES

print("\n========== ZERO AND NEGATIVE VALUE CHECK ==========")

for column in numeric_columns:
    print(f"\nColumn: {column}")

    print("Zero Values:",
          (population_clean[column] == 0).sum())

    print("Negative Values:",
          (population_clean[column] < 0).sum())

# STEP 11 - CHECK DATE COLUMNS

print("\n========== DATE COLUMN CHECK ==========")

for column in population_clean.columns:
    if "date" in column.lower() or "year" in column.lower():
        print(f"\nColumn: {column}")
        print(population_clean[column].head())

# STEP 12 - CHECK UNIQUE VALUES

print("\n========== UNIQUE VALUE CHECK ==========")

for column in population_clean.columns:
    print(f"\n{column}:")
    print("Unique Count:", population_clean[column].nunique())

# STEP 13 - CHECK FINAL DATA TYPES

print("\n========== FINAL DATA TYPES ==========")

print(population_clean.dtypes)

# STEP 14 - FINAL MISSING VALUE CHECK

print("\n========== FINAL MISSING VALUE CHECK ==========")

print(population_clean.isnull().sum())

# STEP 15 - FINAL DUPLICATE CHECK

print("\n========== FINAL DUPLICATE CHECK ==========")

print("Duplicate Rows:",
      population_clean.duplicated().sum())

# STEP 16 - FINAL DATASET SHAPE

print("\n========== FINAL DATASET SHAPE ==========")

print("Final Shape:", population_clean.shape)

# STEP 17 - SAVE CLEANED DATASET

population_clean.to_csv(
    silver_path / "population_cleaned.csv",
    index=False
)

print("\nPopulation cleaned dataset saved successfully!")



#---------------------------------------------------------------
# EMERGENCY RESPONSE DATA CLEANING

# STEP 1 - CREATE A COPY
emergency_clean = emergency.copy()

# STEP 2 - BASIC DATASET ANALYSIS

print("\n========== EMERGENCY RESPONSE DATASET ANALYSIS ==========")

print("\n1. Dataset Shape:")
print(emergency_clean.shape)

print("\n2. Column Names:")
print(emergency_clean.columns.tolist())

print("\n3. Data Types:")
print(emergency_clean.dtypes)

print("\n4. Missing Values:")
print(emergency_clean.isnull().sum())

print("\n5. Duplicate Rows:")
print(emergency_clean.duplicated().sum())

print("\n6. First 5 Records:")
print(emergency_clean.head())


# STEP 3 - CHECK DUPLICATE RECORDS

print("\n========== DUPLICATE RECORD CHECK ==========")

print("Duplicate Rows:")
print(emergency_clean.duplicated().sum())

emergency_clean = emergency_clean.drop_duplicates()

print("Shape After Removing Duplicates:")
print(emergency_clean.shape)


# STEP 4 - CHECK MISSING VALUES

print("\n========== MISSING VALUE CHECK ==========")

print(emergency_clean.isnull().sum())

print("\nTotal Missing Values:")
print(emergency_clean.isnull().sum().sum())


# STEP 5 - CHECK MISSING VALUE PERCENTAGE

print("\n========== MISSING VALUE PERCENTAGE ==========")

missing_percentage = (
    emergency_clean.isnull().sum() / len(emergency_clean)
) * 100

print(missing_percentage)


# STEP 6 - CHECK DUPLICATE IDs

print("\n========== DUPLICATE ID CHECK ==========")

for column in emergency_clean.columns:
    if "id" in column.lower():
        print(f"\nDuplicate values in {column}:")
        print(emergency_clean[column].duplicated().sum())


# STEP 7 - CHECK TEXT COLUMNS

print("\n========== TEXT QUALITY CHECK ==========")

text_columns = emergency_clean.select_dtypes(
    include=["object", "string"]
).columns

for column in text_columns:
    print(f"\nColumn: {column}")
    print("Unique Values:")
    print(emergency_clean[column].unique()[:30])

    if emergency_clean[column].dtype == "object":
        emergency_clean[column] = emergency_clean[column].str.strip()


# STEP 8 - CHECK NUMERIC COLUMNS

print("\n========== NUMERIC VALUE CHECK ==========")

numeric_columns = emergency_clean.select_dtypes(
    include=["int64", "float64"]
).columns

print(emergency_clean[numeric_columns].describe())


# STEP 9 - CHECK ABNORMAL VALUES

print("\n========== ABNORMAL VALUE CHECK ==========")

for column in numeric_columns:
    print(f"\nColumn: {column}")
    print("Minimum Value:", emergency_clean[column].min())
    print("Maximum Value:", emergency_clean[column].max())


# STEP 10 - CHECK ZERO AND NEGATIVE VALUES

print("\n========== ZERO AND NEGATIVE VALUE CHECK ==========")

for column in numeric_columns:
    print(f"\nColumn: {column}")

    print("Zero Values:",
          (emergency_clean[column] == 0).sum())

    print("Negative Values:",
          (emergency_clean[column] < 0).sum())


# STEP 11 - CHECK DATE AND TIME COLUMNS

print("\n========== DATE AND TIME CHECK ==========")

for column in emergency_clean.columns:
    if any(word in column.lower() for word in ["date", "time"]):
        print(f"\nColumn: {column}")
        print(emergency_clean[column].head())


 #  CONVERT INCIDENT DATE TO DATETIME

print("\n========== INCIDENT DATE CONVERSION ==========")

emergency_clean["incident_date"] = pd.to_datetime(
    emergency_clean["incident_date"],
    errors="coerce"
)

print("\nIncident Date Data Type:")
print(emergency_clean["incident_date"].dtype)

print("\nInvalid Dates:")
print(emergency_clean["incident_date"].isnull().sum())


# STEP 12 - CHECK UNIQUE VALUES

print("\n========== UNIQUE VALUE CHECK ==========")

for column in emergency_clean.columns:
    print(f"\n{column}:")
    print("Unique Count:", emergency_clean[column].nunique())


# STEP 13 - CHECK FINAL DATA TYPES

print("\n========== FINAL DATA TYPES ==========")

print(emergency_clean.dtypes)


# STEP 14 - FINAL MISSING VALUE CHECK

print("\n========== FINAL MISSING VALUE CHECK ==========")

print(emergency_clean.isnull().sum())


# STEP 15 - FINAL DUPLICATE CHECK

print("\n========== FINAL DUPLICATE CHECK ==========")

print("Duplicate Rows:",
      emergency_clean.duplicated().sum())


# STEP 16 - FINAL DATASET SHAPE

print("\n========== FINAL DATASET SHAPE ==========")

print("Final Shape:", emergency_clean.shape)


# STEP 17 - SAVE CLEANED DATASET

emergency_clean.to_csv(
    silver_path / "emergency_response_cleaned.csv",
    index=False
)

print("\nEmergency response cleaned dataset saved successfully!")




# REPORTS FOLDER
reports_path = project_path / "reports"

# CREATE REPORTS FOLDER IF NOT EXISTS
reports_path.mkdir(parents=True, exist_ok=True)



# ==========================================
# VERIFY ALL 8 SILVER DATASETS

print("\n========== SILVER LAYER VERIFICATION ==========")

silver_files = {
    "Rainfall": "rainfall_cleaned.csv",
    "Flood": "flood_cleaned.csv",
    "Road Complaints": "road_complaints_cleaned.csv",
    "Traffic": "traffic_cleaned.csv",
    "Public Grievances": "public_grievances_cleaned.csv",
    "Waterlogging": "waterlogging_locations_cleaned.csv",
    "Population": "population_cleaned.csv",
    "Emergency Response": "emergency_response_cleaned.csv"
}

verification_results = []

for name, filename in silver_files.items():

    file_path = silver_path / filename

    print(f"\nChecking: {name}")

    if file_path.exists():

        df = pd.read_csv(file_path)

        print("File Status: Available")
        print("Dataset Shape:", df.shape)
        print("Columns:", df.columns.tolist())
        print("Missing Values:", df.isnull().sum().sum())
        print("Duplicate Rows:", df.duplicated().sum())

        verification_results.append({
            "dataset": name,
            "file": filename,
            "status": "Available",
            "rows": df.shape[0],
            "columns": df.shape[1],
            "missing_values": df.isnull().sum().sum(),
            "duplicate_rows": df.duplicated().sum()
        })

    else:

        print("File Status: NOT FOUND")

        verification_results.append({
            "dataset": name,
            "file": filename,
            "status": "Not Found",
            "rows": 0,
            "columns": 0,
            "missing_values": 0,
            "duplicate_rows": 0
        })


# FINAL VERIFICATION REPORT

verification_df = pd.DataFrame(verification_results)

print("\n========== FINAL SILVER VERIFICATION REPORT ==========")

print(verification_df.to_string(index=False))

print("\nAvailable Datasets:",
      (verification_df["status"] == "Available").sum())

print("Missing Files:",
      (verification_df["status"] == "Not Found").sum())


# SAVE VERIFICATION REPORT

verification_df.to_csv(
    reports_path / "silver_layer_verification.csv",
    index=False
)

print("\nSilver verification report saved successfully!")



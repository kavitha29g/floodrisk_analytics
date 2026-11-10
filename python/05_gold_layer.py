
# STEP 1 - IMPORT LIBRARIES
from pathlib import Path
import pandas as pd
import numpy as np

print("\n========== GOLD LAYER DEVELOPMENT ==========")

# STEP 2 - PROJECT PATHS
project_path = Path(__file__).resolve().parent.parent
silver_path = project_path / "data" / "silver"
gold_path = project_path / "data" / "gold"
reports_path = project_path / "reports"


# Create folders if they do not exist
gold_path.mkdir(parents=True, exist_ok=True)
reports_path.mkdir(parents=True, exist_ok=True)


print("\nProject Path:", project_path)
print("Silver Path:", silver_path)
print("Gold Path:", gold_path)


# STEP 3 - 8 SILVER DATASETS
print("\n========== LOADING SILVER DATASETS ==========")

rainfall = pd.read_csv(
    silver_path / "rainfall_cleaned.csv")

flood = pd.read_csv(
    silver_path / "flood_cleaned.csv")

road = pd.read_csv(
    silver_path / "road_complaints_cleaned.csv")

traffic = pd.read_csv(
    silver_path / "traffic_cleaned.csv")

grievances = pd.read_csv(
    silver_path / "public_grievances_cleaned.csv")

waterlogging = pd.read_csv(
    silver_path / "waterlogging_locations_cleaned.csv")

population = pd.read_csv(
    silver_path / "population_cleaned.csv")

emergency = pd.read_csv(
    silver_path / "emergency_response_cleaned.csv")

print("\nAll 8 Silver datasets loaded successfully!")

# STEP 4 - STORE DATASETS IN A DICTIONARY


datasets = {

    "Rainfall": rainfall,

    "Flood": flood,

    "Road Complaints": road,

    "Traffic": traffic,

    "Public Grievances": grievances,

    "Waterlogging": waterlogging,

    "Population": population,

    "Emergency Response": emergency}

# STEP 5 - DISPLAY DATASET DETAILS
print("\n========== GOLD DATASET DETAILS ==========")

for name, df in datasets.items():

    print("\nDataset:", name)

    print("Shape:", df.shape)

    print("Columns:", df.columns.tolist())

# STEP 6 - CHECK MISSING VALUES
print("\n========== MISSING VALUE CHECK ==========")
for name, df in datasets.items():

    print("\nDataset:", name)

    print("Total Missing Values:",
          df.isnull().sum().sum())

# STEP 7 - CHECK DUPLICATE ROWS
print("\n========== DUPLICATE ROW CHECK ==========")
for name, df in datasets.items():

    print("\nDataset:", name)

    print("Duplicate Rows:",
          df.duplicated().sum())

# STEP 8 - CREATE GOLD LOADING VERIFICATION REPORT
verification_report = []

for name, df in datasets.items():

    verification_report.append({

        "dataset": name,

        "rows": df.shape[0],

        "columns": df.shape[1],

        "missing_values": df.isnull().sum().sum(),

        "duplicate_rows": df.duplicated().sum(),

        "status": "Loaded Successfully"})


gold_report = pd.DataFrame(verification_report)

print("\n========== GOLD LOADING VERIFICATION REPORT ==========")
print(gold_report.to_string(index=False))


# STEP 9 - SAVE GOLD LOADING VERIFICATION REPORT
gold_report.to_csv(

    reports_path / "gold_loading_verification_report.csv",

    index=False

)

print("\nGold loading verification report saved successfully!")

# STEP 10 - FINAL SUMMARY

print("\n========== FINAL GOLD LOADING SUMMARY ==========")

print("Total Datasets Loaded:", len(datasets))

print("Gold Folder Available:", gold_path.exists())

print("Verification Report Saved:", 
      (reports_path / "gold_loading_verification_report.csv").exists())


print("\n========== GOLD LAYER INITIAL SETUP COMPLETED ==========")

#===================================================================================================

 #IDENTIFYING MISSING RECORDS
print("\n========== MISSING RECORD ANALYSIS ==========")

# Rainfall missing values

print("\n1. RAINFALL MISSING VALUES")

print(rainfall.isnull().sum())

# Traffic missing values

print("\n2. TRAFFIC MISSING VALUES")

print(traffic.isnull().sum())

# Road complaints missing values

print("\n3. ROAD CONDITION MISSING VALUES")

road_columns = ["damage_type","severity","status"]

print(road[road_columns].isnull().sum())


# Display records with missing rainfall

missing_rainfall = rainfall[rainfall["rainfall_mm"].isnull()]

print("\nMissing Rainfall Records:")

print(missing_rainfall.head())


# Display records with missing traffic speed

missing_traffic = traffic[traffic["avg_speed_kmph"].isnull()]

print("\nMissing Traffic Records:")

print(missing_traffic.head())


# Display records with missing road condition

missing_road = road[road[road_columns].isnull().any(axis=1)]

print("\nMissing Road Condition Records:")

print(missing_road.head())


# ======================================================================================
#  IDENTIFYING DUPLICATE COMPLAINTS

print("\n========== DUPLICATE COMPLAINT ANALYSIS ==========")

# Check duplicate complaint IDs

duplicate_ids = grievances[
    grievances.duplicated(
        subset=["grievance_id"],
        keep=False)]

print("\nDuplicate Complaint IDs:")

print(duplicate_ids)

# Count duplicate complaint IDs

print("\nTotal Duplicate Complaint IDs:")

print(grievances["grievance_id"].duplicated().sum())


# Check completely duplicate rows

print("\nDuplicate Complete Rows:")

print(grievances.duplicated().sum())


# Check duplicates using multiple columns

duplicate_complaints = grievances[
    grievances.duplicated(
        subset=[
            "zone_id",
            "location_id",
            "complaint_category",
            "complaint_date"
        ],
        keep=False)]

print("\nPotential Duplicate Complaints:")

print(duplicate_complaints.head(10))



# ===============================================================================
# STANDARDIZING ZONE AND LOCATION

print("\n========== ZONE STANDARDIZATION ==========")


# STEP 1 - Remove extra spaces

for name, df in datasets.items():

    text_columns = [ "zone_name","location_name"]

    for column in text_columns:

        if column in df.columns:

            df[column] = (df[column].astype("string").str.strip())


# STEP 2 - Standardize zone names

zone_mapping = {

    "adyar": "Adyar",

    "anna nagar": "Anna Nagar",

    "ambattur": "Ambattur",

    "kodambakkam": "Kodambakkam",

    "perungudi": "Perungudi",

    "sholinganallur": "Sholinganallur",

    "manali": "Manali",

    "madhavaram": "Madhavaram",

    "royapuram": "Royapuram",

    "tondiarpet": "Tondiarpet",

    "tiruvottiyur": "Tiruvottiyur",

    "teynampet": "Teynampet",

    "alandur": "Alandur",

    "valasaravakkam": "Valasaravakkam",

    "thiru-vi-ka nagar": "Thiru-Vi-Ka Nagar"}


# Apply standardization to all datasets

for name, df in datasets.items():

    if "zone_name" in df.columns:

        df["zone_name"] = (df["zone_name"].str.lower().replace(zone_mapping))


# STEP 3 - Standardize location names

for name, df in datasets.items():

    if "location_name" in df.columns:

        df["location_name"] = (df["location_name"].str.strip().str.title())

# STEP 4 - Display unique zone names

print("\nStandardized Chennai Zone Names:")

print(rainfall["zone_name"].unique())


# STEP 5 - Check unique location names

print("\nSample Standardized Locations:")

print(road["location_name"].dropna().unique()[:10])


# Check invalid geographical coordinates

for name, df in datasets.items():

    if "latitude" in df.columns:

        invalid_lat = df[~df["latitude"].between(-90, 90)]

        print(name, "Invalid Latitude:",
              len(invalid_lat))

    if "longitude" in df.columns:

        invalid_long = df[~df["longitude"].between(-180, 180)]

        print(name, "Invalid Longitude:",len(invalid_long))




# ==========================================
# ABNORMAL RAINFALL ANALYSIS

print("\n========== ABNORMAL RAINFALL ANALYSIS ==========")

# Check negative rainfall

negative_rainfall = rainfall[rainfall["rainfall_mm"] < 0]

print("\nNegative Rainfall Records:")

print(negative_rainfall)


# Check unusually high rainfall

high_rainfall = rainfall[rainfall["rainfall_mm"] > 100]

print("\nRainfall Above 100 mm:")

print(high_rainfall.head(10))


# Check missing rainfall

missing_rainfall = rainfall[rainfall["rainfall_mm"].isnull()]

print("\nMissing Rainfall Records:")

print(len(missing_rainfall))



# ========================================================================
# USING IQR OUTLIER DETECTION


# Calculate Q1 and Q3

q1 = rainfall["rainfall_mm"].quantile(0.25)

q3 = rainfall["rainfall_mm"].quantile(0.75)


# Calculate IQR

iqr = q3 - q1


# Calculate lower and upper limits

lower_limit = q1 - (1.5 * iqr)

upper_limit = q3 + (1.5 * iqr)


print("\nQ1:", q1)

print("Q3:", q3)

print("IQR:", iqr)

print("Lower Limit:", lower_limit)

print("Upper Limit:", upper_limit)


# Identify outliers

rainfall_outliers = rainfall[(rainfall["rainfall_mm"] < lower_limit) |(rainfall["rainfall_mm"] > upper_limit)]


print("\nTotal Rainfall Outliers:")

print(len(rainfall_outliers))


print("\nRainfall Outlier Records:")

print(rainfall_outliers.head(10))


#=========================================================================


#  REUSABLE DATA INGESTION


def load_dataset(file_path):

    file_path = Path(file_path)

    # Check CSV files

    if file_path.suffix.lower() == ".csv":

        df = pd.read_csv(file_path)

# Check JSON files

    elif file_path.suffix.lower() == ".json":

        df = pd.read_json(file_path)


    # Check Excel files

    elif file_path.suffix.lower() in [".xlsx", ".xls"]:

        df = pd.read_excel(file_path)


    else:

        raise ValueError("Unsupported file format")


    return df

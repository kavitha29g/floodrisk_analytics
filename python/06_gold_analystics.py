# STEP 1 - IMPORT LIBRARIES
from pathlib import Path
import pandas as pd
import numpy as np
print("\n========== GOLD LAYER ANALYTICS ==========")

# ==========================================================
# STEP 2 - DEFINE PROJECT PATHS
project_path = Path(__file__).resolve().parent.parent

silver_path = project_path / "data" / "silver"

gold_path = project_path / "data" / "gold"

gold_path.mkdir(parents=True, exist_ok=True)


print("\nSilver Path:", silver_path)
print("Gold Path:", gold_path)

# STEP 3 - LOAD ALL 8 SILVER DATASETS

print("\n========== LOADING SILVER DATASETS ==========")

rainfall = pd.read_csv(silver_path / "rainfall_cleaned.csv")

flood = pd.read_csv(silver_path / "flood_cleaned.csv")

road = pd.read_csv(silver_path / "road_complaints_cleaned.csv")

traffic = pd.read_csv(silver_path / "traffic_cleaned.csv")

grievances = pd.read_csv(silver_path / "public_grievances_cleaned.csv")

waterlogging = pd.read_csv(silver_path / "waterlogging_locations_cleaned.csv")

population = pd.read_csv(silver_path / "population_cleaned.csv")

emergency = pd.read_csv(silver_path / "emergency_response_cleaned.csv")


datasets = {

    "Rainfall": rainfall,
    "Flood": flood,
    "Road Complaints": road,
    "Traffic": traffic,
    "Public Grievances": grievances,
    "Waterlogging": waterlogging,
    "Population": population,
    "Emergency Response": emergency}

print("\nAll 8 Silver datasets loaded successfully!")

# STEP 4 - STANDARDIZE ZONE ID DATA TYPE

for name, df in datasets.items():

    if "zone_id" in df.columns:

        df["zone_id"] = (df["zone_id"].astype("string").str.strip())

# STEP 5 - CONVERT NUMERIC COLUMNS
numeric_columns = {

    "Rainfall": ["rainfall_mm"],

    "Flood": ["estimated_affected_people","event_rainfall_mm"],

    "Road Complaints": [],

    "Traffic": ["avg_speed_kmph","free_flow_speed_kmph","vehicle_count"],

    "Public Grievances": ["days_to_close"],

    "Waterlogging": ["waterlogging_reports_2020_2025"],

    "Population": ["population_density_per_sq_km","estimated_population_index"],

    "Emergency Response": ["response_time_minutes","resources_deployed","people_assisted" ]}


for name, columns in numeric_columns.items():

    df = datasets[name]

    for column in columns:

        if column in df.columns:

            df[column] = pd.to_numeric(df[column],errors="coerce")


print("\nNumeric columns converted successfully!")

# STEP 6 - CREATE REUSABLE GOLD SAVE FUNCTION

def save_gold(df, file_name):

    destination = gold_path / file_name

    df.to_csv(destination, index=False)

    print("\nSaved:", file_name)

    print("Rows:", df.shape[0])

    print("Columns:", df.shape[1])


# STEP 7 - ZONE-WISE RAINFALL ANALYSIS

print("\n========== ZONE-WISE RAINFALL ANALYSIS ==========")

zone_wise_rainfall = (

    rainfall.groupby(["zone_id", "zone_name"],as_index=False).agg(

        total_rainfall_mm=("rainfall_mm", "sum"),

        average_rainfall_mm=("rainfall_mm", "mean"),

        maximum_rainfall_mm=("rainfall_mm", "max"),

        minimum_rainfall_mm=("rainfall_mm", "min"),

        valid_rainfall_records=("rainfall_mm", "count"),

        total_rainfall_records=("rainfall_mm", "size")))


zone_wise_rainfall["missing_rainfall_records"] = (zone_wise_rainfall["total_rainfall_records"]- zone_wise_rainfall["valid_rainfall_records"])


print(zone_wise_rainfall.head())

# STEP 8 - ZONE-WISE FLOOD RISK ANALYSIS


print("\n========== ZONE-WISE FLOOD ANALYSIS ==========")


flood["_severity"] = (flood["severity"].astype("string").str.strip().str.lower())


flood["_high_severity_flag"] = (flood["_severity"].isin(["severe", "high", "critical"]).astype(int))


zone_wise_flood = (flood.groupby(["zone_id", "zone_name"],as_index=False).agg(

        total_flood_incidents=("flood_event_id", "count"),

        total_affected_people=("estimated_affected_people", "sum"),

        average_event_rainfall_mm=("event_rainfall_mm", "mean"),

        high_severity_floods=("_high_severity_flag", "sum"),

        affected_locations=("location_id", "nunique")))


print(zone_wise_flood.head())



# STEP 9 - ZONE-WISE ROAD COMPLAINT ANALYSIS

print("\n========== ZONE-WISE ROAD ANALYSIS ==========")


road["_status"] = (

    road["status"]
    .astype("string")
    .str.strip()
    .str.lower()

)


road["_severity"] = (

    road["severity"]
    .astype("string")
    .str.strip()
    .str.lower()

)


road["_resolved_flag"] = (

    road["_status"]
    .eq("resolved")
    .astype(int)

)


road["_critical_flag"] = (

    road["_severity"]
    .eq("critical")
    .astype(int)

)


zone_wise_road = (

    road.groupby(
        ["zone_id", "zone_name"],
        as_index=False
    )

    .agg(

        total_road_complaints=("road_complaint_id", "count"),

        resolved_complaints=("_resolved_flag", "sum"),

        critical_road_complaints=("_critical_flag", "sum"),

        damaged_locations=("location_id", "nunique")

    )
)


zone_wise_road["unresolved_complaints"] = (

    zone_wise_road["total_road_complaints"]

    - zone_wise_road["resolved_complaints"]

)


print(zone_wise_road.head())


# ==========================================================
# STEP 10 - ZONE-WISE TRAFFIC ANALYSIS
# ==========================================================

print("\n========== ZONE-WISE TRAFFIC ANALYSIS ==========")


traffic["_congestion"] = (

    traffic["congestion_level"]
    .astype("string")
    .str.strip()
    .str.lower()

)


traffic["_high_congestion_flag"] = (

    traffic["_congestion"]
    .str.contains(
        "high|severe|heavy|critical",
        na=False
    )
    .astype(int)

)


zone_wise_traffic = (

    traffic.groupby(
        ["zone_id", "zone_name"],
        as_index=False
    )

    .agg(

        total_traffic_records=("traffic_record_id", "count"),

        average_speed_kmph=("avg_speed_kmph", "mean"),

        average_free_flow_speed_kmph=("free_flow_speed_kmph", "mean"),

        average_vehicle_count=("vehicle_count", "mean"),

        total_vehicle_count=("vehicle_count", "sum"),

        high_congestion_records=("_high_congestion_flag", "sum")

    )
)


print(zone_wise_traffic.head())


# ==========================================================
# STEP 11 - ZONE-WISE PUBLIC GRIEVANCE ANALYSIS
# ==========================================================

print("\n========== PUBLIC GRIEVANCE ANALYSIS ==========")


grievances["_status"] = (

    grievances["status"]
    .astype("string")
    .str.strip()
    .str.lower()

)


grievances["_priority"] = (

    grievances["priority"]
    .astype("string")
    .str.strip()
    .str.lower()

)


grievances["_resolved_flag"] = (

    grievances["_status"]
    .eq("resolved")
    .astype(int)

)


grievances["_high_priority_flag"] = (

    grievances["_priority"]
    .isin(["high", "critical", "urgent"])
    .astype(int)

)


zone_wise_grievances = (

    grievances.groupby(
        ["zone_id", "zone_name"],
        as_index=False
    )

    .agg(

        total_grievances=("grievance_id", "count"),

        resolved_grievances=("_resolved_flag", "sum"),

        high_priority_grievances=("_high_priority_flag", "sum"),

        average_days_to_close=("days_to_close", "mean"),

        complaint_locations=("location_id", "nunique")

    )
)


zone_wise_grievances["unresolved_grievances"] = (

    zone_wise_grievances["total_grievances"]

    - zone_wise_grievances["resolved_grievances"]

)


print(zone_wise_grievances.head())


# ==========================================================
# STEP 12 - ZONE-WISE WATERLOGGING ANALYSIS
# ==========================================================

print("\n========== WATERLOGGING ANALYSIS ==========")


waterlogging["_risk_level"] = (

    waterlogging["historical_risk_level"]
    .astype("string")
    .str.strip()
    .str.lower()

)


waterlogging["_high_risk_flag"] = (

    waterlogging["_risk_level"]
    .isin(["high", "severe", "critical"])
    .astype(int)

)


zone_wise_waterlogging = (

    waterlogging.groupby(
        ["zone_id", "zone_name"],
        as_index=False
    )

    .agg(

        total_waterlogging_sites=("waterlogging_id", "count"),

        unique_waterlogging_locations=("location_id", "nunique"),

        total_historical_reports=(
            "waterlogging_reports_2020_2025", "sum"
        ),

        high_risk_waterlogging_sites=("_high_risk_flag", "sum")

    )
)


print(zone_wise_waterlogging.head())


# ==========================================================
# STEP 13 - ZONE-WISE POPULATION ANALYSIS
# ==========================================================

print("\n========== POPULATION ANALYSIS ==========")


zone_wise_population = (

    population.groupby(
        ["year", "zone_id", "zone_name"],
        as_index=False
    )

    .agg(

        average_population_density=(
            "population_density_per_sq_km", "mean"
        ),

        estimated_population_index=(
            "estimated_population_index", "mean"
        )

    )
)


print(zone_wise_population.head())


# ==========================================================
# STEP 14 - ZONE-WISE EMERGENCY RESPONSE ANALYSIS
# ==========================================================

print("\n========== EMERGENCY RESPONSE ANALYSIS ==========")


zone_wise_emergency = (

    emergency.groupby(
        ["zone_id", "zone_name"],
        as_index=False
    )

    .agg(

        total_emergency_incidents=("response_id", "count"),

        average_response_time_minutes=(
            "response_time_minutes", "mean"
        ),

        maximum_response_time_minutes=(
            "response_time_minutes", "max"
        ),

        total_resources_deployed=("resources_deployed", "sum"),

        total_people_assisted=("people_assisted", "sum")

    )
)


print(zone_wise_emergency.head())


# ==========================================================
# STEP 15 - SAVE ALL 8 GOLD DATASETS
# ==========================================================

print("\n========== SAVING GOLD DATASETS ==========")


gold_datasets = {

    "zone_wise_rainfall.csv": zone_wise_rainfall,

    "zone_wise_flood_risk.csv": zone_wise_flood,

    "zone_wise_road_complaints.csv": zone_wise_road,

    "zone_wise_traffic.csv": zone_wise_traffic,

    "zone_wise_public_grievances.csv": zone_wise_grievances,

    "zone_wise_waterlogging.csv": zone_wise_waterlogging,

    "zone_wise_population.csv": zone_wise_population,

    "zone_wise_emergency_response.csv": zone_wise_emergency

}


for file_name, df in gold_datasets.items():

    save_gold(df, file_name)


# ==========================================================
# STEP 16 - GET LATEST POPULATION DATA BY ZONE
# ==========================================================

latest_population = (

    zone_wise_population
    .sort_values("year")
    .groupby("zone_id")
    .tail(1)
    .rename(columns={
        "year": "latest_population_year"
    })

)


# ==========================================================
# STEP 17 - CREATE ZONE MASTER DATASET
# ==========================================================

print("\n========== CREATING ZONE MASTER DATASET ==========")


zone_parts = []

for df in datasets.values():

    if {"zone_id", "zone_name"}.issubset(df.columns):

        zone_parts.append(
            df[["zone_id", "zone_name"]]
        )


zone_master = (

    pd.concat(zone_parts, ignore_index=True)

    .dropna(subset=["zone_id"])

    .drop_duplicates(subset=["zone_id"], keep="first")

)


# ==========================================================
# STEP 18 - COMBINE ALL GOLD ANALYTICS
# ==========================================================

print("\n========== COMBINING ZONE-WISE ANALYTICS ==========")


zone_wise_summary = zone_master.copy()


for df in [

    zone_wise_rainfall,

    zone_wise_flood,

    zone_wise_road,

    zone_wise_traffic,

    zone_wise_grievances,

    zone_wise_waterlogging,

    latest_population,

    zone_wise_emergency

]:

    summary_columns = df.drop(
        columns=["zone_name"],
        errors="ignore"
    )

    zone_wise_summary = zone_wise_summary.merge(

        summary_columns,

        on="zone_id",

        how="left"

    )


print("\nCombined Zone-Wise Summary:")

print(zone_wise_summary.head())


# ==========================================================
# STEP 19 - SAVE COMBINED GOLD SUMMARY
# ==========================================================

save_gold(

    zone_wise_summary,

    "zone_wise_smart_city_summary.csv"

)


# ==========================================================
# STEP 20 - GOLD LAYER FINAL VERIFICATION
# ==========================================================

print("\n========== GOLD LAYER VERIFICATION ==========")


gold_verification = []


for file_name, df in gold_datasets.items():

    gold_verification.append({

        "dataset": file_name,

        "rows": df.shape[0],

        "columns": df.shape[1],

        "missing_values": df.isnull().sum().sum(),

        "duplicate_rows": df.duplicated().sum(),

        "status": "Created Successfully"

    })


gold_verification.append({

    "dataset": "zone_wise_smart_city_summary.csv",

    "rows": zone_wise_summary.shape[0],

    "columns": zone_wise_summary.shape[1],

    "missing_values": zone_wise_summary.isnull().sum().sum(),

    "duplicate_rows": zone_wise_summary.duplicated().sum(),

    "status": "Created Successfully"

})


gold_verification_report = pd.DataFrame(gold_verification)


print(gold_verification_report.to_string(index=False))


# ==========================================================
# STEP 21 - SAVE GOLD VERIFICATION REPORT
# ==========================================================

gold_verification_report.to_csv(

    gold_path / "gold_analytics_verification_report.csv",

    index=False

)


print("\nGold verification report saved successfully!")


# ==========================================================
# STEP 22 - FINAL SUMMARY
# ==========================================================

print("\n========== FINAL GOLD LAYER SUMMARY ==========")


print("Total Silver Datasets Used:", len(datasets))

print("Total Gold Analytical Datasets:", len(gold_datasets) + 1)

print("Gold Folder:", gold_path)

print("\n========== GOLD LAYER ANALYTICS COMPLETED ==========")

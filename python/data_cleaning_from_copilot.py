

# Apply shared cleanup and save every loaded dataset
cleaning_sources = {
    "Rainfall": rainfall_clean,
    "Flood": flood_clean,
    "Road Complaints": road_clean,
    "Traffic": traffic_clean,
    "Public Grievances": grievance,
    "Waterlogging": waterlogging,
    "Population": population,
    "Emergency Response": emergency,
}

cleaned_file_names = {
    "Rainfall": "rainfall_cleaned.csv",
    "Flood": "flood_cleaned.csv",
    "Road Complaints": "road_complaints_cleaned.csv",
    "Traffic": "traffic_cleaned.csv",
    "Public Grievances": "public_grievances_cleaned.csv",
    "Waterlogging": "waterlogging_cleaned.csv",
    "Population": "population_cleaned.csv",
    "Emergency Response": "emergency_response_cleaned.csv",
}

cleaned_datasets = {}

for name, df in cleaning_sources.items():
    cleaned_df = df.copy()

    # Remove leading/trailing whitespace from text columns.
    text_columns = cleaned_df.select_dtypes(include=["object", "string"]).columns
    for column in text_columns:
        cleaned_df[column] = cleaned_df[column].map(
            lambda value: value.strip() if isinstance(value, str) else value
        )

    # Standardize columns that represent dates or timestamps.
    for column in cleaned_df.columns:
        column_name = column.lower()
        is_date_column = (
            "date" in column_name
            or "timestamp" in column_name
            or column_name.endswith("_at")
        )
        if is_date_column and pd.api.types.is_string_dtype(cleaned_df[column]):
            cleaned_df[column] = pd.to_datetime(
                cleaned_df[column],
                errors="coerce",
            )

    cleaned_datasets[name] = cleaned_df
    output_file = silver_path / cleaned_file_names[name]
    cleaned_df.to_csv(output_file, index=False)
    print(f"{name} cleaned and saved to: {output_file}")

print(f"\nAll {len(cleaned_datasets)} datasets cleaned and saved successfully!")

# Chennai Urban Intelligence - Practice Dataset Pack

## Data authenticity
This is a **synthetic practice dataset pack** created for a data engineering portfolio project.
It is not an official Greater Chennai Corporation, IMD, police, transport, or emergency-services dataset.
Zone names are based on commonly used Chennai corporation zone names; all generated observations,
complaint IDs, incidents, coordinates, response times and counts are simulated. Do not describe
simulated values as actual government records.

## Files
- 00_zone_reference.csv: zone dimension (15 zones)
- 00_location_master.csv: location dimension (120 generated sample locations)
- 01_historical_rainfall.csv: daily rainfall by zone, 2020-01-01 to 2025-12-31
- 02_flood_affected_areas.csv: flood event records
- 03_road_damage_complaints.csv: road/pothole complaints (includes intentional duplicate rows)
- 04_traffic_congestion.json: traffic snapshots
- 05_public_grievances.xlsx: public grievances (includes intentional duplicate rows)
- 06_waterlogging_locations.csv: waterlogging site inventory
- 07_population_density_by_zone.xlsx: yearly zone-level population-density estimates
- 08_emergency_response_rescue.json: emergency and rescue response records
- 09_mock_api_response.json: simulated API payload for API-ingestion practice

## Suggested join keys
- zone-level: zone_id
- site-level: location_id
- time-series: date fields (convert to DATE/TIMESTAMP before joining)
- Rainfall to incident analysis: zone_id + calendar date (or aggregate rainfall to zone/day first)
- Flood and waterlogging: location_id and zone_id

## Intentional data quality challenges
- Rainfall has a small number of null values and a few deliberately abnormal 999 mm values.
- Road complaints contain 20 duplicate rows.
- Public grievances contain 25 duplicate rows.
- Mixed formats: CSV, JSON, and Excel.
- Zone names and location names should be standardized using the reference dimensions.
- Traffic records are snapshots, not official traffic sensor feeds.

## Suggested Bronze/Silver/Gold
Bronze: ingest source files unchanged with ingestion_timestamp, source_file, batch_id.
Silver: parse types, standardize names, deduplicate, validate ranges, handle nulls, enrich zone/location IDs.
Gold: zone_daily_rainfall, zone_monthly_complaints, location_waterlogging_risk,
      zone_emergency_response, flood_risk_score, traffic_rainfall_impact.

## Important analytical cautions
A synthetic correlation between rainfall and road damage is not evidence of real-world causation.
For defensible real-world analysis, replace synthetic source files with official/open datasets as they become available.

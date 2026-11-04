# Data Quality Rules – Chennai Urban Intelligence Project

## 1. Historical Rainfall
- Rainfall date should not be missing.
- Zone ID should be valid.
- Rainfall should not contain negative values.
- Rainfall values greater than 300 mm should be investigated.
- Missing rainfall values should be reported.

## 2. Flood Affected Areas
- Flood event ID should be unique.
- Flood date should be valid.
- Zone ID should be valid.
- Location should not be missing.

## 3. Road Damage Complaints
- Complaint ID should be unique.
- Complaint date should be valid.
- Complaint type should not be missing.
- Duplicate complaint records should be investigated.

## 4. Traffic Congestion
- Traffic record ID should be unique.
- Observation date and time should be valid.
- Traffic speed should not be negative.
- Zone ID should be valid.

## 5. Public Grievances
- Grievance ID should be unique.
- Grievance date should be valid.
- Grievance category should not be missing.
- Duplicate grievance records should be investigated.

## 6. Waterlogging Locations
- Location ID should be unique.
- Location name should not be missing.
- Zone ID should be valid.

## 7. Population Density
- Year should be valid.
- Population density should not be negative.
- Zone ID should be valid.

## 8. Emergency Response
- Response ID should be unique.
- Response date should be valid.
- Response time should not be negative.
- Zone ID should be valid.

## Important
These are initial project quality rules. Thresholds and required fields must be checked against the actual dataset columns and documented assumptions before validation.


-- 1. ROAD COMPLAINTS: REMOVE EXTRA SPACES

update fact_road_complaints
set status = trim(status);

update fact_road_complaints
set severity = trim(severity);

update fact_road_complaints
set damage_type = trim(damage_type);

update fact_road_complaints
set reported_channel = trim(reported_channel);

update fact_road_complaints
set probable_cause = trim(probable_cause);


-- 2. ROAD COMPLAINTS: STANDARDIZE CAPITALIZATION

update fact_road_complaints
set status = concat(
    upper(left(lower(trim(status)), 1)),
    substring(lower(trim(status)), 2)
);

update fact_road_complaints
set severity = concat(
    upper(left(lower(trim(severity)), 1)),
    substring(lower(trim(severity)), 2)
);


-- 3. FLOOD: REMOVE EXTRA SPACES

update fact_flood
set severity = trim(severity);

update fact_flood
set flood_type = trim(flood_type);

update fact_flood
set zone_name = trim(zone_name);

update fact_flood
set location_name = trim(location_name);


-- 4. FLOOD: STANDARDIZE CAPITALIZATION

update fact_flood
set severity = concat(
    upper(left(lower(trim(severity)), 1)),
    substring(lower(trim(severity)), 2)
);

update fact_flood
set flood_type = concat(
    upper(left(lower(trim(flood_type)), 1)),
    substring(lower(trim(flood_type)), 2)
);


-- 5. RAINFALL: STANDARDIZE UNIT

update fact_rainfall
set unit = lower(trim(unit));


-- 6. RAINFALL: STANDARDIZE ZONE NAMES

update fact_rainfall
set zone_name = trim(zone_name);


-- ==========================================
-- STEP 14.6: VERIFY STANDARDIZED VALUES
-- ==========================================

-- ROAD COMPLAINTS

select distinct status
from fact_road_complaints;

select distinct severity
from fact_road_complaints;

select distinct damage_type
from fact_road_complaints;

select distinct reported_channel
from fact_road_complaints;

select distinct probable_cause
from fact_road_complaints;


-- FLOOD

select distinct severity
from fact_flood;

select distinct flood_type
from fact_flood;

select distinct zone_name
from fact_flood;


-- RAINFALL

select distinct unit
from fact_rainfall;

select distinct zone_name
from fact_rainfall;



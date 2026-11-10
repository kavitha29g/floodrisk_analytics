# missing data check
select
    count(*) as total_records,
    sum(observation_date is null) as missing_dates,sum(zone_id is null) as missing_zone_id,sum(zone_name is null) as missing_zone_name,sum(rainfall_mm is null) as missing_rainfall,
    sum(unit is null) as missing_unit,sum(source is null) as missing_source,sum(rainfall_quality_flag is null) as missing_quality_flag
from fact_rainfall;

select
    count(*) as total_records,
    sum(flood_event_id is null) as missing_event_id,sum(event_date is null) as missing_event_date, sum(zone_id is null) as missing_zone_id,
    sum(zone_name is null) as missing_zone_name,
    sum(location_id is null) as missing_location_id,
    sum(location_name is null) as missing_location_name,
    sum(latitude is null) as missing_latitude,
    sum(longitude is null) as missing_longitude,
    sum(flood_type is null) as missing_flood_type,
    sum(severity is null) as missing_severity,
    sum(estimated_affected_people is null) as missing_affected_people,
    sum(event_rainfall_mm is null) as missing_event_rainfall,
    sum(source is null) as missing_source
from fact_flood;

select
    count(*) as total_records,
    sum(road_complaint_id is null) as missing_complaint_id,
    sum(complaint_date is null) as missing_date,
    sum(zone_id is null) as missing_zone_id,
    sum(zone_name is null) as missing_zone_name,
    sum(location_id is null) as missing_location_id,
    sum(location_name is null) as missing_location_name,
    sum(latitude is null) as missing_latitude,
    sum(longitude is null) as missing_longitude,
    sum(damage_type is null) as missing_damage_type,
    sum(severity is null) as missing_severity,
    sum(status is null) as missing_status
from fact_road_complaints;

select
    count(*) as total_records,
    sum(traffic_record_id is null) as missing_traffic_id,
    sum(recorded_at is null) as missing_recorded_at,
    sum(zone_id is null) as missing_zone_id,
    sum(zone_name is null) as missing_zone_name,
    sum(location_id is null) as missing_location_id,
    sum(location_name is null) as missing_location_name,
    sum(latitude is null) as missing_latitude,
    sum(longitude is null) as missing_longitude,
    sum(avg_speed_kmph is null) as missing_avg_speed,
    sum(free_flow_speed_kmph is null) as missing_free_flow_speed
from fact_traffic;


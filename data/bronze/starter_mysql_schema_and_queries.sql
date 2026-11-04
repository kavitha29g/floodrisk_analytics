-- MySQL starter tables (adapt data types as needed)
create database if not exists chennai_smart_city;
use chennai_smart_city;

create table dim_zone (
  zone_id int primary key,
  zone_name varchar(100),
  zone_latitude decimal(9,6),
  zone_longitude decimal(9,6),
  population_density_per_sq_km_2021 int
);

-- Recommended additional tables:
-- dim_location(location_id, zone_id, zone_name, location_name, latitude, longitude)
-- fact_rainfall(observation_date, zone_id, rainfall_mm, unit, source)
-- fact_flood_event(flood_event_id, event_date, zone_id, location_id, severity, estimated_affected_people)
-- fact_road_complaint(road_complaint_id, complaint_date, zone_id, location_id, damage_type, severity, status)
-- fact_traffic(traffic_record_id, recorded_at, zone_id, location_id, avg_speed_kmph, free_flow_speed_kmph, vehicle_count)
-- fact_grievance(grievance_id, complaint_date, zone_id, location_id, complaint_category, priority, status)
-- dim_waterlogging_site(waterlogging_id, zone_id, location_id, historical_risk_level, waterlogging_reports_2020_2025)
-- fact_population(year, zone_id, population_density_per_sq_km)
-- fact_emergency(response_id, incident_date, zone_id, location_id, incident_type, severity, response_time_minutes)

-- Example: zone with highest total rainfall (after loading)
-- select z.zone_name, sum(r.rainfall_mm) total_rainfall_mm
-- from fact_rainfall r join dim_zone z on r.zone_id=z.zone_id
-- where r.rainfall_mm is not null
-- group by z.zone_name order by total_rainfall_mm desc;

-- Example: average emergency response time by zone
-- select zone_name, avg(response_time_minutes) avg_response_minutes
-- from fact_emergency group by zone_name order by avg_response_minutes desc;

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

select
    count(*) as total_records,
    sum(grievance_id is null) as missing_grievance_id,
    sum(complaint_date is null) as missing_complaint_date,
    sum(zone_id is null) as missing_zone_id,
    sum(zone_name is null) as missing_zone_name,
    sum(location_id is null) as missing_location_id,
    sum(location_name is null) as missing_location_name
from fact_public_grievances;

select
    count(*) as total_records,
    sum(waterlogging_id is null) as missing_waterlogging_id,
    sum(zone_id is null) as missing_zone_id,
    sum(zone_name is null) as missing_zone_name,
    sum(location_id is null) as missing_location_id,
    sum(location_name is null) as missing_location_name,
    sum(latitude is null) as missing_latitude,
    sum(longitude is null) as missing_longitude,
    sum(site_type is null) as missing_site_type,
    sum(historical_risk_level is null) as missing_risk_level
from fact_waterlogging_locations;

select
    count(*) as total_records,
    sum(zone_id is null) as missing_zone_id,
    sum(zone_name is null) as missing_zone_name,
    sum(population_density_per_sq_km is null) as missing_population_density
from fact_population;

select
    count(*) as total_records,
    sum(response_id is null) as missing_response_id,
    sum(zone_id is null) as missing_zone_id,
    sum(zone_name is null) as missing_zone_name,
    sum(response_time_minutes is null) as missing_response_time
from fact_emergency_response;

# duplication check 
select
    'rainfall' as dataset,
    count(*) - count(distinct observation_date, zone_id) as duplicate_records
from fact_rainfall

union all

select
    'flood',
    count(*) - count(distinct flood_event_id)
from fact_flood

union all

select
    'road complaints',
    count(*) - count(distinct road_complaint_id)
from fact_road_complaints

union all

select
    'traffic',
    count(*) - count(distinct traffic_record_id)
from fact_traffic

union all

select
    'public grievances',
    count(*) - count(distinct grievance_id)
from fact_public_grievances

union all

select
    'waterlogging',
    count(*) - count(distinct waterlogging_id)
from fact_waterlogging_locations

union all

select
    'population',
    count(*) - count(distinct zone_id)
from fact_population

union all

select
    'emergency response',
    count(*) - count(distinct response_id)
from fact_emergency_response;

# abnormal value check

select
    count(*) as total_records,
    min(rainfall_mm) as minimum_rainfall,
    max(rainfall_mm) as maximum_rainfall,
    sum(case
        when rainfall_mm < 0 then 1
        else 0
    end) as negative_rainfall,
    sum(case
        when rainfall_mm = 999 then 1
        else 0
    end) as invalid_placeholder
from fact_rainfall;

select
    count(*) as total_records,
    min(estimated_affected_people) as minimum_affected,
    max(estimated_affected_people) as maximum_affected,
    sum(case
        when estimated_affected_people < 0 then 1
        else 0
    end) as negative_affected_people
from fact_flood;

select
    count(*) as total_records,
    sum(case
        when latitude < 8 or latitude > 14 then 1
        else 0
    end) as invalid_latitude,
    sum(case
        when longitude < 76 or longitude > 82 then 1
        else 0
    end) as invalid_longitude
from fact_road_complaints;

select
    count(*) as total_records,
    min(vehicle_count) as minimum_vehicles,
    max(vehicle_count) as maximum_vehicles,
    sum(case when vehicle_count < 0 then 1 else 0 end) as negative_vehicles
from fact_traffic;



select
    count(*) as total_records,
    sum(case when grievance_id is null then 1 else 0 end) as missing_grievance_id
from fact_public_grievances;

select
    count(*) as total_records,
    sum(case when latitude < 8 or latitude > 14 then 1 else 0 end) as invalid_latitude,
    sum(case when longitude < 76 or longitude > 82 then 1 else 0 end) as invalid_longitude
from fact_waterlogging_locations;
select
    count(*) as total_records,
    min(population_density_per_sq_km) as minimum_population,
    max(population_density_per_sq_km) as maximum_population,
    sum(case when population_density_per_sq_km < 0 then 1 else 0 end) as negative_population
from fact_population;

select * from fact_population limit 2;

select
    count(*) as total_records,
    min(response_time_minutes) as minimum_response_time,
    max(response_time_minutes) as maximum_response_time,
    sum(case when response_time_minutes < 0 then 1 else 0 end) as negative_response_time
from fact_emergency_response;

# Data Quality Rules Validation

select
    count(*) as total_records,

    sum(case
        when zone_id is null then 1
        else 0
    end) as missing_zone_id,

    sum(case
        when unit <> 'mm' then 1
        else 0
    end) as invalid_unit,

    sum(case
        when rainfall_mm < 0 then 1
        else 0
    end) as invalid_rainfall

from fact_rainfall;

select
    count(*) as total_records,

    sum(case
        when severity not in ('Low', 'Moderate', 'High', 'Severe')
        or severity is null then 1
        else 0
    end) as invalid_severity,

    sum(case
        when flood_type not in (
            'Residential flooding',
            'Canal overflow',
            'Street flooding',
            'Subway flooding'
        )
        or flood_type is null then 1
        else 0
    end) as invalid_flood_type

from fact_flood;

select
    count(*) as total_records,

    sum(case
        when status not in (
            'Open',
            'Assigned',
            'In Progress',
            'Resolved'
        ) or status is null then 1
        else 0
    end) as invalid_status,

    sum(case
        when severity not in (
            'Low',
            'Medium',
            'High',
            'Critical'
        ) or severity is null then 1
        else 0
    end) as invalid_severity

from fact_road_complaints;

select distinct zone_id
from fact_rainfall
where zone_id not between 1 and 15
   or zone_id is null;

   # Final Data Quality Validation Report
   use chennai_smart_city;

select 'Rainfall' as dataset, count(*) as total_records
from fact_rainfall

union all

select 'Flood', count(*)
from fact_flood

union all

select 'Road Complaints', count(*)
from fact_road_complaints

union all

select 'Traffic', count(*)
from fact_traffic

union all

select 'Public Grievances', count(*)
from fact_public_grievances

union all

select 'Waterlogging', count(*)
from fact_waterlogging_locations

union all

select 'Population', count(*)
from fact_population

union all

select 'Emergency Response', count(*)
from fact_emergency_response;

select
    table_name,
    column_name,
    data_type,
    is_nullable,
    column_key
from information_schema.columns
where table_schema = 'chennai_urban_intelligence'
and table_name in (
    'fact_rainfall',
    'fact_flood',
    'fact_road_complaints',
    'fact_traffic',
    'fact_public_grievances',
    'fact_waterlogging_locations',
    'fact_population',
    'fact_emergency_response')
order by table_name, ordinal_position;

drop table data_quality_validation_report;
create table data_quality_validation_report (
    dataset_name varchar(100),
    total_records int,
    missing_values int,
    duplicate_records int,
    abnormal_values int,
    business_rule_errors int,
    validation_status varchar(30)
);

insert into data_quality_validation_report
(dataset_name, total_records)
select 'Rainfall', count(*) from fact_rainfall

union all
select 'Flood', count(*) from fact_flood

union all
select 'Road Complaints', count(*) from fact_road_complaints

union all
select 'Traffic', count(*) from fact_traffic

union all
select 'Public Grievances', count(*) from fact_public_grievances

union all
select 'Waterlogging', count(*) from fact_waterlogging_locations

union all
select 'Population', count(*) from fact_population

union all
select 'Emergency Response', count(*) from fact_emergency_response;

update data_quality_validation_report
set
    missing_values = 109,
    duplicate_records = 0,
    abnormal_values = 0,
    business_rule_errors = 0,
    validation_status = 'Validated'
where dataset_name = 'Rainfall';

select * from data_quality_validation_report;
update data_quality_validation_report
set missing_values = 109
where dataset_name = 'Rainfall';

update data_quality_validation_report
set missing_values = 0
where dataset_name = 'Flood';

update data_quality_validation_report
set missing_values = 0
where dataset_name = 'Road Complaints';

update data_quality_validation_report
set missing_values = 0
where dataset_name = 'Traffic';

update data_quality_validation_report
set missing_values = 0
where dataset_name = 'Public Grievances';

update data_quality_validation_report
set missing_values = 0
where dataset_name = 'Waterlogging';

update data_quality_validation_report
set missing_values = 0
where dataset_name = 'Population';

update data_quality_validation_report
set missing_values = 0
where dataset_name = 'Emergency Response';

update data_quality_validation_report
set duplicate_records = 0
where dataset_name = 'Rainfall';

update data_quality_validation_report
set duplicate_records = 0
where dataset_name = 'Flood';

update data_quality_validation_report
set duplicate_records = 0
where dataset_name = 'Road Complaints';

update data_quality_validation_report
set duplicate_records = 0
where dataset_name = 'Traffic';

update data_quality_validation_report
set duplicate_records = 0
where dataset_name = 'Public Grievances';

update data_quality_validation_report
set duplicate_records = 0
where dataset_name = 'Waterlogging';

update data_quality_validation_report
set duplicate_records = 0
where dataset_name = 'Population';

update data_quality_validation_report
set duplicate_records = 0
where dataset_name = 'Emergency Response';

update data_quality_validation_report
set abnormal_values = 0
where dataset_name = 'Rainfall';

update data_quality_validation_report
set abnormal_values = 0
where dataset_name = 'Flood';

update data_quality_validation_report
set abnormal_values = 0
where dataset_name = 'Road Complaints';

update data_quality_validation_report
set abnormal_values = 0
where dataset_name = 'Traffic';

update data_quality_validation_report
set abnormal_values = 0
where dataset_name = 'Public Grievances';

update data_quality_validation_report
set abnormal_values = 0
where dataset_name = 'Waterlogging';

update data_quality_validation_report
set abnormal_values = 0
where dataset_name = 'Population';

update data_quality_validation_report
set abnormal_values = 0
where dataset_name = 'Emergency Response';

update data_quality_validation_report
set business_rule_errors = 0
where dataset_name = 'Rainfall';

update data_quality_validation_report
set business_rule_errors = 0
where dataset_name = 'Flood';

update data_quality_validation_report
set business_rule_errors = 0
where dataset_name = 'Road Complaints';

update data_quality_validation_report
set business_rule_errors = 0
where dataset_name = 'Traffic';

update data_quality_validation_report
set business_rule_errors = 0
where dataset_name = 'Public Grievances';

update data_quality_validation_report
set business_rule_errors = 0
where dataset_name = 'Waterlogging';

update data_quality_validation_report
set business_rule_errors = 0
where dataset_name = 'Population';

update data_quality_validation_report
set business_rule_errors = 0
where dataset_name = 'Emergency Response';

select * from data_quality_validation_report;
update data_quality_validation_report
set validation_status =
case
    when missing_values = 0
     and duplicate_records = 0
     and abnormal_values = 0
     and business_rule_errors = 0
    then 'Passed'
    else 'Review Required'
end;
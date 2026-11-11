

select
    table_name,
    column_name,
    column_key
from information_schema.columns
where table_schema = 'chennai_urban_intelligence'
and table_name like 'dim_%'
and column_key = 'PRI'
order by table_name;
-- duplicate check for primary keys in dimension tables
select zone_id, count(*) as record_count
from dim_zone
group by zone_id
having count(*) > 1;

select location_id, count(*) as record_count
from dim_location
group by location_id
having count(*) > 1;

select incident_type, count(*) as record_count
from dim_incident_type
group by incident_type
having count(*) > 1;


select 'dim_date' as dimension, count(*) as duplicate_keys
from (
    select full_date
    from dim_date
    group by full_date
    having count(*) > 1
) as x

union all

select 'dim_flood_type', count(*)
from (
    select flood_type
    from dim_flood_type
    group by flood_type
    having count(*) > 1
) as x

union all

select 'dim_severity', count(*)
from (
    select severity
    from dim_severity
    group by severity
    having count(*) > 1
) as x

union all

select 'dim_complaint_category', count(*)
from (
    select complaint_category
    from dim_complaint_category
    group by complaint_category
    having count(*) > 1
) as x

union all

select 'dim_priority', count(*)
from (
    select priority
    from dim_priority
    group by priority
    having count(*) > 1
) as x

union all

select 'dim_grievance_status', count(*)
from (
    select status
    from dim_grievance_status
    group by status
    having count(*) > 1
) as x

union all

select 'dim_road_damage', count(*)
from (
    select damage_type
    from dim_road_damage
    group by damage_type
    having count(*) > 1
) as x

union all

select 'dim_congestion', count(*)
from (
    select congestion_level
    from dim_congestion
    group by congestion_level
    having count(*) > 1
) as x

union all

select 'dim_site_type', count(*)
from (
    select site_type
    from dim_site_type
    group by site_type
    having count(*) > 1
) as x

union all

select 'dim_risk_level', count(*)
from (
    select historical_risk_level
    from dim_risk_level
    group by historical_risk_level
    having count(*) > 1
) as x

union all

select 'dim_likely_cause', count(*)
from (
    select likely_cause
    from dim_likely_cause
    group by likely_cause
    having count(*) > 1
) as x

union all

select 'dim_response_outcome', count(*)
from (
    select outcome
    from dim_response_outcome
    group by outcome
    having count(*) > 1
) as x;


alter table fact_rainfall
add constraint fk_fact_rainfall_zone
foreign key (zone_id)
references dim_zone(zone_id);

select
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
from information_schema.key_column_usage
where table_schema = 'chennai_urban_intelligence'
and table_name = 'fact_rainfall'
and referenced_table_name is not null;


alter table fact_rainfall
add constraint fk_fact_rainfall_date
foreign key (observation_date)
references dim_date(full_date);

select
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
from information_schema.key_column_usage
where table_schema = 'chennai_urban_intelligence'
and table_name = 'fact_rainfall'
and referenced_table_name is not null;

alter table fact_flood
add constraint fk_fact_flood_zone
foreign key (zone_id)
references dim_zone(zone_id);



alter table fact_flood
add constraint fk_fact_flood_date
foreign key (event_date)
references dim_date(full_date);

alter table fact_flood
add constraint fk_fact_flood_location
foreign key (location_id)
references dim_location(location_id);

alter table fact_flood
add constraint fk_fact_flood_severity
foreign key (severity)
references dim_severity(severity);

alter table fact_flood
add constraint fk_fact_flood_type
foreign key (flood_type)
references dim_flood_type(flood_type);

select
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
from information_schema.key_column_usage
where table_schema = 'chennai_urban_intelligence'
and table_name = 'fact_flood'
and referenced_table_name is not null;

alter table fact_population
add constraint fk_fact_population_zone
foreign key (zone_id)
references dim_zone(zone_id);

select
    constraint_name,
    table_name,
    column_name,
    referenced_table_name,
    referenced_column_name
from information_schema.key_column_usage
where table_schema = 'chennai_urban_intelligence'
and table_name = 'fact_population'
and referenced_table_name is not null;

alter table fact_public_grievances
add constraint fk_grievance_category
foreign key (complaint_category)
references dim_complaint_category(complaint_category);



alter table fact_public_grievances
add constraint fk_grievance_priority
foreign key (priority)
references dim_priority(priority);

alter table fact_public_grievances
add constraint fk_grievance_status
foreign key (status)
references dim_grievance_status(status);

alter table fact_public_grievances
add constraint fk_grievance_zone
foreign key (zone_id)
references dim_zone(zone_id);

alter table fact_public_grievances
add constraint fk_grievance_location
foreign key (location_id)
references dim_location(location_id);

alter table fact_public_grievances
add constraint fk_grievance_date
foreign key (complaint_date)
references dim_date(full_date);

#--

alter table fact_road_complaints
add constraint fk_road_damage
foreign key (damage_type)
references dim_road_damage(damage_type);

alter table fact_road_complaints
add constraint fk_road_severity
foreign key (severity)
references dim_severity(severity);

alter table fact_road_complaints
add constraint fk_road_zone
foreign key (zone_id)
references dim_zone(zone_id);

alter table fact_road_complaints
add constraint fk_road_location
foreign key (location_id)
references dim_location(location_id);

alter table fact_road_complaints
add constraint fk_road_date
foreign key (complaint_date)
references dim_date(full_date);

#--


alter table fact_traffic
add constraint fk_traffic_congestion
foreign key (congestion_level)
references dim_congestion(congestion_level);

alter table fact_traffic
add constraint fk_traffic_zone
foreign key (zone_id)
references dim_zone(zone_id);

alter table fact_traffic
add constraint fk_traffic_location
foreign key (location_id)
references dim_location(location_id);

#--

alter table fact_waterlogging_locations
add constraint fk_waterlogging_site
foreign key (site_type)
references dim_site_type(site_type);

alter table fact_waterlogging_locations
add constraint fk_waterlogging_risk
foreign key (historical_risk_level)
references dim_risk_level(historical_risk_level);

alter table fact_waterlogging_locations
add constraint fk_waterlogging_cause
foreign key (likely_cause)
references dim_likely_cause(likely_cause);

alter table fact_waterlogging_locations
add constraint fk_waterlogging_zone
foreign key (zone_id)
references dim_zone(zone_id);

alter table fact_waterlogging_locations
add constraint fk_waterlogging_location
foreign key (location_id)
references dim_location(location_id);

#--

alter table fact_emergency_response
add constraint fk_emergency_incident
foreign key (incident_type)
references dim_incident_type(incident_type);

alter table fact_emergency_response
add constraint fk_emergency_severity
foreign key (severity)
references dim_severity(severity);

alter table fact_emergency_response
add constraint fk_emergency_outcome
foreign key (outcome)
references dim_response_outcome(outcome);

alter table fact_emergency_response
add constraint fk_emergency_zone
foreign key (zone_id)
references dim_zone(zone_id);

alter table fact_emergency_response
add constraint fk_emergency_location
foreign key (location_id)
references dim_location(location_id);

alter table fact_emergency_response
add constraint fk_emergency_date
foreign key (incident_date)
references dim_date(full_date);

select
    table_name,
    constraint_name,
    column_name,
    referenced_table_name,
    referenced_column_name
from information_schema.key_column_usage
where table_schema = 'chennai_urban_intelligence'
and referenced_table_name is not null
order by table_name, constraint_name;





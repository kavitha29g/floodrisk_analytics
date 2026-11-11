

select
    table_name,
    column_name,
    data_type,
    column_key
from information_schema.columns
where table_schema = 'chennai_urban_intelligence'
and table_name like 'fact_%'
order by table_name, ordinal_position;

select
    table_name,
    column_name,
    data_type,
    column_key
from information_schema.columns
where table_schema = 'chennai_urban_intelligence'
and table_name like 'dim_%'
order by table_name, ordinal_position;







select
    'rainfall - zone' as relationship,
    count(*) as total_records,
    sum(f.zone_id is null) as null_values,
    sum(f.zone_id is not null and d.zone_id is null) as unmatched_records
from fact_rainfall f
left join dim_zone d
on f.zone_id = d.zone_id;

select
    'rainfall - date' as relationship,
    count(*) as total_records,
    sum(f.observation_date is null) as null_values,
    sum(f.observation_date is not null
        and d.full_date is null) as unmatched_records
from fact_rainfall f
left join dim_date d
on f.observation_date = d.full_date;

select
    'flood - zone' as relationship,
    count(*) as total_records,
    sum(f.zone_id is null) as null_values,
    sum(f.zone_id is not null
        and d.zone_id is null) as unmatched_records
from fact_flood f
left join dim_zone d
on f.zone_id = d.zone_id;

select
    'flood - date' as relationship,
    count(*) as total_records,
    sum(f.event_date is null) as null_values,
    sum(f.event_date is not null
        and d.full_date is null) as unmatched_records
from fact_flood f
left join dim_date d
on f.event_date = d.full_date;

select
    'flood - severity' as relationship,
    count(*) as total_records,
    sum(f.severity is null) as null_values,
    sum(f.severity is not null
        and d.severity is null) as unmatched_records
from fact_flood f
left join dim_severity d
on f.severity = d.severity;

select
    'flood - type' as relationship,
    count(*) as total_records,
    sum(f.flood_type is null) as null_values,
    sum(f.flood_type is not null
        and d.flood_type is null) as unmatched_records
from fact_flood f
left join dim_flood_type d
on f.flood_type = d.flood_type;

select
    'flood - location' as relationship,
    count(*) as total_records,
    sum(f.location_id is null) as null_values,
    sum(f.location_id is not null
        and d.location_id is null) as unmatched_records
from fact_flood f
left join dim_location d
on f.location_id = d.location_id;

select
    'population - zone' as relationship,
    count(*) as total_records,
    sum(f.zone_id is null) as null_values,
    sum(f.zone_id is not null
        and d.zone_id is null) as unmatched_records
from fact_population f
left join dim_zone d
on f.zone_id = d.zone_id;


select
    'grievance - category' as relationship,
    count(*) as total_records,
    sum(f.complaint_category is null) as null_values,
    sum(f.complaint_category is not null
        and d.complaint_category is null) as unmatched_records
from fact_public_grievances f
left join dim_complaint_category d
on f.complaint_category = d.complaint_category;

select
    'grievance - priority' as relationship,
    count(*) as total_records,
    sum(f.priority is null) as null_values,
    sum(f.priority is not null
        and d.priority is null) as unmatched_records
from fact_public_grievances f
left join dim_priority d
on f.priority = d.priority;

select
    'grievance - status' as relationship,
    count(*) as total_records,
    sum(f.status is null) as null_values,
    sum(f.status is not null
        and d.status is null) as unmatched_records
from fact_public_grievances f
left join dim_grievance_status d
on f.status = d.status;

select
    'grievance - zone' as relationship,
    count(*) as total_records,
    sum(f.zone_id is null) as null_values,
    sum(f.zone_id is not null
        and d.zone_id is null) as unmatched_records
from fact_public_grievances f
left join dim_zone d
on f.zone_id = d.zone_id;

select
    'grievance - location' as relationship,
    count(*) as total_records,
    sum(f.location_id is null) as null_values,
    sum(f.location_id is not null
        and d.location_id is null) as unmatched_records
from fact_public_grievances f
left join dim_location d
on f.location_id = d.location_id;

select
    'grievance - date' as relationship,
    count(*) as total_records,
    sum(f.complaint_date is null) as null_values,
    sum(f.complaint_date is not null
        and d.full_date is null) as unmatched_records
from fact_public_grievances f
left join dim_date d
on f.complaint_date = d.full_date;

select
    'road - damage type' as relationship,
    count(*) as total_records,
    sum(f.damage_type is null) as null_values,
    sum(f.damage_type is not null
        and d.damage_type is null) as unmatched_records
from fact_road_complaints f
left join dim_road_damage d
on f.damage_type = d.damage_type;

select
    'road - severity' as relationship,
    count(*) as total_records,
    sum(f.severity is null) as null_values,
    sum(f.severity is not null
        and d.severity is null) as unmatched_records
from fact_road_complaints f
left join dim_severity d
on f.severity = d.severity;

select
    'road - zone' as relationship,
    count(*) as total_records,
    sum(f.zone_id is null) as null_values,
    sum(f.zone_id is not null
        and d.zone_id is null) as unmatched_records
from fact_road_complaints f
left join dim_zone d
on f.zone_id = d.zone_id;

select
    'road - location' as relationship,
    count(*) as total_records,
    sum(f.location_id is null) as null_values,
    sum(f.location_id is not null
        and d.location_id is null) as unmatched_records
from fact_road_complaints f
left join dim_location d
on f.location_id = d.location_id;

select
    'road - date' as relationship,
    count(*) as total_records,
    sum(f.complaint_date is null) as null_values,
    sum(f.complaint_date is not null
        and d.full_date is null) as unmatched_records
from fact_road_complaints f
left join dim_date d
on f.complaint_date = d.full_date;

select
    'traffic - congestion' as relationship,
    count(*) as total_records,
    sum(f.congestion_level is null) as null_values,
    sum(f.congestion_level is not null
        and d.congestion_level is null) as unmatched_records
from fact_traffic f
left join dim_congestion d
on f.congestion_level = d.congestion_level;

select
    'traffic - zone' as relationship,
    count(*) as total_records,
    sum(f.zone_id is null) as null_values,
    sum(f.zone_id is not null
        and d.zone_id is null) as unmatched_records
from fact_traffic f
left join dim_zone d
on f.zone_id = d.zone_id;

select
    'traffic - location' as relationship,
    count(*) as total_records,
    sum(f.location_id is null) as null_values,
    sum(f.location_id is not null
        and d.location_id is null) as unmatched_records
from fact_traffic f
left join dim_location d
on f.location_id = d.location_id;

select
    'traffic - date' as relationship,
    count(*) as total_records,
    sum(f.recorded_at is null) as null_values,
    sum(f.recorded_at is not null
        and d.full_date is null) as unmatched_records
from fact_traffic f
left join dim_date d
on date(f.recorded_at) = d.full_date;

select
    'waterlogging - site type' as relationship,
    count(*) as total_records,
    sum(f.site_type is null) as null_values,
    sum(f.site_type is not null
        and d.site_type is null) as unmatched_records
from fact_waterlogging_locations f
left join dim_site_type d
on f.site_type = d.site_type;

select
    'waterlogging - risk level' as relationship,
    count(*) as total_records,
    sum(f.historical_risk_level is null) as null_values,
    sum(f.historical_risk_level is not null
        and d.historical_risk_level is null) as unmatched_records
from fact_waterlogging_locations f
left join dim_risk_level d
on f.historical_risk_level = d.historical_risk_level;

select
    'waterlogging - likely cause' as relationship,
    count(*) as total_records,
    sum(f.likely_cause is null) as null_values,
    sum(f.likely_cause is not null
        and d.likely_cause is null) as unmatched_records
from fact_waterlogging_locations f
left join dim_likely_cause d
on f.likely_cause = d.likely_cause;

select
    'waterlogging - zone' as relationship,
    count(*) as total_records,
    sum(f.zone_id is null) as null_values,
    sum(f.zone_id is not null
        and d.zone_id is null) as unmatched_records
from fact_waterlogging_locations f
left join dim_zone d
on f.zone_id = d.zone_id;

select
    'waterlogging - location' as relationship,
    count(*) as total_records,
    sum(f.location_id is null) as null_values,
    sum(f.location_id is not null
        and d.location_id is null) as unmatched_records
from fact_waterlogging_locations f
left join dim_location d
on f.location_id = d.location_id;

select
    'emergency - zone' as relationship,
    count(*) as total_records,
    sum(f.zone_id is null) as null_values,
    sum(f.zone_id is not null
        and d.zone_id is null) as unmatched_records
from fact_emergency_response f
left join dim_zone d
on f.zone_id = d.zone_id;

select
    'emergency - location' as relationship,
    count(*) as total_records,
    sum(f.location_id is null) as null_values,
    sum(f.location_id is not null
        and d.location_id is null) as unmatched_records
from fact_emergency_response f
left join dim_location d
on f.location_id = d.location_id;



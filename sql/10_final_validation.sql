

select
    table_name,
    table_type
from information_schema.tables
where table_schema = 'chennai_urban_intelligence'
order by table_type, table_name;

-- primary key
select
    table_name,
    column_name,
    constraint_name
from information_schema.key_column_usage
where table_schema = 'chennai_urban_intelligence'
and constraint_name = 'primary'
order by table_name, ordinal_position;
-- Validate foreign keys
select
    table_name as fact_table,
    constraint_name as foreign_key_name,
    column_name as fact_column,
    referenced_table_name as dimension_table,
    referenced_column_name as dimension_column
from information_schema.key_column_usage
where table_schema = 'chennai_urban_intelligence'
and referenced_table_name is not null
order by table_name, constraint_name;

select
    table_name,
    column_name,
    is_nullable,
    column_key
from information_schema.columns
where table_schema = 'chennai_urban_intelligence'
and column_key = 'pri'
order by table_name;

select zone_id, count(*) as duplicate_count
from dim_zone
group by zone_id
having count(*) > 1;

select location_id, count(*) as duplicate_count
from dim_location
group by location_id
having count(*) > 1;


select date_key, count(*) as duplicate_count
from dim_date
group by date_key
having count(*) > 1;

select 'fact_emergency_response' as table_name, count(*) as total_records from fact_emergency_response
union all
select 'fact_flood', count(*) from fact_flood
union all
select 'fact_population', count(*) from fact_population
union all
select 'fact_public_grievances', count(*) from fact_public_grievances
union all
select 'fact_rainfall', count(*) from fact_rainfall
union all
select 'fact_road_complaints', count(*) from fact_road_complaints
union all
select 'fact_traffic', count(*) from fact_traffic
union all
select 'fact_waterlogging_locations', count(*) from fact_waterlogging_locations;
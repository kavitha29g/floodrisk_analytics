select
    table_name,
    column_name,
    column_type
from information_schema.columns
where table_schema = 'chennai_urban_intelligence'
and table_name in (
    'fact_rainfall',
    'fact_flood',
    'fact_road_complaints',
    'fact_traffic',
    'fact_public_grievances',
    'fact_waterlogging',
    'fact_population',
    'fact_emergency_response'
)
order by table_name, ordinal_position;

select
    zone_id,
    zone_name,
    count(*) as total_records
from fact_population
group by zone_id, zone_name
order by zone_id;

create table dim_zone (
    zone_id int not null,
    zone_name varchar(100) not null,
    primary key (zone_id)
);

insert into dim_zone (zone_id, zone_name)
select distinct
    zone_id,
    zone_name
from fact_population;
select *
from dim_zone
order by zone_id;
select count(*) as total_zones
from dim_zone;

select
    zone_id,
    count(*) as total_records
from dim_zone
group by zone_id
having count(*) > 1;


create table dim_date (
    date_key int not null,
    full_date date not null,
    year int,
    quarter int,
    month int,
    month_name varchar(20),
    day int,
    day_name varchar(20),
    weekend_flag varchar(10),
    primary key (date_key),
    unique key (full_date)
);

insert into dim_date
select
    date_format(d, '%Y%m%d') + 0,
    d,
    year(d),
    quarter(d),
    month(d),
    monthname(d),
    day(d),
    dayname(d),
    case
        when dayofweek(d) in (1, 7) then 'Weekend'
        else 'Weekday'
    end
from (
    with recursive dates as (
        select cast('2020-01-01' as date) as d
        union all
        select date_add(d, interval 1 day)
        from dates
        where d < '2025-12-31'
    )
    select d from dates
) as calendar;

select* from dim_date;


create table dim_location (
    location_id varchar(100) not null,
    location_name varchar(200),
    latitude double,
    longitude double,
    primary key (location_id)
);

insert into dim_location
    (location_id, location_name, latitude, longitude)
select
    location_id,
    max(location_name),
    max(latitude),
    max(longitude)
from (
    select location_id, location_name, latitude, longitude
    from fact_flood

    union all

    select location_id, location_name, latitude, longitude
    from fact_road_complaints

    union all

    select location_id, location_name, latitude, longitude
    from fact_waterlogging_locations
) as locations
where location_id is not null
group by location_id;

select * from dim_location;


create table dim_flood_type (
    flood_type varchar(100) not null,
    primary key (flood_type)
);

insert into dim_flood_type
select distinct trim(flood_type)
from fact_flood
where flood_type is not null
and trim(flood_type) <> '';
select * from dim_flood_type;

create table dim_road_damage (
    damage_type varchar(100) not null,
    primary key (damage_type)
);

insert into dim_road_damage
select distinct trim(damage_type)
from fact_road_complaints
where damage_type is not null
and trim(damage_type) <> '';

select * from dim_road_damage;


create table dim_severity (
    severity varchar(50) primary key
);

insert into dim_severity
select distinct trim(severity)
from (
    select severity from fact_flood

    union

    select severity from fact_road_complaints
) as severity_data
where severity is not null
and trim(severity) <> '';

select * from dim_severity;



select 'dim_zone' as table_name, count(*) as total_records
from dim_zone

union all

select 'dim_date', count(*)
from dim_date

union all

select 'dim_flood_type', count(*)
from dim_flood_type

union all

select 'dim_road_damage', count(*)
from dim_road_damage

union all

select 'dim_severity', count(*)
from dim_severity

union all

select 'dim_location', count(*)
from dim_location;




-- increase recursion limit
set session cte_max_recursion_depth = 10000;

describe fact_traffic;

describe fact_public_grievances;

describe fact_emergency_response;

describe fact_waterlogging_locations;


-- create traffic congestion dimension
create table dim_congestion (
    congestion_level varchar(30) primary key
);

-- insert unique congestion levels
insert into dim_congestion
select distinct trim(congestion_level)
from fact_traffic
where congestion_level is not null
and trim(congestion_level) <> '';

-- validate
select * from dim_congestion;


create table dim_complaint_category (
    complaint_category varchar(100) primary key
);

insert into dim_complaint_category
select distinct trim(complaint_category)
from fact_public_grievances
where complaint_category is not null
and trim(complaint_category) <> '';

select * from dim_complaint_category;



create table dim_priority (
    priority varchar(30) primary key
);

insert into dim_priority
select distinct trim(priority)
from fact_public_grievances
where priority is not null
and trim(priority) <> '';

select * from dim_priority;



create table dim_grievance_status (
    status varchar(50) primary key
);

insert into dim_grievance_status
select distinct trim(status)
from fact_public_grievances
where status is not null
and trim(status) <> '';

select * from dim_grievance_status;



select 'dim_congestion' as table_name,
       count(*) as total_records
from dim_congestion

union all

select 'dim_complaint_category',
       count(*)
from dim_complaint_category

union all

select 'dim_priority',
       count(*)
from dim_priority

union all

select 'dim_grievance_status',
       count(*)
from dim_grievance_status;

create table dim_incident_type (
    incident_type varchar(100) primary key
);

insert into dim_incident_type
select distinct trim(incident_type)
from fact_emergency_response
where incident_type is not null
and trim(incident_type) <> '';

select * from dim_incident_type;

create table dim_response_outcome (
    outcome varchar(100) primary key
);

insert into dim_response_outcome
select distinct trim(outcome)
from fact_emergency_response
where outcome is not null
and trim(outcome) <> '';

select * from dim_response_outcome;


create table dim_site_type (
    site_type varchar(100) primary key
);

insert into dim_site_type
select distinct trim(site_type)
from fact_waterlogging_locations
where site_type is not null
and trim(site_type) <> '';

select * from dim_site_type;


create table dim_risk_level (
    historical_risk_level varchar(30) primary key
);

insert into dim_risk_level
select distinct trim(historical_risk_level)
from fact_waterlogging_locations
where historical_risk_level is not null
and trim(historical_risk_level) <> '';

select * from dim_risk_level;

create table dim_likely_cause (
    likely_cause varchar(150) primary key
);

insert into dim_likely_cause
select distinct trim(likely_cause)
from fact_waterlogging_locations
where likely_cause is not null
and trim(likely_cause) <> '';

select * from dim_likely_cause;

select 'dim_incident_type' as table_name,
       count(*) as total_records
from dim_incident_type

union all

select 'dim_response_outcome', count(*)
from dim_response_outcome

union all

select 'dim_site_type', count(*)
from dim_site_type

union all

select 'dim_risk_level', count(*)
from dim_risk_level

union all

select 'dim_likely_cause', count(*)
from dim_likely_cause;
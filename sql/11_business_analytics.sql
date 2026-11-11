#1 – Which Chennai zones recorded the highest rainfall?


select
    z.zone_name,
    round(sum(r.rainfall_mm), 2) as total_rainfall_mm,
    round(avg(r.rainfall_mm), 2) as average_rainfall_mm,
    max(r.rainfall_mm) as maximum_rainfall_mm,
    count(*) as rainfall_records
from fact_rainfall r
join dim_zone z
    on r.zone_id = z.zone_id
where r.rainfall_mm is not null
group by z.zone_name
order by total_rainfall_mm desc;

#Query 2 – Which areas experience repeated flooding?

select
    l.location_name,
    z.zone_name,
    count(*) as total_flood_events,
    count(distinct f.event_date) as flood_days,
    max(f.estimated_affected_people) as maximum_affected_people
from fact_flood f
join dim_location l
    on f.location_id = l.location_id
join dim_zone z
    on f.zone_id = z.zone_id
group by
    l.location_name,
    z.zone_name
having count(*) > 1
order by total_flood_events desc;


#Query 3 – Which locations have the highest road damage complaints?

select
    l.location_name,
    z.zone_name,
    count(*) as total_complaints
from fact_road_complaints r
join dim_location l
    on r.location_id = l.location_id
join dim_zone z
    on r.zone_id = z.zone_id
group by
    l.location_name,
    z.zone_name
order by total_complaints desc
limit 10;

#Query 4 – What is the relationship between rainfall and road damage frequency?
with rainfall_monthly as (
    select
        year(observation_date) as report_year,
        month(observation_date) as report_month,
        zone_id,
        avg(rainfall_mm) as average_rainfall
    from fact_rainfall
    where rainfall_mm is not null
    group by
        year(observation_date),
        month(observation_date),
        zone_id
),

road_monthly as (
    select
        year(complaint_date) as report_year,
        month(complaint_date) as report_month,
        zone_id,
        count(*) as road_complaints
    from fact_road_complaints
    group by
        year(complaint_date),
        month(complaint_date),
        zone_id
)

select
    r.report_year,
    r.report_month,
    z.zone_name,
    round(r.average_rainfall, 2) as average_rainfall_mm,
    coalesce(d.road_complaints, 0) as road_complaints
from rainfall_monthly r
join dim_zone z
    on r.zone_id = z.zone_id
left join road_monthly d
    on r.zone_id = d.zone_id
    and r.report_year = d.report_year
    and r.report_month = d.report_month
order by
    r.report_year,
    r.report_month,
    z.zone_name;
    describe fact_emergency_response;
# Which zones have the highest average emergency response time?
select
    z.zone_name,
    count(e.response_id) as total_incidents,
    round(avg(e.response_time_minutes), 2) as average_response_time_minutes,
    max(e.response_time_minutes) as maximum_response_time_minutes,
    min(e.response_time_minutes) as minimum_response_time_minutes
from fact_emergency_response e
join dim_zone z
    on e.zone_id = z.zone_id
where e.response_time_minutes is not null
group by
    z.zone_id,
    z.zone_name
order by average_response_time_minutes desc;


# Query 6 – Which locations have repeated public complaints?

select
    l.location_name,
    z.zone_name,
    count(*) as total_complaints,
    count(distinct g.complaint_date) as complaint_days
from fact_public_grievances g
join dim_location l
    on g.location_id = l.location_id
join dim_zone z
    on g.zone_id = z.zone_id
group by
    l.location_id,
    l.location_name,
    z.zone_name
having count(*) > 1
order by total_complaints desc;

#Query 7 – Which areas require immediate infrastructure improvement?

select
    l.location_name,
    z.zone_name,

    count(distinct f.flood_event_id) as total_flood_events,

    count(distinct r.road_complaint_id) as total_road_complaints,

    count(distinct w.waterlogging_id) as total_waterlogging_records

from dim_location l

left join fact_flood f
    on l.location_id = f.location_id

left join fact_road_complaints r
    on l.location_id = r.location_id

left join fact_waterlogging_locations w
    on l.location_id = w.location_id

left join dim_zone z
    on f.zone_id = z.zone_id

group by
    l.location_id,
    l.location_name,
    z.zone_name

order by
    total_flood_events desc,
    total_road_complaints desc;

# additonal queries - Monthly flood trend

select
    year(event_date) as report_year,
    month(event_date) as report_month,
    count(*) as total_flood_events,
    sum(estimated_affected_people) as total_affected_people
from fact_flood
group by
    year(event_date),
    month(event_date)
order by report_year, report_month;

# – Zone-wise flood severity analysis

select
    z.zone_name,
    s.severity,
    count(*) as total_flood_events
from fact_flood f
join dim_zone z
    on f.zone_id = z.zone_id
join dim_severity s
    on f.severity = s.severity
group by
    z.zone_name,
    s.severity
order by
    z.zone_name,
    total_flood_events desc;

#Stored procedures

delimiter //

create procedure sp_zone_rainfall_analysis()
begin

    select
        z.zone_name,
        round(avg(r.rainfall_mm), 2) as average_rainfall,
        max(r.rainfall_mm) as maximum_rainfall,
        count(*) as total_records
    from fact_rainfall r
    join dim_zone z
        on r.zone_id = z.zone_id
    where r.rainfall_mm is not null
    group by z.zone_name
    order by average_rainfall desc;

end //

delimiter ;

call sp_zone_rainfall_analysis();

# views

create or replace view vw_zone_rainfall_analysis as
select
    z.zone_id,
    z.zone_name,
    round(avg(r.rainfall_mm), 2) as average_rainfall,
    max(r.rainfall_mm) as maximum_rainfall,
    count(*) as total_records
from fact_rainfall r
join dim_zone z
    on r.zone_id = z.zone_id
where r.rainfall_mm is not null
group by
    z.zone_id,
    z.zone_name;

select * from vw_zone_rainfall_analysis;


# SQL performance optimization by indexing

create index idx_rainfall_zone_date
on fact_rainfall(zone_id, observation_date);

create index idx_flood_zone_date
on fact_flood(zone_id, event_date);

create index idx_road_zone_date
on fact_road_complaints(zone_id, complaint_date);

select
    table_name,
    column_name,
    data_type,
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
    'fact_emergency_response'
)
order by table_name, ordinal_position;
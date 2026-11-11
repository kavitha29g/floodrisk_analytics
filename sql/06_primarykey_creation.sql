-- Check duplicate records in primary key columns


-- 1. rainfall
select observation_date, zone_id, count(*) as duplicate_count
from fact_rainfall
group by observation_date, zone_id
having count(*) > 1;

-- 2. flood
select flood_event_id, count(*) as duplicate_count
from fact_flood
group by flood_event_id
having count(*) > 1;

-- 3. road complaints
select road_complaint_id, count(*) as duplicate_count
from fact_road_complaints
group by road_complaint_id
having count(*) > 1;

-- 4. traffic
select traffic_record_id, count(*) as duplicate_count
from fact_traffic
group by traffic_record_id
having count(*) > 1;

select * from fact_traffic limit 1;

-- 5. public grievances
select grievance_id, count(*) as duplicate_count
from fact_public_grievances
group by grievance_id
having count(*) > 1;

-- 6. waterlogging
select waterlogging_id, count(*) as duplicate_count
from fact_waterlogging_locations
group by waterlogging_id
having count(*) > 1;

-- 7. population
select zone_id, count(*) as duplicate_count
from fact_population
group by zone_id
having count(*) > 1;

-- 8. emergency response
select response_id, count(*) as duplicate_count
from fact_emergency_response
group by response_id
having count(*) > 1;


-- Check NULL values


-- rainfall
select count(*) as null_count
from fact_rainfall
where observation_date is null or zone_id is null;

-- flood
select count(*) as null_count
from fact_flood
where flood_event_id is null;

-- road complaints
select count(*) as null_count
from fact_road_complaints
where road_complaint_id is null;

-- traffic
select count(*) as null_count
from fact_traffic
where traffic_record_id is null;

-- public grievances
select count(*) as null_count
from fact_public_grievances
where grievance_id is null;

-- waterlogging
select count(*) as null_count
from fact_waterlogging_locations
where waterlogging_id is null;

-- population
select count(*) as null_count
from fact_population
where zone_id is null;

-- emergency response
select count(*) as null_count
from fact_emergency_response
where response_id is null;

-- Create Primary Keys

-- 1. rainfall: composite primary key
alter table fact_rainfall
add primary key (observation_date, zone_id);

-- 2. flood
alter table fact_flood
add primary key (flood_event_id);

-- 3. road complaints
alter table fact_road_complaints
add primary key (road_complaint_id);

-- 4. traffic
alter table fact_traffic
add primary key (traffic_record_id);

-- 5. public grievances
alter table fact_public_grievances
add primary key (grievance_id);

-- 6. waterlogging
alter table fact_waterlogging_locations
add primary key (waterlogging_id);

-- 7. population


alter table fact_population
add primary key (year, zone_id);


show keys from fact_population
where key_name = 'primary';



-- 8. emergency response
alter table fact_emergency_response
add primary key (response_id);










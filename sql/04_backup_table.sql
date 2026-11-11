

create table backup_fact_rainfall as
select * from fact_rainfall;

create table backup_fact_flood as
select * from fact_flood;

create table backup_fact_road_complaints as
select * from fact_road_complaints;

create table backup_fact_traffic as
select * from fact_traffic;

create table backup_fact_public_grievances as
select * from fact_public_grievances;

create table backup_fact_waterlogging as
select * from fact_waterlogging_locations;

create table backup_fact_population as
select * from fact_population;

create table backup_fact_emergency_response as
select * from fact_emergency_response;

show tables;

select 'Rainfall' as dataset, count(*) as records
from backup_fact_rainfall

union all

select 'Flood', count(*) from backup_fact_flood

union all

select 'Road Complaints', count(*) from backup_fact_road_complaints

union all

select 'Traffic', count(*) from backup_fact_traffic

union all

select 'Public Grievances', count(*) from backup_fact_public_grievances

union all

select 'Waterlogging', count(*) from backup_fact_waterlogging

union all

select 'Population', count(*) from backup_fact_population

union all

select 'Emergency Response', count(*) from backup_fact_emergency_response;
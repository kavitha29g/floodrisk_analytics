select 'rainfall' as dataset, count(*) as total_records
from fact_rainfall
union all
select 'flood', count(*)
from fact_flood
union all
select 'road complaints', count(*)
from fact_road_complaints
union all
select 'traffic', count(*)
from fact_traffic
union all
select 'public grievances', count(*)
from fact_public_grievances
union all
select 'waterlogging', count(*)
from fact_waterlogging_locations
union all
select 'population', count(*)
from fact_population
union all
select 'emergency response', count(*)
from fact_emergency_response;
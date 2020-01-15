DROP view IF EXISTS career_summary;
create view career_summary as
select
any_value(annual_summary.playerID) as playerID, 
any_value(sum(annual_summary.G_all)) as g_all,
any_value(sum(annual_summary.GS)) as gs,
any_value(sum(annual_summary.AB)) as ab,
any_value(sum(annual_summary.H)) as h,
any_value(sum(annual_summary.HR)) as hr,
any_value(sum(annual_summary.RBI)) as rbi,
any_value(sum(annual_summary.W)) as w,
any_value(sum(annual_summary.L)) as l,
any_value(sum(annual_summary.IPouts)) as IPouts,
any_value(sum(annual_summary.PO)) as po,
any_value(sum(annual_summary.A)) as a,
any_value(sum(annual_summary.E)) as e,
group_concat(distinct fielding.POS) as positions
from annual_summary join fielding
using(playerID,yearID,teamID)
group by annual_summary.playerID
order by annual_summary.playerID;

select * from career_summary limit 10;


DROP view IF EXISTS career_summary;
create view career_summary as
select
any_value(annual_summary.playerID) as playerID, 
any_value(annual_summary.G_all) as G_all,any_value(annual_summary.GS) as GS,
any_value(annual_summary.AB) as AB,
any_value(annual_summary.H) as H,any_value(annual_summary.HR) as HR,
any_value(annual_summary.RBI) as RBI,
any_value(annual_summary.W) as W,any_value(annual_summary.L) as L,
any_value(annual_summary.IPouts) as IPouts,
any_value(annual_summary.PO) as PO,any_value(annual_summary.A) as A,
any_value(annual_summary.E) as E,
group_concat(distinct fielding.POS separator ',') as POS
from lahman2019clean.annual_summary join lahman2019clean.fielding
using(playerID,yearID,teamID)
group by lahman2019clean.annual_summary.playerID
order by lahman2019clean.annual_summary.playerID;

select * from career_summary limit 10;





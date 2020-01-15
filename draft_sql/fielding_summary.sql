SELECT * FROM lahman2019clean.pitching;
create view fielding_summary as

select fielding.playerid,fielding.yearID, fielding.teamID, fielding.PO, fielding.A, fielding.E, group_concat(fielding.pos)
from fielding
where fielding.playerid='willite01'
group by fielding.yearID;

create view fielding_summary as
select fielding.playerid,fielding.yearID, fielding.teamID, fielding.PO, fielding.A, fielding.E, group_concat(fielding.pos) as pos
from fielding
group by fielding.playerid, fielding.yearid;

create view fielding_summary as   
SELECT  any_value(playerID) as playerID,any_value(yearID) as yearID ,
any_value(teamID) as teamID, any_value(sum(PO)) as PO, 
any_value(sum(A)) as A,any_value(sum(E)) as E, 
group_concat(POS order by yearID separator ',') as POS  
FROM lahman2019clean.fielding   
group by lahman2019clean.fielding.playerID, lahman2019clean.fielding.yearID;

select * from fielding_summary where playerid='willite01'

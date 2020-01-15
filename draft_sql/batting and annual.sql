SELECT * FROM lahman2019clean.batting;

create view batting_summary as
select batting.playerID, batting.yearID, batting.teamID, batting.AB, batting.H, batting.HR, batting.RBI 
from batting;

create view annual_summary as
select pfb.playerID,pfb.yearID,pfb.teamID,
appearances_summary.G_all,appearances_summary.GS,pfb.AB,pfb.H,pfb.HR,pfb.RBI,
pfb.W, pfb.L,pfb.IPouts,pfb.PO,pfb.A,pfb.E,pfb.POS from
(select
pf.playerID,pf.yearID,pf.teamID,batting_summary.AB,batting_summary.H,batting_summary.HR,
batting_summary.RBI, pf.W, pf.L,pf.IPouts,pf.PO,pf.A,pf.E,pf.POS
from
(select 
fielding_summary.playerID,fielding_summary.yearID,fielding_summary.teamID,
pitching_summary.W,pitching_summary.L,pitching_summary.IPouts,
fielding_summary.PO, fielding_summary.A, fielding_summary.E, fielding_summary.POS
from lahman2019clean.fielding_summary left join lahman2019clean.pitching_summary
using(playerID,yearID,teamID))pf left join lahman2019clean.batting_summary
using(playerID,yearID,teamID))pfb left join lahman2019clean.appearances_summary
using(playerID,yearID,teamID);

create view annual_summary as
select f_p_b.playerID,f_p_b.yearID,f_p_b.teamID,
appearances_summary.G_all,appearances_summary.GS,f_p_b.AB,f_p_b.H,f_p_b.HR,f_p_b.RBI,
f_p_b.W, f_p_b.L,f_p_b.G,f_p_b.IPouts,f_p_b.PO,f_p_b.A,f_p_b.E,f_p_b.POS from
(select
f_p.playerID,f_p.yearID,f_p.teamID,batting_summary.AB,batting_summary.H,batting_summary.HR,
batting_summary.RBI, f_p.W, f_p.L,f_p.G,f_p.IPouts,f_p.PO,f_p.A,f_p.E,f_p.POS
from
(select 
fielding_summary.playerID,fielding_summary.yearID,fielding_summary.teamID,
pitching_summary.W,pitching_summary.L,pitching_summary.G,pitching_summary.IPouts,
fielding_summary.PO, fielding_summary.A, fielding_summary.E, fielding_summary.POS
from lahman2019clean.fielding_summary left join pitching_summary
using(playerID,yearID,teamID))f_p left join batting_summary
using(playerID,yearID,teamID))f_p_b left join appearances_summary
using(playerID,yearID,teamID);

-- %%sql 
create view annual_summary as
select f_p_b.playerID,f_p_b.yearID,f_p_b.teamID, appearances_summary.G_all,appearances_summary.GS,f_p_b.AB,f_p_b.H,f_p_b.HR,f_p_b.RBI, f_p_b.W, f_p_b.L,f_p_b.G,f_p_b.IPouts,f_p_b.PO,f_p_b.A,f_p_b.E,f_p_b.POS 
from
(select f_p.playerID,f_p.yearID,f_p.teamID,batting_summary.AB,batting_summary.H,batting_summary.HR, batting_summary.RBI, f_p.W, f_p.L,f_p.G,f_p.IPouts,f_p.PO,f_p.A,f_p.E,f_p.POS
from
(select fielding_summary.playerID,fielding_summary.yearID,fielding_summary.teamID, pitching_summary.W,pitching_summary.L,pitching_summary.G,pitching_summary.IPouts, fielding_summary.PO, fielding_summary.A, fielding_summary.E, fielding_summary.POS
from lahman2019clean.fielding_summary 
left join pitching_summary using(playerID,yearID,teamID))f_p 
left join batting_summary using(playerID,yearID,teamID))f_p_b 
left join appearances_summary using(playerID,yearID,teamID);

select * from annual_summary where playerid='willite01'



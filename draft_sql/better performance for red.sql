select people.playerID,people.nameLast,people.bats,
batting.H, batting.AB, batting.h-batting.2B-batting.3b-batting.hr as 1B,batting.2B, batting.3B, batting.HR, batting.RBI, batting.H/batting.AB as AVG, (batting.H+batting.BB)/(batting.BB+batting.AB) as OBP, (batting.h-batting.2B-batting.3b-batting.hr+2*batting.2b+3*batting.3b+4*batting.hr)/batting.AB as SLG
from lahman2019clean.people join lahman2019clean.batting
on people.playerID=batting.playerID
where batting.teamid='BOS' and batting.yearID='1960'
order by (batting.h-batting.2B-batting.3b-batting.hr+2*batting.2b+3*batting.3b+4*batting.hr)/batting.AB DESC
limit 10
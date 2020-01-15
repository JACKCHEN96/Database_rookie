select people.playerid,people.nameLast,people.nameFirst
from halloffame join people join appearances join pitching join managers
on halloffame.playerID=people.playerid=appearances.playerid=pitching.playerID=managers.playerID;

select t.playerid,t.nameLast,t.nameFirst from appearances.playerID join (
	select people.playerid,people.nameLast,people.nameFirst
	from halloffame join people
	on halloffame.playerID=people.playerid
	) t
    on t.playerID=appearances.playerID;

select people.playerID,people.nameLast,people.nameFirst from people 
where
	exists (select * from halloffame where people.playerID=halloffame.playerID) and
	exists (select * from appearances where people.playerID=appearances.playerID) and
	exists (select * from pitching where people.playerID=pitching.playerID) and
	exists (select * from managers where people.playerID=managers.playerID)
    order by people.playerID desc;
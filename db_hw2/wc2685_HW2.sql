DROP TABLE IF EXISTS JOHNS;
DROP VIEW IF EXISTS AverageHeightWeight, AverageHeight;

/*QUESTION 0
EXAMPLE QUESTION
What is the highest salary in baseball history?
*/
Select 1
;
/*SAMPLE ANSWER*/
SELECT MAX(salary) as Max_Salary
FROM Salaries;

/*QUESTION 1
Select the first name, last name, and given name of players who are taller than 6 ft
[hint]: Use "People"
*/

SELECT nameFirst, nameLast, nameGiven from people where height>72
;

/*QUESTION 2
Create a Table of all the distinct players with a first name of John who were born in the United States and
played at Fordham university
Include their first name, last name, playerID, and birth state
Add a column called nameFull that is a concatenated version of first and last
[hint] Use a Join between People and CollegePlaying
*/
DROP TABLE IF EXISTS JOHNS;
CREATE Table JOHNS as
	SELECT DISTINCT nameFirst, nameLast, people.playerID, birthState, concat(nameFirst," ",nameLast) nameFull
    FROM people JOIN collegeplaying ON people.playerID= collegeplaying.playerID
    WHERE people.birthCountry="USA" AND collegeplaying.schoolID="fordham" AND people.nameFirst="John"
;

SELECT * from JOHNS;

/*QUESTION 3
Delete all Johns from the above table whose total career runs batted in is less than 2
[hint] use a subquery to select these johns from people by playerid
[hint] you may have to set sql_safe_updates = 1 to delete without a key
*/
-- SELECT * FROM batting;

SET SQL_SAFE_UPDATES = 0;
Delete From JOHNS
WHERE EXISTS(
SELECT People.playerID
	FROM People join Batting
    ON People.playerID = Batting.playerID
    WHERE Batting.RBI < 2
AND JOHNS.playerID = People.playerID
);
SET SQL_SAFE_UPDATES = 1;

/*QUESTION 4
Group together players with the same birth year, and report the year, 
 the number of players in the year, and average height for the year
 Order the resulting by year in descending order. Put this in a view
 [hint] height will be NULL for some of these years
*/
-- SELECT * FROM people;

CREATE VIEW AverageHeight(birthYear, count_player, average_height)
AS
  SELECT birthYear, count(playerID), avg(height) FROM people GROUP BY birthYear ORDER BY birthYear DESC ;
;
SELECT * FROM averageheight;

/*QUESTION 5
Using Question 3, only include groups with an average weight >180 lbs,
also return the average weight of the group. This time, order by ascending
*/
CREATE VIEW AverageHeightWeight(birthYear, count_player, average_height, average_weight)
AS
  SELECT average_weight_group.birthYear, count_player, average_height, average_weight 
  FROM 
  (SELECT birthYear, avg(weight) as average_weight FROM People GROUP BY birthYear) average_weight_group
  JOIN AverageHeight ON AverageHeight.birthYear = average_weight_group.birthYear
  WHERE average_weight > 180
  ORDER BY birthYear ASC;
;

SELECT * FROM averageheightweight;


/*QUESTION 6
Find the players who made it into the hall of fame who played for a college located in NY
return the player ID, first name, last name, and school ID. Order the players by School alphabetically.
Update all entries with full name Columbia University to 'Columbia University!' in the schools table
*/
SELECT people.playerID, nameFirst, nameLast, schoolId
FROM 
people JOIN
	(SELECT halloffame.playerId as playerId, schoolId
    FROM halloffame JOIN
		(SELECT playerId, CollegePlaying.schoolId 
		FROM CollegePlaying 
		JOIN Schools ON CollegePlaying.schoolId = Schools.schoolId
		WHERE Schools.state = "NY") nySchool
	ON halloffame.playerId=nySchool.playerId) nyHalloffame
ON people.playerId=nyHalloffame.playerId ORDER BY schoolId;
;
SET SQL_SAFE_UPDATES = 0;
UPDATE Schools set name_full = "Columbia University!" where name_full = "Columbia University";
SET SQL_SAFE_UPDATES = 1;

/*QUESTION 7
Find the team id, yearid and average HBP for each team using a subquery.
Limit the total number of entries returned to 100
group the entries by team and year and order by descending values
[hint] be careful to only include entries where AB is > 0
*/

SELECT teamID, yearID, avg(HBP) as average_hbp
FROM
(SELECT teamID, yearID, HBP
FROM Teams
WHERE AB > 0) b
GROUP BY teamID, yearID
ORDER BY average_hbp DESC
LIMIT 100;

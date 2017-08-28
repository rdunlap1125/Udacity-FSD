
CREATE VIEW vw_question1
AS
SELECT title, cnt 
FROM
articles 
INNER JOIN
(
SELECT 
replace(path, '/article/', '') AS slug,
COUNT(*) AS cnt from log 
GROUP BY slug
) AS A
ON articles.slug = A.slug
ORDER BY cnt DESC LIMIT 3;

CREATE VIEW vw_question2
AS
SELECT name, SUM(cnt) AS cnt
FROM
articles 
INNER JOIN
(
SELECT 
replace(path, '/article/', '') AS slug,
COUNT(*) AS cnt from log 
GROUP BY slug
) AS A
ON articles.slug = A.slug
INNER JOIN 
authors 
ON authors.id = articles.author
GROUP BY name
ORDER BY cnt DESC;

CREATE VIEW vw_question3
AS
SELECT date, errorrate FROM
(
SELECT 
time::date as date, 
CAST(SUM(CASE WHEN status != '200 OK' THEN 1 ELSE 0 END) AS FLOAT) / COUNT(*) AS errorrate
FROM log
GROUP BY time::date
) AS A
WHERE errorrate > .01;


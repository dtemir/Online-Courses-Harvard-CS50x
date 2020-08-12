SELECT movies.title FROM movies 
WHERE movies.id IN (SELECT stars.movie_id FROM stars 
WHERE stars.person_id IN (SELECT people.id FROM people 
WHERE name = 'Johnny Depp'))
INTERSECT
SELECT movies.title FROM movies 
WHERE movies.id IN (SELECT stars.movie_id FROM stars 
WHERE stars.person_id IN (SELECT people.id FROM people 
WHERE name = 'Helena Bonham Carter'))
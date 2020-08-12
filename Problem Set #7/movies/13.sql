SELECT people.name FROM people
WHERE people.id IN (SELECT stars.person_id FROM stars 
WHERE stars.movie_id IN (SELECT stars.movie_id FROM stars 
WHERE stars.person_id = (SELECT people.id FROM people
WHERE name = 'Kevin Bacon' and birth = 1958))) and people.name != 'Kevin Bacon'
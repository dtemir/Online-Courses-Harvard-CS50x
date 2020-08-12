SELECT movies.title FROM people
JOIN stars ON people.id = stars.person_id
JOIN movies ON stars.movie_id = movies.id
JOIN ratings ON movies.id = ratings.movie_id
WHERE people.name = 'Chadwick Boseman'
ORDER BY rating DESC
LIMIT 5

-- JOINs are ineffecient, but otherwise I could not sort the movies by their ratings
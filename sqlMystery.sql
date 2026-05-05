--1 sql--
SELECT * FROM crime_scene_report
WHERE date = 20180115 AND type = 'murder' AND city like 'sql city'
--2 sql--
SELECT * FROM crime_scene_report
WHERE date = 20180115 AND type = 'murder' AND city like 'sql city'
--3 sql--
SELECT p.name, dl.car_model 
FROM person p JOIN drivers_license dl ON p.license_id = dl.id              
WHERE p.name  like 'Chris%' 
--4 sql--
SELECT * FROM person 
WHERE address_street_name like 'Northwestern Dr'
ORDER BY address_number DESC LIMIT 5
--5 sql--
SELECT * FROM person 
WHERE name like 'Annabel%' 
AND address_street_name = 'Franklin Ave'
--6 sql--
SELECT p.name, i.transcript FROM person p
JOIN interview i ON p.id = i.person_id
WHERE p.name IN ('Morty Schapiro', 'Annabel Miller')
--7 sql--
SELECT p.name, p.id, g.id, dl.plate_number FROM person p
JOIN get_fit_now_member g ON p.id = g.person_id
JOIN drivers_license dl ON p.license_id = dl.id
WHERE g.id like '48Z%' AND g.membership_status = 'gold'
AND dl.plate_number like '%H42W%'
--8 sql--
SELECT i.transcript FROM interview i
JOIN person p ON i.person_id = p.id
WHERE p.name = 'Jeremy Bowers'
--9 sql--
SELECT p.name, dl.height, fb.event_name FROM person p
JOIN drivers_license dl ON p.license_id = dl.id
JOIN facebook_event_checkin fb ON p.id = fb.person_id
WHERE dl.hair_color = 'red' AND dl.height BETWEEN 65 AND 67
AND dl.car_make = 'Tesla' AND dl.car_model = 'Model S' 
AND fb.event_name = 'SQL Symphony Concert'







--datos--
--id sospechoso-- Annabel Miller 14887
--id sospechoso-- Morty Schapiro 16371
--Sospechoso: miembro del gym
--ID comienza con 48Z
--Placa contiene H42W
--Jeremy Bowers id:67318
-----------------------
--datos--
--genero: Mujer
--Pelo: rojo
--Auto: Tesla
--Altura: entre 65–67 pulgadas
--Asistió varias veces al evento SQL Symphony Concert
--Es quien contrató al asesino
-------------------
--Asesino--
--Miranda Priestly

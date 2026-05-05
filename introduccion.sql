--Crear la base de datos
SELECT * FROM inhabitant
--
SELECT * FROM inhabitant WHERE state = 'Friendly'
--
SELECT * FROM inhabitant WHERE job = 'wheaponsmith'
--Selecciona  Desde           Donde Columna
SELECT * FROM inhabitant WHERE name = 'Stranger' AND job LIKE '%smith'
--Selecciona  nombre de columa     Desde           Donde Columna
SELECT personid FROM inhabitant WHERE name = 'Stranger' 
--      
SELECT gold FROM inhabitant WHERE name = 'Stranger'
--
SELECT gold FROM inhabitant WHERE name = 'Stranger'
--
SELECT * FROM item WHERE owner IS NULL
--
UPDATE item SET owner = 20 WHERE owner IS NULL
--
SELECT * FROM inhabitant WHERE state = 'friendly' AND job = 'dealer' OR job = 'merchant'
--
UPDATE item SET owner = 15 WHERE item = 'teapot' OR item = 'ring'
--
UPDATE inhabitant SET name = 'Pablo' WHERE personid = 20
--
SELECT * FROM inhabitant WHERE job = 'baker' ORDER BY gold
--
SELECT * FROM inhabitant WHERE job = 'pilot'
--1 sql--
SELECT e.FirstName, e.LastName FROM employees e
ORDER BY e.FirstName ASC
--2 sql--
SELECT t.name, t.Milliseconds, a.Title FROM albums a JOIN tracks t ON a.AlbumId = t.AlbumId
WHERE a.Title LIKE 'Big Ones' ORDER BY t.Milliseconds ASC
--3 sql--
SELECT t.UnitPrice,t.name, a.Title FROM albums a JOIN tracks t ON a.AlbumId = t.AlbumId
WHERE t.name ORDER BY t.UnitPrice ASC LIMIT 10
--4 sql--
SELECT t.UnitPrice,t.name, a.Title, g.Name FROM albums a JOIN tracks t ON a.AlbumId = t.AlbumId 
JOIN genres g ON t.GenreId = g.GenreId 
WHERE t.name AND t.UnitPrice = 0.99
--5 sql--
SELECT at.name, t.name, t.Milliseconds, a.Title, g.Name FROM albums a JOIN tracks t ON a.AlbumId = t.AlbumId 
JOIN genres g ON t.GenreId = g.GenreId 
JOIN artists at ON a.ArtistId = at.ArtistId 
WHERE t.name ORDER BY t.Milliseconds ASC LIMIT 20
--6 sql--
SELECT emp.LastName AS empleado, jefe.LastName AS jefe, COUNT(*)  FROM employees emp
JOIN employees jefe ON emp.ReportsTo = jefe.EmployeeId
JOIN customers cus ON emp.EmployeeId = cus.SupportRepId
GROUP BY emp.EmployeeId
ORDER by jefe ASC
--7 sql--
SELECT e.FirstName AS Nombre_Empleado, e.LastName AS Apellido_Empleado,c.FirstName AS Nombre_Cliente, 
c.LastName AS Apellido_Cliente FROM employees e JOIN customers c ON e.EmployeeId = c.SupportRepId
--8 sql--
SELECT c.FirstName AS Nombre, c.LastName AS Apellido, c.Address AS Direccion, i.InvoiceId AS Factura
FROM customers c JOIN invoices i ON c.CustomerId = i.CustomerId
--9 sql--
SELECT g.name, sum(t.TrackId) AS Canciones FROM genres g 
  JOIN tracks t ON g.GenreId = t.GenreId
  GROUP by g.GenreId
--10 sql--
SELECT c.FirstName, art.Name AS Artista
FROM customers c JOIN invoices i ON c.CustomerId = i.CustomerId
JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId JOIN tracks t ON ii.TrackId = t.TrackId
JOIN albums alb ON t.AlbumId = alb.AlbumId JOIN artists art ON alb.ArtistId = art.ArtistId
GROUP BY c.FirstName, art.Name
ORDER BY c.FirstName ASC
--11 sql--
SELECT c.FirstName, c.City, t.name AS Song, g.name AS Genre FROM customers c
JOIN invoices inv ON c.CustomerId = inv.CustomerId JOIN invoice_items inv_i ON inv.InvoiceId = inv_i.InvoiceId
JOIN tracks t ON inv_i.TrackId = t.TrackId JOIN albums a ON t.AlbumId = a.AlbumId
JOIN artists art ON a.ArtistId = art.ArtistId JOIN genres g ON t.GenreId = g.GenreId
--12 sql--
SELECT * FROM employees e
JOIN customers c ON e.EmployeeId = c.SupportRepId JOIN invoices i ON c.CustomerId = i.CustomerId
JOIN invoice_items ii ON i.InvoiceId = ii.InvoiceId JOIN tracks t ON ii.TrackId = t.TrackId
JOIN albums al ON t.AlbumId = al.AlbumId JOIN artists ar ON al.ArtistId = ar.ArtistId
JOIN genres g ON t.GenreId = g.GenreId JOIN media_types mt ON t.MediaTypeId = mt.MediaTypeId
JOIN playlist_track pt ON t.TrackId = pt.TrackId JOIN playlists p ON pt.PlaylistId = p.PlaylistId
--(si se puede)--
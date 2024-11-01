
-- CONSULTAS SIMPLES
SELECT * FROM Clientes;

INSERT INTO Clientes (Nombre, Apellido, DNI, CorreoElectronico, Telefono, FechaNacimiento, NombreUsuario, Contraseña, Churn, IDAreaGeografica, IDPlan) VALUES
('Ana', 'López', '54321678', 'ana.lopez@example.com', '3421234567', '1995-11-23', 'anal', 'hashedpassword', FALSE, 3, 1);

UPDATE Clientes
SET IDPlan = 3
WHERE IDCliente = 1;

DELETE FROM Clientes WHERE IDCliente = 2;

SELECT Clientes.Nombre, Clientes.Apellido, LlamadasClientes.FechaLlamada, LlamadasClientes.MinutosTotales, LlamadasClientes.CostoLlamada
FROM Clientes
INNER JOIN LlamadasClientes ON Clientes.IDCliente = LlamadasClientes.IDCliente;

SELECT Clientes.Nombre, Clientes.Apellido, AreaGeografica.Estado, TiposPlanes.TipoPlan
FROM Clientes
INNER JOIN AreaGeografica ON Clientes.IDAreaGeografica = AreaGeografica.IDAreaGeografica
INNER JOIN TiposPlanes ON Clientes.IDPlan = TiposPlanes.IDPlan;

-- Consultas AVANZADAS
-- SELECT - Listar clientes que hayan realizado llamadas internacionales
SELECT c.Nombre, c.Apellido, lc.TipoLlamada, lc.MinutosTotales
FROM Cliente c
 INNER JOIN LlamadasCliente lc ON c.IDCliente = lc.IDCliente
 WHERE lc.TipoLlamada = 'internacional';                              -- Mostrar solo llamadas internacionales

-- UPDATE - Cambiar el estado de abandono (Churn) de un cliente
UPDATE Cliente
SET Churn = TRUE                                                    --estamos marcando estos clientes como clientes que han abandonado.
WHERE DNI IN ('12345678', '87654321');                -- update multiple segun la condicion del where

-- DELETE - Eliminar registros de llamadas de un cliente específico
UPDATE Clientes
SET Activo = FALSE                          -- suponiendo este activo
WHERE IDCliente = 2; 

-- Consultas con join
-- Listar clientes y su historial de cuentas
SELECT Clientes.Nombre, Clientes.Apellido, HistorialCuentas.FechaAlta, HistorialCuentas.AntiguedadCta, HistorialCuentas.Churn
FROM Clientes
INNER JOIN HistorialCuentas ON Clientes.IDCliente = HistorialCuentas.IDCliente;

-- Obtener el detalle de cargos de las llamadas de los clientes
SELECT Clientes.Nombre, Clientes.Apellido, CargosLlamadas.CargoDia, CargosLlamadas.CargoTarde, CargosLlamadas.CargoNoche, CargosLlamadas.CargoInternacional
FROM Clientes
INNER JOIN LlamadasClientes ON Clientes.IDCliente = LlamadasClientes.IDCliente
INNER JOIN CargosLlamadas ON LlamadasClientes.IDLlamada = CargosLlamadas.IDLlamada;

-- Consultas con agregación group by
--Sumarel número de llamadas por cliente
SELECT c.Nombre, c.Apellido, SUM(lc.CostoLlamada) AS CostoTotal
FROM Clientes c
 INNER JOIN LlamadasClientes lc ON c.IDCliente = lc.IDCliente
  GROUP BY c.Nombre, c.Apellido;

--Sumar el costo total de llamadas por cliente
SELECT c.Nombre, c.Apellido, SUM(lc.CostoLlamada) AS CostoTotal
FROM Clientes c
 INNER JOIN LlamadasClientes lc ON c.IDCliente = lc.IDCliente
 WHERE lc.FechaLlamada BETWEEN '2024-01-01' AND '2024-12-31'  -- Filtrar por rango de fechas
  GROUP BY c.Nombre, c.Apellido;
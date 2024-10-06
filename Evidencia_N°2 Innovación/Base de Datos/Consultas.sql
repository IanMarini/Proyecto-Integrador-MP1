-- ----------------------------------------------------------
-- CONSULTAS
-- ----------------------------------------------------------

-- Consultas CRUD
-- SELECT - Listar clientes que hayan realizado llamadas internacionales
SELECT Clientes.Nombre, Clientes.Apellido, LlamadasClientes.TipoLlamada, LlamadasClientes.MinutosTotales
FROM Clientes
INNER JOIN LlamadasClientes ON Clientes.IDCliente = LlamadasClientes.IDCliente
WHERE LlamadasClientes.TipoLlamada = 'internacional';

-- UPDATE - Cambiar el estado de abandono (Churn) de un cliente
UPDATE Clientes
SET Churn = TRUE
WHERE IDCliente = 5;

-- DELETE - Eliminar registros de llamadas de un cliente específico
DELETE FROM LlamadasClientes
WHERE IDCliente = 2;

-- Consultas con JOIN 
-- Listar clientes y su historial de cuentas
SELECT Clientes.Nombre, Clientes.Apellido, HistorialCuentas.FechaAlta, HistorialCuentas.AntiguedadCta, HistorialCuentas.Churn
FROM Clientes
INNER JOIN HistorialCuentas ON Clientes.IDCliente = HistorialCuentas.IDCliente;

-- Obtener el detalle de cargos de las llamadas de los clientes
SELECT Clientes.Nombre, Clientes.Apellido, CargosLlamadas.CargoDia, CargosLlamadas.CargoTarde, CargosLlamadas.CargoNoche, CargosLlamadas.CargoInternacional
FROM Clientes
INNER JOIN LlamadasClientes ON Clientes.IDCliente = LlamadasClientes.IDCliente
INNER JOIN CargosLlamadas ON LlamadasClientes.IDLlamada = CargosLlamadas.IDLlamada;

-- Consultas con agregación GROUP BY
-- Contar el número de llamadas por cliente
SELECT Clientes.Nombre, Clientes.Apellido, COUNT(LlamadasClientes.IDLlamada) AS TotalLlamadas
FROM Clientes
INNER JOIN LlamadasClientes ON Clientes.IDCliente = LlamadasClientes.IDCliente
GROUP BY Clientes.IDCliente;

-- Sumar el costo total de llamadas por cliente
SELECT Clientes.Nombre, Clientes.Apellido, SUM(LlamadasClientes.CostoLlamada) AS TotalGasto
FROM Clientes
INNER JOIN LlamadasClientes ON Clientes.IDCliente = LlamadasClientes.IDCliente
GROUP BY Clientes.IDCliente;
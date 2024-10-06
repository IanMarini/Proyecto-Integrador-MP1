-- ----------------------------------------------------------
-- CREAR BASE DE DATOS
-- ----------------------------------------------------------

CREATE DATABASE d_BaseDatos_Fidelizacion_ISPC;
USE d_BaseDatos_Fidelizacion_ISPC;

-- ----------------------------------------------------------
-- TABLAS
-- ----------------------------------------------------------

-- Tabla ÁREAS GEOGRÁFICAS
CREATE TABLE AreaGeografica (
    IDAreaGeografica INT PRIMARY KEY AUTO_INCREMENT,
    CodArea VARCHAR(10),
    Estado VARCHAR(50)
);

-- Tabla TIPOS DE PLANES
CREATE TABLE TiposPlanes (
    IDPlan INT PRIMARY KEY AUTO_INCREMENT,
    TipoPlan VARCHAR(50),
    Internacional BOOLEAN,
    CorreoVoz BOOLEAN,
    AntiguedadRequerida INT
);

-- Tabla CLIENTES
CREATE TABLE Clientes (
    IDCliente INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    DNI VARCHAR(20),
    CorreoElectronico VARCHAR(100),
    Telefono VARCHAR(20),
    FechaNacimiento DATE,
    NombreUsuario VARCHAR(50),
    Contraseña VARCHAR(255),
    Churn BOOLEAN,
    IDAreaGeografica INT,
    IDPlan INT,
    FOREIGN KEY (IDAreaGeografica) REFERENCES AreaGeografica(IDAreaGeografica),
    FOREIGN KEY (IDPlan) REFERENCES TiposPlanes(IDPlan)
);

-- Tabla HISTORIAL DE CUENTAS
CREATE TABLE HistorialCuentas (
    IDHistorial INT PRIMARY KEY AUTO_INCREMENT,
    IDCliente INT,
    FechaAlta DATE,
    AntiguedadCta INT,
    Churn BOOLEAN,
    FOREIGN KEY (IDCliente) REFERENCES Clientes(IDCliente)
);

-- Tabla LLAMADAS REALIZADAS CLIENTES
CREATE TABLE LlamadasClientes (
    IDLlamada INT PRIMARY KEY AUTO_INCREMENT,
    IDCliente INT,
    FechaLlamada DATETIME,
    MinutosTotales INT,
    TipoLlamada ENUM('día', 'tarde', 'noche', 'internacional'),
    CostoLlamada DECIMAL(10, 2),
    FOREIGN KEY (IDCliente) REFERENCES Clientes(IDCliente)
);

-- Tabla DETALLE LLAMADAS
CREATE TABLE DetallesLlamadas (
    IDDetalleLlamada INT PRIMARY KEY AUTO_INCREMENT,
    IDLlamada INT,
    DuracionDia INT,
    DuracionTarde INT,
    DuracionNoche INT,
    DuracionInternacional INT,
    FOREIGN KEY (IDLlamada) REFERENCES LlamadasClientes(IDLlamada)
);

-- Tabla CARGOS LLAMADAS
CREATE TABLE CargosLlamadas (
    IDCargoLlamada INT PRIMARY KEY AUTO_INCREMENT,
    IDLlamada INT,
    CargoDia DECIMAL(10, 2),
    CargoTarde DECIMAL(10, 2),
    CargoNoche DECIMAL(10, 2),
    CargoInternacional DECIMAL(10, 2),
    FOREIGN KEY (IDLlamada) REFERENCES LlamadasClientes(IDLlamada)
);

-- Tabla LLAMADA SERVICIO DE CLIENTE
CREATE TABLE LlamadasServicioCliente (
    IDServicioLlamada INT PRIMARY KEY AUTO_INCREMENT,
    IDCliente INT,
    CantidadLlamadas INT,
    FOREIGN KEY (IDCliente) REFERENCES Clientes(IDCliente)
);

-- ----------------------------------------------------------
-- DATOS
-- ----------------------------------------------------------

INSERT INTO AreaGeografica (CodArea, Estado) VALUES
('011', 'Buenos Aires'),
('0351', 'Córdoba'),
('0342', 'Santa Fe');

INSERT INTO TiposPlanes (TipoPlan, Internacional, CorreoVoz, AntiguedadRequerida) VALUES
('Básico', FALSE, TRUE, 0),
('Estándar', TRUE, TRUE, 12),
('Premium', TRUE, TRUE, 24);

INSERT INTO Clientes (Nombre, Apellido, DNI, CorreoElectronico, Telefono, FechaNacimiento, NombreUsuario, Contraseña, Churn, IDAreaGeografica, IDPlan) VALUES
('Juan', 'Pérez', '12345678', 'juan.perez@example.com', '1123456789', '1985-07-23', 'juanp', 'hashedpassword', FALSE, 1, 1),
('María', 'Gómez', '87654321', 'maria.gomez@example.com', '3511234567', '1990-01-12', 'mariag', 'hashedpassword', TRUE, 2, 2);

INSERT INTO HistorialCuentas (IDCliente, FechaAlta, AntiguedadCta, Churn) VALUES
(1, '2020-01-01', 48, FALSE),
(2, '2019-06-15', 54, TRUE);

INSERT INTO LlamadasClientes (IDCliente, FechaLlamada, MinutosTotales, TipoLlamada, CostoLlamada) VALUES
(1, '2024-01-01 10:00:00', 30, 'día', 10.50),
(2, '2024-01-02 15:00:00', 45, 'internacional', 25.00);

INSERT INTO DetallesLlamadas (IDLlamada, DuracionDia, DuracionTarde, DuracionNoche, DuracionInternacional) VALUES
(1, 30, 0, 0, 0),
(2, 0, 0, 0, 45);

INSERT INTO CargosLlamadas (IDLlamada, CargoDia, CargoTarde, CargoNoche, CargoInternacional) VALUES
(1, 10.50, 0.00, 0.00, 0.00),
(2, 0.00, 0.00, 0.00, 25.00);

INSERT INTO LlamadasServicioCliente (IDCliente, CantidadLlamadas) VALUES
(1, 3),
(2, 5);

-- ----------------------------------------------------------
-- CONSULTAS
-- ----------------------------------------------------------

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
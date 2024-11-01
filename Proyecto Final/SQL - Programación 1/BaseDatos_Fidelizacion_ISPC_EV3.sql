 /*Evidencia de aprendizaje 3 - Innovación en Gestión de Datos - TSCDIA - 2024*/
-- CREAR BASE DE DATOS
CREATE DATABASE d_BaseDatos_Fidelizacion_ISPC;
USE d_BaseDatos_Fidelizacion_ISPC;


-- TABLAS
-- AREA GEOGRAFICA (EN SINGULAR)
CREATE TABLE AreaGeografica (
    IDAreaGeografica INT PRIMARY KEY AUTO_INCREMENT,
    CodArea VARCHAR(10),
    Estado VARCHAR(50)
);

--TIPO PLAN
CREATE TABLE TipoPlan (
    IDPlan INT PRIMARY KEY AUTO_INCREMENT,
    TipoPlan VARCHAR(50),
    Internacional BOOLEAN,
    CorreoVoz BOOLEAN,
    AntiguedadRequerida INT
);

--CLIENTE
CREATE TABLE Cliente (
    IDCliente INT PRIMARY KEY AUTO_INCREMENT,
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    DNI VARCHAR(20) UNIQUE,                                                    -- UNIQUE PARA EVITAR DUPLICADOS
    CorreoElectronico VARCHAR(100) UNIQUE, -
    Telefono VARCHAR(20),
    FechaNacimiento DATE,
    NombreUsuario VARCHAR(50) UNIQUE, 
    Contraseña VARCHAR(255),                                                    -- Importante: SE DEBE ENCRIPTAR CONTRASEñA ANTES DE SER CARGADA
    Churn BOOLEAN,
    IDAreaGeografica INT,
    IDPlan INT,
    FOREIGN KEY (IDAreaGeografica) REFERENCES AreaGeografica(IDAreaGeografica),
    FOREIGN KEY (IDPlan) REFERENCES TipoPlan(IDPlan)
);

--HISTORIAL CUENTA
CREATE TABLE HistorialCuenta (
    IDHistorial INT PRIMARY KEY AUTO_INCREMENT,
    IDCliente INT,
    FechaAlta DATE,
    AntiguedadCta INT,
    Churn BOOLEAN,
    FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente)
);

-- LLAMADA CLIENTE
CREATE TABLE LlamadaCliente (
    IDLlamada INT PRIMARY KEY AUTO_INCREMENT,
    IDCliente INT,
    FechaLlamada DATETIME,
    MinutosTotales INT,
    TipoLlamada ENUM('día', 'tarde', 'noche', 'internacional'),
    CostoLlamada DECIMAL(10, 2),
    FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente)
);

--DETALLE LLAMADA
CREATE TABLE DetalleLlamada (
    IDDetalleLlamada INT PRIMARY KEY AUTO_INCREMENT,
    IDLlamada INT,
    DuracionDia INT,
    DuracionTarde INT,
    DuracionNoche INT,
    DuracionInternacional INT,
    FOREIGN KEY (IDLlamada) REFERENCES LlamadaCliente(IDLlamada)
);

--CARGO LLAMADA
CREATE TABLE CargoLlamada (
    IDCargoLlamada INT PRIMARY KEY AUTO_INCREMENT,
    IDLlamada INT,
    CargoDia DECIMAL(10, 2),
    CargoTarde DECIMAL(10, 2),
    CargoNoche DECIMAL(10, 2),
    CargoInternacional DECIMAL(10, 2),
    FOREIGN KEY (IDLlamada) REFERENCES LlamadaCliente(IDLlamada)
);

--SERVICIO CLIENTE
CREATE TABLE LlamadaServicioCliente (
    IDServicioLlamada INT PRIMARY KEY AUTO_INCREMENT,
    IDCliente INT,
    CantidadLlamadas INT,
    FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente)
);


-- OPTIMIZACIONES Y MEJORAS SEGUN FEEDBACK EVIDENCIA No 2

-- Agregar índices a campos utilizados frecuentemente en búsquedas
CREATE INDEX idx_NombreUsuario ON Cliente(NombreUsuario);
CREATE INDEX idx_DNI ON Cliente(DNI);

-- Implementar ON DELETE CASCADE para asegurar integridad referencial al eliminar registros
ALTER TABLE HistorialCuenta
ADD CONSTRAINT fk_HistorialCuenta_Cliente
FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente)
ON DELETE CASCADE;

ALTER TABLE LlamadaCliente
ADD CONSTRAINT fk_LlamadaCliente_Cliente
FOREIGN KEY (IDCliente) REFERENCES Cliente(IDCliente)
ON DELETE CASCADE;



-- INSERTAR DATOS
INSERT INTO AreaGeografica (CodArea, Estado) 
VALUES
('011', 'Buenos Aires'),
('0351', 'Córdoba'),
('0342', 'Santa Fe');

INSERT INTO TipoPlan (TipoPlan, Internacional, CorreoVoz, AntiguedadRequerida) 
VALUES
('Básico', FALSE, TRUE, 0),
('Estándar', TRUE, TRUE, 12),
('Premium', TRUE, TRUE, 24);

INSERT INTO Cliente (Nombre, Apellido, DNI, CorreoElectronico, Telefono, FechaNacimiento, NombreUsuario, Contraseña, Churn, IDAreaGeografica, IDPlan) 
VALUES             
('Juan', 'Pérez', '12345678', 'juan.perez@example.com', '1123456789', '1985-07-23', 'juanp', 'hashedpassword', FALSE, 1, 1),
('María', 'Gómez', '87654321', 'maria.gomez@example.com', '3511234567', '1990-01-12', 'mariag', 'hashedpassword', TRUE, 2, 2);

INSERT INTO HistorialCuenta (IDCliente, FechaAlta, AntiguedadCta, Churn) 
VALUES
(1, '2020-01-01', 48, FALSE),
(2, '2019-06-15', 54, TRUE);

INSERT INTO LlamadaCliente (IDCliente, FechaLlamada, MinutosTotales, TipoLlamada, CostoLlamada)
 VALUES
(1, '2024-01-01 10:00:00', 30, 'día', 10.50),
(2, '2024-01-02 15:00:00', 45, 'internacional', 25.00);

INSERT INTO DetalleLlamada (IDLlamada, DuracionDia, DuracionTarde, DuracionNoche, DuracionInternacional) 
VALUES
(1, 30, 0, 0, 0),
(2, 0, 0, 0, 45);

INSERT INTO CargoLlamada (IDLlamada, CargoDia, CargoTarde, CargoNoche, CargoInternacional)
 VALUES
(1, 10.50, 0.00, 0.00, 0.00),
(2, 0.00, 0.00, 0.00, 25.00);

INSERT INTO LlamadaServicioCliente (IDCliente, CantidadLlamadas) 
VALUES
(1, 3),
(2, 5);





CREATE DATABASE d_bbdd_fidelizacion_ispc;

USE d_bbdd_fidelizacion_ispc; 



-- Tabla para almacenar información de áreas geográficas
CREATE TABLE Area (
    CodArea VARCHAR(10) PRIMARY KEY, -- Código de área (Clave Primaria)
    Estado VARCHAR(50) -- Estado
);

-- Tabla para almacenar información de los planes
CREATE TABLE Planes (
    IDPlan INT PRIMARY KEY AUTO_INCREMENT,
    PlanInternacional BOOLEAN,
    PlanCorreoVoz BOOLEAN,
    Antiguedad INT 
);

-- Tabla para almacenar información de los clientes
CREATE TABLE Clientes 
(
    TelefonoNro VARCHAR(20) PRIMARY KEY, -- Número de teléfono (Clave Primaria)
    CodArea VARCHAR(10), -- Código de área (Clave Foránea que referencia a la tabla Area)
    AntiguedadCta INT, -- Antigüedad de la cuenta
    Churn BOOLEAN, -- Indicador de abandono del servicio
    IDPlan INT, -- ID del plan (Clave Foránea que referencia a la tabla Planes)
    Nombre VARCHAR(100),
    Apellido VARCHAR(100),
    DNI VARCHAR(20),
    Correo VARCHAR(100),
    FechaNacimiento DATE,
    NombreUsuario VARCHAR(50),
    Contraseña VARCHAR(255),
    FOREIGN KEY (CodArea) REFERENCES Area(CodArea),
    FOREIGN KEY (IDPlan) REFERENCES Planes(IDPlan)
);

-- Tabla para almacenar información de las llamadas realizadas por los clientes
CREATE TABLE Llamadas
(
    #ID INT PRIMARY KEY AUTO_INCREMENT,  -- Si se requiere un ID único para cada llamada
    TelefonoNro VARCHAR(20), -- Número de teléfono (Clave Foránea que referencia a la tabla Clientes)
    MinutosDia INT, -- Minutos de llamadas durante el día
    MinutosTarde INT, -- Minutos de llamadas durante la tarde
    MinutosNoche INT, -- Minutos de llamadas durante la noche
    MinutosInternacionales INT, -- Minutos de llamadas internacionales
    LlamadasDia INT, -- Número de llamadas durante el día
    LlamadasTarde INT, -- Número de llamadas durante la tarde
    LlamadasNoche INT, -- Número de llamadas durante la noche
    LlamadasInternacionales INT, -- Número de llamadas internacionales
    CargoDia DECIMAL(10, 2), -- Cargo por las llamadas durante el día
    CargoTarde DECIMAL(10, 2), -- Cargo por las llamadas durante la tarde
    CargoNoche DECIMAL(10, 2), -- Cargo por las llamadas durante la noche
    CargoInter DECIMAL(10, 2), -- Cargo por las llamadas internacionales
    LlamadasServicioCliente INT, -- Número de llamadas al servicio al cliente
    FOREIGN KEY (TelefonoNro) REFERENCES Clientes(TelefonoNro)
);
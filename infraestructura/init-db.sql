CREATE DATABASE IF NOT EXISTS mystery_shopping
CHARACTER SET utf8mb4
COLLATE utf8mb4_unicode_ci;
USE mystery_shopping;



CREATE TABLE Ubicacion (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Codigo_Postal VARCHAR(20),
    Poblacion VARCHAR(255),
    Comunidad_Autonoma VARCHAR(255)
);

CREATE TABLE Local (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Codigo_Local VARCHAR(20),
    Nombre VARCHAR(255),
    Ubicacion_ID INT,
    FOREIGN KEY (Ubicacion_ID) REFERENCES Ubicacion(ID)
);

CREATE TABLE Oficina (
    ID VARCHAR(20) PRIMARY KEY,
    Nombre VARCHAR(255)
);

CREATE TABLE Auditor (
    ID INT AUTO_INCREMENT PRIMARY KEY,
    Codigo_Auditor VARCHAR(45),
    Nombre VARCHAR(255),
    Oficina VARCHAR(20),
    FOREIGN KEY (Oficina) REFERENCES Oficina(ID)
);

CREATE TABLE Evaluacion (
    Id_Evaluacion INT PRIMARY KEY,
    Resultado VARCHAR(255),
    Titulo VARCHAR(255),
    Fecha DATE,
    Codigo_Proyecto VARCHAR(100),
    Auditor INT,
    Id_Local INT,
    FOREIGN KEY (Auditor) REFERENCES Auditor(ID),
    FOREIGN KEY (Id_local) REFERENCES Local(ID)
);
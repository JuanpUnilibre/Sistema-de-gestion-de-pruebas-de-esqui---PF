USE master;
GO

CREATE DATABASE esqui_olimpico;
GO

USE esqui_olimpico;
GO

-- =============================================
-- TABLAS BASE
-- =============================================

CREATE TABLE federaciones (
  Id_Federacion int IDENTITY NOT NULL,
  Nombre        varchar(255) NOT NULL,
  num_Federados int          NOT NULL,
  PRIMARY KEY (Id_Federacion)
);

CREATE TABLE [Estaciones de esqui] (
  Codigo_Estacion  int IDENTITY NOT NULL,
  Nombre           varchar(255) NOT NULL,
  Persona_Contacto varchar(255) NOT NULL,
  Dirrecion        varchar(255) NOT NULL,
  Telefono         int          NOT NULL,
  Km_Esquiables    float(10)    NOT NULL,
  PRIMARY KEY (Codigo_Estacion)
);

CREATE TABLE Participantes (
  Id_participantes int IDENTITY NOT NULL,
  Tipo             varchar(255) NOT NULL,
  PRIMARY KEY (Id_participantes)
);

-- =============================================
-- TABLAS CON DEPENDENCIAS
-- =============================================

CREATE TABLE Esquiadores (
  DNI           int          NOT NULL,
  Nombre        varchar(255) NOT NULL,
  Edad          int          NOT NULL,
  ID_Federacion int          NOT NULL,
  PRIMARY KEY (DNI)
);

CREATE TABLE Equipos (
  Id_Equipo  int IDENTITY NOT NULL,
  Nombre     varchar(255) NOT NULL,
  DniCapitan int          NOT NULL,
  PRIMARY KEY (Id_Equipo)
);

CREATE TABLE Administran (
  ID_Federacion   int NOT NULL,
  Codigo_Estacion int NOT NULL,
  PRIMARY KEY (ID_Federacion, Codigo_Estacion)
);

CREATE TABLE Pistas (
  [Num secuanecial] int       NOT NULL,
  Codigo_Estacion   int       NOT NULL,
  kilometros        float(10) NOT NULL,
  GradoDificultas   varchar(255) NOT NULL,
  PRIMARY KEY ([Num secuanecial], Codigo_Estacion)
);

CREATE TABLE Pista_Compuesta (
  PistasCodigo_Estacion int NOT NULL,
  Pista_1               int NOT NULL,
  Pista_2               int NOT NULL,
  PRIMARY KEY (PistasCodigo_Estacion, Pista_1, Pista_2)
);

CREATE TABLE Pruebas (
  IdTPrueba             int IDENTITY    NOT NULL,
  Nombre                varchar(255)    NOT NULL,
  Tipo                  varchar(255)    NOT NULL,
  Fecha_inicio_Prevista date            NOT NULL,
  fecha_fin_Previsra    date            NOT NULL,
  Tiempo_Ganador        decimal(19, 0)  NOT NULL,
  Codigo_Estacion       int             NOT NULL,
  ID_Ganador            int             NOT NULL,
  PRIMARY KEY (IdTPrueba)
);

CREATE TABLE Pertenece_Equipos (
  DNI       int NOT NULL,
  ID_Equipo int NOT NULL,
  PRIMARY KEY (DNI)
);

CREATE TABLE Pruebas_Pistas (
  ID_Prueba         int NOT NULL,
  [Num secuanecial] int NOT NULL,
  Codigo_Estacion   int NOT NULL,
  PRIMARY KEY (ID_Prueba, [Num secuanecial], Codigo_Estacion)
);

CREATE TABLE Jornadas (
  IdJornada       int IDENTITY  NOT NULL,
  Id_participante int           NOT NULL,
  IdPrueba        int           NOT NULL,
  fecha           date          NOT NULL,
  TiempoParcial   decimal(19,0) NOT NULL,
  PRIMARY KEY (Id_participante, IdPrueba, fecha),
  UNIQUE (IdJornada)
);

CREATE TABLE [Participante indivi] (
  Id_participantes int NOT NULL,
  DNI              int NOT NULL,
  PRIMARY KEY (Id_participantes)
);

CREATE TABLE ParticipanteEqupo (
  Id_participantes int NOT NULL,
  Id_Equipo        int NOT NULL,
  PRIMARY KEY (Id_participantes)
);

CREATE TABLE Participacion (
  Id_participante int NOT NULL,
  IdPrueba        int NOT NULL,
  Posicion        int NOT NULL,
  PRIMARY KEY (Id_participante, IdPrueba)
);

CREATE TABLE interviene (
  DNI              int           NOT NULL,
  IdTPrueba        int           NOT NULL,
  Id_participantes int           NOT NULL,
  fecha            date          NOT NULL,
  TiempoEmpleado   decimal(19,0) NOT NULL,
  Posicion         int           NOT NULL,
  PRIMARY KEY (DNI, IdTPrueba, Id_participantes)
);
GO

-- =============================================
-- FOREIGN KEYS
-- =============================================
ALTER TABLE Esquiadores       ADD CONSTRAINT Federa          FOREIGN KEY (ID_Federacion)   REFERENCES federaciones (Id_Federacion);
ALTER TABLE Equipos            ADD CONSTRAINT [Es capitan]    FOREIGN KEY (DniCapitan)       REFERENCES Esquiadores (DNI);
ALTER TABLE Administran        ADD CONSTRAINT administra      FOREIGN KEY (ID_Federacion)    REFERENCES federaciones (Id_Federacion);
ALTER TABLE Administran        ADD CONSTRAINT [administrada por] FOREIGN KEY (Codigo_Estacion) REFERENCES [Estaciones de esqui] (Codigo_Estacion);
ALTER TABLE Pistas             ADD CONSTRAINT Tiene           FOREIGN KEY (Codigo_Estacion)  REFERENCES [Estaciones de esqui] (Codigo_Estacion);
ALTER TABLE Pista_Compuesta    ADD CONSTRAINT [se compone]    FOREIGN KEY (Pista_1, PistasCodigo_Estacion) REFERENCES Pistas ([Num secuanecial], Codigo_Estacion);
ALTER TABLE Pista_Compuesta    ADD CONSTRAINT compone         FOREIGN KEY (Pista_2, PistasCodigo_Estacion) REFERENCES Pistas ([Num secuanecial], Codigo_Estacion);
ALTER TABLE Pruebas            ADD CONSTRAINT [sede de]       FOREIGN KEY (Codigo_Estacion)  REFERENCES [Estaciones de esqui] (Codigo_Estacion);
ALTER TABLE Pruebas            ADD CONSTRAINT gana            FOREIGN KEY (ID_Ganador)       REFERENCES Participantes (Id_participantes);
ALTER TABLE Pertenece_Equipos  ADD CONSTRAINT [pertenece a]   FOREIGN KEY (ID_Equipo)        REFERENCES Equipos (Id_Equipo);
ALTER TABLE Pertenece_Equipos  ADD CONSTRAINT Integra         FOREIGN KEY (DNI)              REFERENCES Esquiadores (DNI);
ALTER TABLE Pruebas_Pistas     ADD CONSTRAINT [se usa para]   FOREIGN KEY (ID_Prueba)        REFERENCES Pruebas (IdTPrueba);
ALTER TABLE Pruebas_Pistas     ADD CONSTRAINT [es usada en]   FOREIGN KEY ([Num secuanecial], Codigo_Estacion) REFERENCES Pistas ([Num secuanecial], Codigo_Estacion);
ALTER TABLE [Participante indivi] ADD CONSTRAINT pertenece    FOREIGN KEY (DNI)              REFERENCES Esquiadores (DNI);
ALTER TABLE [Participante indivi] ADD CONSTRAINT subtiip      FOREIGN KEY (Id_participantes) REFERENCES Participantes (Id_participantes);
ALTER TABLE ParticipanteEqupo  ADD CONSTRAINT subtipo         FOREIGN KEY (Id_participantes) REFERENCES Participantes (Id_participantes);
ALTER TABLE ParticipanteEqupo  ADD CONSTRAINT es              FOREIGN KEY (Id_Equipo)        REFERENCES Equipos (Id_Equipo);
ALTER TABLE Participacion      ADD CONSTRAINT compite         FOREIGN KEY (Id_participante)  REFERENCES Participantes (Id_participantes);
ALTER TABLE Participacion      ADD CONSTRAINT FKParticipac554505 FOREIGN KEY (IdPrueba)      REFERENCES Pruebas (IdTPrueba);
ALTER TABLE Jornadas           ADD CONSTRAINT [es en la]      FOREIGN KEY (Id_participante, IdPrueba) REFERENCES Participacion (Id_participante, IdPrueba);
ALTER TABLE interviene         ADD CONSTRAINT interve         FOREIGN KEY (DNI)              REFERENCES Esquiadores (DNI);
ALTER TABLE interviene         ADD CONSTRAINT [es prueba]     FOREIGN KEY (IdTPrueba)        REFERENCES Pruebas (IdTPrueba);
ALTER TABLE interviene         ADD CONSTRAINT FKinterviene214810 FOREIGN KEY (Id_participantes) REFERENCES ParticipanteEqupo (Id_participantes);
GO

-- =============================================
-- DATOS: FEDERACIONES
-- =============================================
INSERT INTO federaciones (Nombre, num_Federados) VALUES
('Federacion Española de Esqui',   1500),
('Federacion Francesa de Esqui',   2000),
('Federacion Alemana de Esqui',    1800),
('Federacion Italiana de Esqui',   1600),
('Federacion Austriaca de Esqui',  2200),
('Federacion Suiza de Esqui',      1900),
('Federacion Noruega de Esqui',    2500),
('Federacion Sueca de Esqui',      2100),
('Federacion Americana de Esqui',  3000),
('Federacion Canadiense de Esqui', 2800);

-- =============================================
-- DATOS: ESQUIADORES (DNI manual)
-- =============================================
INSERT INTO Esquiadores (DNI, Nombre, Edad, ID_Federacion) VALUES
(12345678, 'Carlos Lopez',       25, 1),
(87654321, 'Maria Garcia',       28, 1),
(11111111, 'Luis Fernandez',     29, 1),
(22222222, 'Elena Rodriguez',    26, 1),
(33333333, 'Ana Martinez',       23, 1),
(44444444, 'Pedro Sanchez',      31, 1),
(55555555, 'Laura Gomez',        24, 1),
(66666666, 'Jorge Ruiz',         27, 1),
(10000001, 'Pierre Dupont',      30, 2),
(10000002, 'Sophie Martin',      22, 2),
(10000003, 'Jean Leclerc',       28, 2),
(10000004, 'Marie Rousseau',     25, 2),
(10000005, 'Antoine Bernard',    32, 2),
(10000006, 'Camille Petit',      24, 2),
(10000007, 'Hugo Lefevre',       27, 2),
(10000008, 'Amelie Moreau',      26, 2),
(20000001, 'Hans Mueller',       27, 3),
(20000002, 'Anna Schmidt',       24, 3),
(20000003, 'Klaus Weber',        30, 3),
(20000004, 'Petra Fischer',      22, 3),
(20000005, 'Dieter Braun',       29, 3),
(20000006, 'Greta Wagner',       25, 3),
(30000001, 'Marco Rossi',        28, 4),
(30000002, 'Giulia Ferrari',     23, 4),
(30000003, 'Luca Esposito',      31, 4),
(30000004, 'Chiara Romano',      26, 4),
(30000005, 'Alessandro Ricci',   24, 4),
(30000006, 'Francesca Marino',   27, 4),
(40000001, 'Wolfgang Huber',     33, 5),
(40000002, 'Sabine Gruber',      25, 5),
(40000003, 'Markus Bauer',       28, 5),
(40000004, 'Claudia Hofer',      22, 5),
(40000005, 'Stefan Mayer',       30, 5),
(40000006, 'Eva Steiner',        27, 5),
(50000001, 'Lukas Keller',       24, 6),
(50000002, 'Nina Zimmermann',    26, 6),
(50000003, 'Tobias Wirth',       29, 6),
(50000004, 'Silvia Brunner',     23, 6),
(60000001, 'Erik Andersen',      31, 7),
(60000002, 'Ingrid Hansen',      25, 7),
(60000003, 'Lars Olsen',         28, 7),
(60000004, 'Astrid Berg',        24, 7),
(70000001, 'Bjorn Nilsson',      30, 8),
(70000002, 'Maja Lindqvist',     26, 8),
(80000001, 'Tyler Johnson',      27, 9),
(80000002, 'Ashley Williams',    23, 9),
(80000003, 'Ryan Davis',         29, 9),
(80000004, 'Megan Wilson',       25, 9),
(90000001, 'Connor Brown',       28, 10),
(90000002, 'Emma Thompson',      24, 10);

-- =============================================
-- DATOS: EQUIPOS
-- =============================================
INSERT INTO Equipos (Nombre, DniCapitan) VALUES
('Equipo España A',   12345678),
('Equipo España B',   33333333),
('Equipo Francia A',  10000001),
('Equipo Francia B',  10000005),
('Equipo Alemania A', 20000001),
('Equipo Alemania B', 20000005),
('Equipo Italia A',   30000001),
('Equipo Italia B',   30000005),
('Equipo Austria A',  40000001),
('Equipo Austria B',  40000005),
('Equipo Suiza A',    50000001),
('Equipo Noruega A',  60000001),
('Equipo Suecia A',   70000001),
('Equipo USA A',      80000001),
('Equipo Canada A',   90000001);

-- =============================================
-- DATOS: PERTENECE_EQUIPOS
-- Individuales sin equipo: 22222222, 66666666,
-- 10000004, 10000008, 20000004, 30000004,
-- 40000004, 50000004, 60000004, 70000002
-- =============================================
INSERT INTO Pertenece_Equipos (DNI, ID_Equipo) VALUES
(12345678, 1),
(87654321, 1),
(11111111, 1),
(33333333, 2),
(44444444, 2),
(55555555, 2),
(10000001, 3),
(10000002, 3),
(10000003, 3),
(10000005, 4),
(10000006, 4),
(10000007, 4),
(20000001, 5),
(20000002, 5),
(20000003, 5),
(20000005, 6),
(20000006, 6),
(30000001, 7),
(30000002, 7),
(30000003, 7),
(30000005, 8),
(30000006, 8),
(40000001, 9),
(40000002, 9),
(40000003, 9),
(40000005, 10),
(40000006, 10),
(50000001, 11),
(50000002, 11),
(50000003, 11),
(60000001, 12),
(60000002, 12),
(60000003, 12),
(70000001, 13),
(80000001, 14),
(80000002, 14),
(80000003, 14),
(90000001, 15),
(90000002, 15),
(70000002, 13);

-- =============================================
-- DATOS: ESTACIONES DE ESQUI
-- =============================================
INSERT INTO [Estaciones de esqui] (Nombre, Persona_Contacto, Dirrecion, Telefono, Km_Esquiables) VALUES
('Sierra Nevada',     'Juan Perez',    'Granada, España',       958100001, 120),
('Baqueira Beret',    'Rosa Vidal',    'Lleida, España',        973100002, 150),
('Les Deux Alpes',    'Claude Renard', 'Isere, Francia',        476100003, 200),
('Val Thorens',       'Michel Blanc',  'Savoie, Francia',       479100004, 180),
('Chamonix',          'Paul Girard',   'Alta Saboya, Francia',  450100005, 170),
('Garmisch Classic',  'Klaus Bauer',   'Bavaria, Alemania',     882100006, 150),
('Zugspitze Arena',   'Heinz Vogel',   'Wetterstein, Alemania', 881100007, 130),
('Cortina dAmpezzo',  'Roberto Conti', 'Belluno, Italia',       436100008, 140),
('Sestriere',         'Filippo Bruno', 'Turin, Italia',         122100009, 110),
('Kitzbuhel',         'Ernst Huber',   'Tirol, Austria',        535100010, 160),
('St Anton',          'Brigitte Wolf', 'Vorarlberg, Austria',   554100011, 190),
('Verbier',           'Alain Morand',  'Valais, Suiza',         277100012, 210),
('Zermatt',           'Hans Amstutz',  'Valais, Suiza',         279100013, 220),
('Lillehammer',       'Ole Bakken',    'Innlandet, Noruega',    612100014, 130),
('Are',               'Sven Lindgren', 'Jamtland, Suecia',      647100015, 145);

-- =============================================
-- DATOS: ADMINISTRAN
-- =============================================
INSERT INTO Administran (ID_Federacion, Codigo_Estacion) VALUES
(1, 1),(1, 2),(2, 3),(2, 4),(2, 5),
(3, 6),(3, 7),(4, 8),(4, 9),(5, 10),
(5, 11),(6, 12),(6, 13),(7, 14),(8, 15),
(1, 3),(2, 1),(3, 8),(5, 12),(7, 15);

-- =============================================
-- DATOS: PISTAS
-- =============================================
INSERT INTO Pistas ([Num secuanecial], Codigo_Estacion, kilometros, GradoDificultas) VALUES
(1,1,2.5,'Azul'),(2,1,3.8,'Roja'),(3,1,5.0,'Negra'),(4,1,1.5,'Verde'),
(1,2,3.0,'Azul'),(2,2,4.5,'Roja'),(3,2,6.0,'Negra'),(4,2,1.8,'Verde'),
(1,3,4.0,'Roja'),(2,3,6.5,'Negra'),(3,3,2.0,'Azul'),(4,3,2.5,'Azul'),
(1,4,3.5,'Roja'),(2,4,5.5,'Negra'),(3,4,1.8,'Verde'),
(1,5,4.2,'Negra'),(2,5,3.1,'Roja'),
(1,6,3.0,'Azul'),(2,6,4.5,'Roja'),(3,6,5.8,'Negra'),(4,6,1.5,'Verde'),
(1,7,2.8,'Verde'),(2,7,4.0,'Roja'),
(1,8,3.5,'Azul'),(2,8,5.0,'Roja'),(3,8,7.0,'Negra'),
(1,9,2.2,'Verde'),(2,9,3.8,'Azul'),(3,9,4.5,'Negra'),
(1,10,4.5,'Roja'),(2,10,6.0,'Negra'),(3,10,2.5,'Azul'),(4,10,2.0,'Verde'),
(1,11,5.0,'Negra'),(2,11,3.5,'Roja'),
(1,12,4.0,'Roja'),(2,12,6.5,'Negra'),(3,12,2.0,'Verde'),(4,12,3.0,'Azul'),
(1,13,5.5,'Negra'),(2,13,4.0,'Roja'),(3,13,2.5,'Azul'),(4,13,2.8,'Verde'),
(1,14,3.0,'Azul'),(2,14,4.8,'Roja'),(3,14,6.2,'Negra'),(4,14,1.5,'Verde'),
(1,15,3.5,'Roja'),(2,15,5.0,'Negra');

-- =============================================
-- DATOS: PISTA_COMPUESTA
-- =============================================
INSERT INTO Pista_Compuesta (PistasCodigo_Estacion, Pista_1, Pista_2) VALUES
(1,1,2),(1,2,3),(2,1,2),(2,2,3),(3,1,2),(3,2,3),
(4,1,2),(5,1,2),(6,1,2),(6,2,3),(7,1,2),(8,1,2),
(8,2,3),(9,1,2),(10,1,2),(10,2,3),(11,1,2),(12,1,2),
(13,1,2),(14,1,2);

-- =============================================
-- DATOS: PARTICIPANTES
-- =============================================
INSERT INTO Participantes (Tipo) VALUES
('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),
('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),
('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),
('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),
('EQUIPO'),('EQUIPO'),('EQUIPO'),('EQUIPO'),('EQUIPO'),
('EQUIPO'),('EQUIPO'),('EQUIPO'),('EQUIPO'),('EQUIPO'),
('EQUIPO'),('EQUIPO'),('EQUIPO'),('EQUIPO'),('EQUIPO'),
('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),
('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),
('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL'),('INDIVIDUAL');

-- =============================================
-- DATOS: PARTICIPANTE INDIVIDUAL
-- =============================================
INSERT INTO [Participante indivi] (Id_participantes, DNI) VALUES
(1,  22222222),(2,  66666666),(3,  10000004),(4,  10000008),
(5,  20000004),(6,  30000004),(7,  40000004),(8,  50000004),
(9,  60000004),(10, 70000002),(11, 22222222),(12, 66666666),
(13, 10000004),(14, 10000008),(15, 20000004),(16, 30000004),
(17, 40000004),(18, 50000004),(19, 60000004),(20, 70000002);

-- =============================================
-- DATOS: PARTICIPANTE EQUIPO
-- =============================================
INSERT INTO ParticipanteEqupo (Id_participantes, Id_Equipo) VALUES
(21,1),(22,2),(23,3),(24,4),(25,5),
(26,6),(27,7),(28,8),(29,9),(30,10),
(31,11),(32,12),(33,13),(34,14),(35,15);

-- =============================================
-- DATOS: PRUEBAS
-- =============================================
INSERT INTO Pruebas (Nombre, Tipo, Fecha_inicio_Prevista, fecha_fin_Previsra, Tiempo_Ganador, Codigo_Estacion, ID_Ganador) VALUES
('Slalom Gigante Masculino',  'Slalom',    '2026-02-10', '2026-02-12', 18345, 1,  1),
('Slalom Gigante Femenino',   'Slalom',    '2026-02-10', '2026-02-12', 19100, 1,  4),
('Descenso Masculino',        'Descenso',  '2026-02-14', '2026-02-14', 22100, 3,  2),
('Descenso Femenino',         'Descenso',  '2026-02-15', '2026-02-15', 23400, 3,  3),
('Super G Masculino',         'SuperG',    '2026-02-17', '2026-02-17', 20500, 5,  5),
('Super G Femenino',          'SuperG',    '2026-02-17', '2026-02-17', 21300, 5,  6),
('Slalom Especial Masculino', 'Slalom',    '2026-02-19', '2026-02-20', 17800, 6,  7),
('Slalom Especial Femenino',  'Slalom',    '2026-02-19', '2026-02-20', 18600, 6,  8),
('Combinada Masculina',       'Combinada', '2026-02-22', '2026-02-23', 40200, 8,  9),
('Combinada Femenina',        'Combinada', '2026-02-22', '2026-02-23', 41500, 8,  10),
('Slalom por Equipos A',      'Slalom',    '2026-02-25', '2026-02-26', 55200, 10, 21),
('Slalom por Equipos B',      'Slalom',    '2026-02-25', '2026-02-26', 56100, 10, 22),
('Descenso por Equipos A',    'Descenso',  '2026-02-28', '2026-02-28', 48000, 12, 23),
('Descenso por Equipos B',    'Descenso',  '2026-02-28', '2026-02-28', 49500, 12, 24),
('Fondo 10km Masculino',      'Fondo',     '2026-03-02', '2026-03-02', 35000, 14, 1),
('Fondo 10km Femenino',       'Fondo',     '2026-03-02', '2026-03-02', 37500, 14, 4),
('Fondo por Equipos',         'Fondo',     '2026-03-04', '2026-03-05', 72000, 14, 25),
('Salto Individual',          'Salto',     '2026-03-07', '2026-03-07', 10500, 15, 2),
('Salto por Equipos',         'Salto',     '2026-03-08', '2026-03-08', 42000, 15, 26),
('Gran Slalom Final',         'Slalom',    '2026-03-10', '2026-03-12', 17500, 2,  21);

-- =============================================
-- DATOS: PRUEBAS_PISTAS
-- =============================================
INSERT INTO Pruebas_Pistas (ID_Prueba, [Num secuanecial], Codigo_Estacion) VALUES
(1,2,1),(1,3,1),(2,1,1),(2,2,1),(3,1,3),(3,2,3),(4,1,3),(4,3,3),
(5,1,5),(5,2,5),(6,1,5),(6,2,5),(7,1,6),(7,2,6),(8,1,6),(8,3,6),
(9,1,8),(9,2,8),(10,1,8),(10,3,8),(11,1,10),(11,2,10),(12,1,10),
(12,3,10),(13,1,12),(13,2,12),(14,1,12),(14,3,12),(15,1,14),(15,2,14),
(16,1,14),(16,3,14),(17,1,14),(17,2,14),(17,3,14),(18,1,15),(18,2,15),
(19,1,15),(19,2,15),(20,1,2),(20,2,2),(20,3,2),(3,3,3),(7,3,6),
(8,2,6),(11,3,10),(13,3,12),(15,3,14),(4,2,3),(9,3,8);

-- =============================================
-- DATOS: PARTICIPACION
-- =============================================
INSERT INTO Participacion (Id_participante, IdPrueba, Posicion) VALUES
(1,1,2),(2,3,1),(3,4,3),(4,2,1),(5,5,2),(6,6,1),(7,7,3),(8,8,2),
(9,9,1),(10,10,3),(1,15,1),(2,18,1),(3,16,2),(4,16,3),(5,5,4),
(6,6,2),(7,7,1),(8,8,1),(9,9,2),(10,10,1),(21,11,1),(22,12,1),
(23,13,1),(24,14,2),(25,17,1),(26,19,1),(27,11,2),(28,13,3),
(29,14,1),(30,12,3),(31,13,2),(32,17,2),(33,19,2),(34,11,3),
(35,17,3),(1,20,3),(2,20,2),(21,20,1),(23,11,4),(25,11,5),
(4,2,4),(6,6,3),(7,20,4),(9,15,5),(10,16,4),(22,20,2),(24,12,2),
(26,19,3),(28,14,4),(29,17,4);

-- =============================================
-- DATOS: JORNADAS
-- =============================================
INSERT INTO Jornadas (Id_participante, IdPrueba, fecha, TiempoParcial) VALUES
(1,1,'2026-02-10',9200),(1,1,'2026-02-11',9145),(2,3,'2026-02-14',22100),
(3,4,'2026-02-15',23400),(4,2,'2026-02-10',9550),(4,2,'2026-02-11',9550),
(5,5,'2026-02-17',20500),(6,6,'2026-02-17',21300),(7,7,'2026-02-19',8900),
(7,7,'2026-02-20',8900),(8,8,'2026-02-19',9300),(8,8,'2026-02-20',9300),
(9,9,'2026-02-22',20100),(9,9,'2026-02-23',20100),(10,10,'2026-02-22',20750),
(10,10,'2026-02-23',20750),(1,15,'2026-03-02',35000),(2,18,'2026-03-07',10500),
(3,16,'2026-03-02',37500),(4,16,'2026-03-02',38000),(5,5,'2026-02-17',21000),
(6,6,'2026-02-17',21800),(7,20,'2026-03-10',8850),(7,20,'2026-03-11',8850),
(7,20,'2026-03-12',8800),(9,15,'2026-03-02',36000),(10,16,'2026-03-02',39000),
(1,20,'2026-03-10',9100),(1,20,'2026-03-11',9100),(1,20,'2026-03-12',9000),
(2,20,'2026-03-10',8900),(2,20,'2026-03-11',8800),(2,20,'2026-03-12',8800),
(4,2,'2026-02-12',9600),(6,6,'2026-02-17',22000),(8,8,'2026-02-19',9400),
(8,8,'2026-02-20',9200),(3,4,'2026-02-15',24000),(9,9,'2026-02-22',20500),
(10,10,'2026-02-23',21000),(5,5,'2026-02-17',21500),(7,7,'2026-02-19',9100),
(7,7,'2026-02-20',9100),(9,9,'2026-02-23',20200),(10,10,'2026-02-22',21200),
(1,1,'2026-02-12',9300),(2,3,'2026-02-14',22500),(3,16,'2026-03-02',38500),
(6,6,'2026-02-17',22300),(8,8,'2026-02-20',9500);

-- =============================================
-- DATOS: INTERVIENE
-- =============================================
INSERT INTO interviene (DNI, IdTPrueba, Id_participantes, fecha, TiempoEmpleado, Posicion) VALUES
(12345678,11,21,'2026-02-25',18200,1),(87654321,11,21,'2026-02-25',18300,1),(11111111,11,21,'2026-02-26',18700,1),
(33333333,12,22,'2026-02-25',18900,1),(44444444,12,22,'2026-02-25',19000,1),(55555555,12,22,'2026-02-26',19200,1),
(10000001,13,23,'2026-02-28',16100,1),(10000002,13,23,'2026-02-28',15900,1),(10000003,13,23,'2026-02-28',16000,1),
(10000005,14,24,'2026-02-28',16500,2),(10000006,14,24,'2026-02-28',16700,2),
(20000001,17,25,'2026-03-04',24100,1),(20000002,17,25,'2026-03-04',23900,1),(20000003,17,25,'2026-03-05',24000,1),
(20000005,19,26,'2026-03-08',14200,1),(20000006,19,26,'2026-03-08',14100,1),
(30000001,11,27,'2026-02-25',18500,2),(30000002,11,27,'2026-02-25',18600,2),(30000003,11,27,'2026-02-26',18800,2),
(30000005,13,28,'2026-02-28',16300,3),(30000006,13,28,'2026-02-28',16400,3),
(40000001,14,29,'2026-02-28',16000,1),(40000002,14,29,'2026-02-28',16100,1),(40000003,14,29,'2026-02-28',16200,1),
(40000005,12,30,'2026-02-25',19100,3),(40000006,12,30,'2026-02-26',19300,3),
(50000001,13,31,'2026-02-28',16200,2),(50000002,13,31,'2026-02-28',16350,2),(50000003,13,31,'2026-02-28',16500,2),
(60000001,17,32,'2026-03-04',24300,2),(60000002,17,32,'2026-03-05',24500,2),
(70000001,19,33,'2026-03-08',14400,2),(70000002,19,33,'2026-03-08',14600,2),
(80000001,11,34,'2026-02-25',18700,3),(80000002,11,34,'2026-02-25',18900,3),(80000003,11,34,'2026-02-26',19100,3),
(90000001,17,35,'2026-03-04',24600,3),(90000002,17,35,'2026-03-05',24800,3),
(12345678,20,21,'2026-03-10',8800,1),(87654321,20,21,'2026-03-11',8750,1),
(33333333,20,22,'2026-03-10',8950,2),(44444444,20,22,'2026-03-11',9000,2),
(10000001,11,23,'2026-02-25',18400,4),(10000002,11,23,'2026-02-26',18500,4),
(20000001,11,25,'2026-02-25',18600,5),(20000002,11,25,'2026-02-26',18700,5),
(40000001,17,29,'2026-03-04',24200,4),(40000002,17,29,'2026-03-05',24400,4),
(60000001,19,32,'2026-03-08',14500,3),(60000002,19,32,'2026-03-08',14700,3);
GO
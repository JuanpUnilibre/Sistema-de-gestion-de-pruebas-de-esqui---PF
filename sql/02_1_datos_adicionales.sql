USE esqui_olimpico;
GO

/* ============================================================
   2.1 DATOS ADICIONALES
   Completa las tablas para que tengan minimo 50 registros.
   Los campos varchar usan nombres reales o coherentes.
   ============================================================ */

DECLARE @i int;
DECLARE @dni int;
DECLARE @id int;
DECLARE @equipo int;
DECLARE @participante int;
DECLARE @prueba int;
DECLARE @estacion int;
DECLARE @pista int;
DECLARE @pista2 int;
DECLARE @fecha date;

DECLARE @FederacionesExtra TABLE (Nombre varchar(255), num_Federados int);
INSERT INTO @FederacionesExtra (Nombre, num_Federados) VALUES
('Federacion Colombiana de Deportes de Invierno', 920),
('Federacion Argentina de Ski y Andinismo', 1340),
('Federacion Chilena de Ski y Snowboard', 1180),
('Federacion Mexicana de Ski', 760),
('Federacion Japonesa de Ski', 2300),
('Federacion Coreana de Deportes de Invierno', 2100),
('Federacion Finlandesa de Ski', 1980),
('Federacion Danesa de Ski', 870),
('Federacion Neerlandesa de Ski', 940),
('Federacion Belga de Deportes de Nieve', 890),
('Federacion Portuguesa de Deportes de Invierno', 640),
('Federacion Polaca de Ski', 1740),
('Federacion Checa de Ski', 1690),
('Federacion Eslovaca de Ski', 1430),
('Federacion Eslovena de Ski', 1560),
('Federacion Croata de Ski', 1250),
('Federacion Rumana de Ski', 980),
('Federacion Bulgara de Ski', 910),
('Federacion Griega de Deportes de Invierno', 620),
('Federacion Turca de Ski', 1040),
('Federacion Australiana de Ski', 1890),
('Federacion Neozelandesa de Ski', 1320),
('Federacion China de Deportes de Invierno', 2800),
('Federacion Britanica de Ski', 1600),
('Federacion Irlandesa de Deportes de Nieve', 580),
('Federacion Islandesa de Ski', 720),
('Federacion Ucraniana de Ski', 1450),
('Federacion Lituana de Ski', 660),
('Federacion Letona de Ski', 610),
('Federacion Estonia de Ski', 700),
('Federacion Andorrana de Ski', 820),
('Federacion Luxemburguesa de Ski', 430),
('Federacion Serbia de Ski', 840),
('Federacion Bosnia de Ski', 530),
('Federacion Marroqui de Ski', 410),
('Federacion Sudafricana de Deportes de Invierno', 390),
('Federacion Brasilena de Deportes de Nieve', 880),
('Federacion Peruana de Ski', 360),
('Federacion Ecuatoriana de Andinismo y Ski', 340),
('Federacion Uruguaya de Deportes de Invierno', 310);

;WITH actuales AS (
    SELECT Id_Federacion, ROW_NUMBER() OVER (ORDER BY Id_Federacion) AS rn
    FROM federaciones
    WHERE Nombre LIKE 'Federacion Complementaria %'
),
nuevos AS (
    SELECT Nombre, num_Federados, ROW_NUMBER() OVER (ORDER BY Nombre) AS rn
    FROM @FederacionesExtra
)
UPDATE f
SET f.Nombre = n.Nombre,
    f.num_Federados = n.num_Federados
FROM federaciones f
INNER JOIN actuales a ON a.Id_Federacion = f.Id_Federacion
INNER JOIN nuevos n ON n.rn = a.rn;

INSERT INTO federaciones (Nombre, num_Federados)
SELECT TOP (50 - (SELECT COUNT(*) FROM federaciones)) Nombre, num_Federados
FROM @FederacionesExtra fe
WHERE NOT EXISTS (SELECT 1 FROM federaciones f WHERE f.Nombre = fe.Nombre);

DECLARE @EstacionesExtra TABLE (Nombre varchar(255), Persona_Contacto varchar(255), Dirrecion varchar(255), Telefono int, Km_Esquiables float);
INSERT INTO @EstacionesExtra VALUES
('Aspen Snowmass', 'Michael Turner', 'Colorado, Estados Unidos', 970300101, 237),
('Whistler Blackcomb', 'Emily Fraser', 'Columbia Britanica, Canada', 604300102, 200),
('Park City Mountain', 'Daniel Brooks', 'Utah, Estados Unidos', 435300103, 250),
('Vail Mountain', 'Sarah Collins', 'Colorado, Estados Unidos', 970300104, 195),
('Jackson Hole Mountain Resort', 'Robert Miller', 'Wyoming, Estados Unidos', 307300105, 116),
('Niseko United', 'Haruki Sato', 'Hokkaido, Japon', 811300106, 90),
('Hakuba Valley', 'Yuki Tanaka', 'Nagano, Japon', 812300107, 135),
('Yongpyong Resort', 'Min Seo Park', 'Gangwon, Corea del Sur', 823300108, 75),
('Levi Ski Resort', 'Aino Korhonen', 'Laponia, Finlandia', 358300109, 43),
('Ruka Ski Resort', 'Mika Virtanen', 'Kuusamo, Finlandia', 358300110, 35),
('Jasna Nizke Tatry', 'Peter Novak', 'Demänovska Dolina, Eslovaquia', 421300111, 50),
('Spindleruv Mlyn', 'Jan Dvorak', 'Krkonose, Republica Checa', 420300112, 25),
('Kranjska Gora', 'Luka Zupan', 'Alta Carniola, Eslovenia', 386300113, 20),
('Bansko Ski Resort', 'Ivan Petrov', 'Blagoevgrad, Bulgaria', 359300114, 75),
('Poiana Brasov', 'Andrei Popescu', 'Brasov, Rumania', 403300115, 24),
('Gudauri Ski Resort', 'Nika Beridze', 'Caucaso, Georgia', 995300116, 70),
('Palandoken', 'Emre Kaya', 'Erzurum, Turquia', 904300117, 55),
('Perisher', 'Olivia Harris', 'Nueva Gales del Sur, Australia', 612300118, 100),
('Thredbo', 'William Clark', 'Nueva Gales del Sur, Australia', 612300119, 50),
('Coronet Peak', 'James Wilson', 'Queenstown, Nueva Zelanda', 643300120, 40),
('The Remarkables', 'Sophie Walker', 'Otago, Nueva Zelanda', 643300121, 35),
('Cerro Catedral', 'Martin Alvarez', 'Bariloche, Argentina', 294300122, 120),
('Las Lenas', 'Valentina Silva', 'Mendoza, Argentina', 260300123, 65),
('Nevados de Chillan', 'Camila Rojas', 'Nuble, Chile', 422300124, 35),
('Valle Nevado', 'Diego Morales', 'Santiago, Chile', 223300125, 40),
('La Parva', 'Josefina Herrera', 'Santiago, Chile', 223300126, 38),
('Portillo', 'Francisco Vidal', 'Los Andes, Chile', 342300127, 35),
('Cerro Castor', 'Lucia Benitez', 'Ushuaia, Argentina', 290300128, 34),
('El Colorado', 'Nicolas Fuentes', 'Santiago, Chile', 223300129, 50),
('Masikryong Ski Resort', 'Ji Ho Kim', 'Kangwon, Corea del Norte', 850300130, 45),
('Alpensia Resort', 'Joon Lee', 'Pyeongchang, Corea del Sur', 823300131, 28),
('Beidahu Ski Resort', 'Li Wei', 'Jilin, China', 864300132, 60),
('Yabuli Ski Resort', 'Chen Ming', 'Heilongjiang, China', 864300133, 35),
('Gulmarg Ski Resort', 'Aarav Sharma', 'Cachemira, India', 911300134, 25),
('Oukaimeden', 'Youssef El Amrani', 'Atlas, Marruecos', 212300135, 20);

;WITH actuales AS (
    SELECT Codigo_Estacion, ROW_NUMBER() OVER (ORDER BY Codigo_Estacion) AS rn
    FROM [Estaciones de esqui]
    WHERE Nombre LIKE 'Estacion Complementaria %'
),
nuevos AS (
    SELECT Nombre, Persona_Contacto, Dirrecion, Telefono, Km_Esquiables,
           ROW_NUMBER() OVER (ORDER BY Nombre) AS rn
    FROM @EstacionesExtra
)
UPDATE e
SET e.Nombre = n.Nombre,
    e.Persona_Contacto = n.Persona_Contacto,
    e.Dirrecion = n.Dirrecion,
    e.Telefono = n.Telefono,
    e.Km_Esquiables = n.Km_Esquiables
FROM [Estaciones de esqui] e
INNER JOIN actuales a ON a.Codigo_Estacion = e.Codigo_Estacion
INNER JOIN nuevos n ON n.rn = a.rn;

INSERT INTO [Estaciones de esqui] (Nombre, Persona_Contacto, Dirrecion, Telefono, Km_Esquiables)
SELECT TOP (50 - (SELECT COUNT(*) FROM [Estaciones de esqui])) Nombre, Persona_Contacto, Dirrecion, Telefono, Km_Esquiables
FROM @EstacionesExtra ee
WHERE NOT EXISTS (SELECT 1 FROM [Estaciones de esqui] e WHERE e.Nombre = ee.Nombre);

DECLARE @EsquiadoresExtra TABLE (DNI int, Nombre varchar(255), Edad int, ID_Federacion int);
INSERT INTO @EsquiadoresExtra VALUES
(91000051, 'Mateo Restrepo', 24, 11),
(91000052, 'Valeria Montoya', 22, 11),
(91000053, 'Santiago Alvarez', 27, 12),
(91000054, 'Luciana Pereira', 25, 37),
(91000055, 'Rafael Nakamura', 29, 15),
(91000056, 'Akari Yamamoto', 23, 15),
(91000057, 'Min Jun Kim', 26, 16),
(91000058, 'Aino Lehtinen', 28, 17),
(91000059, 'Jakub Kowalski', 30, 22),
(91000060, 'Petra Novakova', 24, 23);

UPDATE e
SET e.Nombre = ex.Nombre,
    e.Edad = ex.Edad,
    e.ID_Federacion = ex.ID_Federacion
FROM Esquiadores e
INNER JOIN @EsquiadoresExtra ex ON ex.DNI = e.DNI
WHERE e.Nombre LIKE 'Esquiador Complementario %';

INSERT INTO Esquiadores (DNI, Nombre, Edad, ID_Federacion)
SELECT DNI, Nombre, Edad, ID_Federacion
FROM @EsquiadoresExtra ex
WHERE (SELECT COUNT(*) FROM Esquiadores) < 60
  AND NOT EXISTS (SELECT 1 FROM Esquiadores e WHERE e.DNI = ex.DNI);

DECLARE @EquiposExtra TABLE (Nombre varchar(255), Orden int);
INSERT INTO @EquiposExtra VALUES
('Equipo Colombia Nieve', 1), ('Equipo Argentina Andes', 2), ('Equipo Chile Cordillera', 3),
('Equipo Japon Hokkaido', 4), ('Equipo Corea Alpino', 5), ('Equipo Finlandia Norte', 6),
('Equipo Polonia Tatras', 7), ('Equipo Chequia Krkonose', 8), ('Equipo Eslovenia Alpes', 9),
('Equipo Australia Snowy', 10), ('Equipo Nueva Zelanda Otago', 11), ('Equipo China Jilin', 12),
('Equipo Gran Bretana Alpino', 13), ('Equipo Islandia Norte', 14), ('Equipo Andorra Pirineos', 15),
('Equipo Croacia Slalom', 16), ('Equipo Bulgaria Pirin', 17), ('Equipo Rumania Brasov', 18),
('Equipo Turquia Erzurum', 19), ('Equipo Brasil Neve', 20), ('Equipo Peru Andes', 21),
('Equipo Mexico Nevado', 22), ('Equipo Belgica Invierno', 23), ('Equipo Portugal Serra', 24),
('Equipo Ucrania Carpatos', 25), ('Equipo Lituania Baltico', 26), ('Equipo Letonia Riga', 27),
('Equipo Estonia Tartu', 28), ('Equipo Serbia Kopaonik', 29), ('Equipo Marruecos Atlas', 30),
('Equipo Sudafrica Drakensberg', 31), ('Equipo Uruguay Invierno', 32), ('Equipo Ecuador Volcanes', 33),
('Equipo Canada Montanas Rocosas', 34), ('Equipo Estados Unidos Rockies', 35);

;WITH actuales AS (
    SELECT Id_Equipo, ROW_NUMBER() OVER (ORDER BY Id_Equipo) AS rn
    FROM Equipos
    WHERE Nombre LIKE 'Equipo Complementario %'
),
nuevos AS (
    SELECT Nombre, ROW_NUMBER() OVER (ORDER BY Orden) AS rn
    FROM @EquiposExtra
)
UPDATE e
SET e.Nombre = n.Nombre
FROM Equipos e
INNER JOIN actuales a ON a.Id_Equipo = e.Id_Equipo
INNER JOIN nuevos n ON n.rn = a.rn;

INSERT INTO Equipos (Nombre, DniCapitan)
SELECT TOP (50 - (SELECT COUNT(*) FROM Equipos))
    eq.Nombre,
    cap.DNI
FROM @EquiposExtra eq
CROSS APPLY (
    SELECT TOP 1 DNI
    FROM Esquiadores
    ORDER BY ABS(CHECKSUM(DNI, eq.Orden))
) cap
WHERE NOT EXISTS (SELECT 1 FROM Equipos e WHERE e.Nombre = eq.Nombre)
ORDER BY eq.Orden;

WHILE (SELECT COUNT(*) FROM Administran) < 50
BEGIN
    SELECT TOP 1 @id = f.Id_Federacion, @estacion = e.Codigo_Estacion
    FROM federaciones f
    CROSS JOIN [Estaciones de esqui] e
    WHERE NOT EXISTS (
        SELECT 1 FROM Administran a
        WHERE a.ID_Federacion = f.Id_Federacion
          AND a.Codigo_Estacion = e.Codigo_Estacion
    )
    ORDER BY f.Id_Federacion, e.Codigo_Estacion;

    INSERT INTO Administran (ID_Federacion, Codigo_Estacion)
    VALUES (@id, @estacion);
END;

WHILE (SELECT COUNT(*) FROM Pistas) < 50
BEGIN
    SELECT TOP 1 @estacion = e.Codigo_Estacion, @pista = n.Numero
    FROM [Estaciones de esqui] e
    CROSS JOIN (VALUES (1), (2), (3), (4), (5)) n(Numero)
    WHERE NOT EXISTS (
        SELECT 1 FROM Pistas p
        WHERE p.Codigo_Estacion = e.Codigo_Estacion
          AND p.[Num secuanecial] = n.Numero
    )
    ORDER BY e.Codigo_Estacion, n.Numero;

    INSERT INTO Pistas ([Num secuanecial], Codigo_Estacion, kilometros, GradoDificultas)
    VALUES (
        @pista,
        @estacion,
        1.5 + (@pista * 0.8),
        CASE WHEN @pista % 4 = 0 THEN 'Negra'
             WHEN @pista % 3 = 0 THEN 'Roja'
             WHEN @pista % 2 = 0 THEN 'Azul'
             ELSE 'Verde' END
    );
END;

WHILE (SELECT COUNT(*) FROM Pista_Compuesta) < 50
BEGIN
    SELECT TOP 1 @estacion = p1.Codigo_Estacion, @pista = p1.[Num secuanecial], @pista2 = p2.[Num secuanecial]
    FROM Pistas p1
    INNER JOIN Pistas p2
        ON p1.Codigo_Estacion = p2.Codigo_Estacion
       AND p1.[Num secuanecial] < p2.[Num secuanecial]
    WHERE NOT EXISTS (
        SELECT 1 FROM Pista_Compuesta pc
        WHERE pc.PistasCodigo_Estacion = p1.Codigo_Estacion
          AND pc.Pista_1 = p1.[Num secuanecial]
          AND pc.Pista_2 = p2.[Num secuanecial]
    )
    ORDER BY p1.Codigo_Estacion, p1.[Num secuanecial], p2.[Num secuanecial];

    INSERT INTO Pista_Compuesta (PistasCodigo_Estacion, Pista_1, Pista_2)
    VALUES (@estacion, @pista, @pista2);
END;

WHILE (SELECT COUNT(*) FROM Participantes) < 50
BEGIN
    INSERT INTO Participantes (Tipo) VALUES ('INDIVIDUAL');
END;

DECLARE @PruebasExtra TABLE (Nombre varchar(255), Tipo varchar(255), Orden int);
INSERT INTO @PruebasExtra VALUES
('Copa Andina de Slalom Masculino', 'Slalom', 1),
('Copa Andina de Slalom Femenino', 'Slalom', 2),
('Descenso Internacional de Aspen', 'Descenso', 3),
('Gran Premio Whistler Alpino', 'Descenso', 4),
('Trofeo Hokkaido Super G', 'SuperG', 5),
('Clasica de Hakuba', 'Slalom', 6),
('Challenge Pyeongchang', 'SuperG', 7),
('Copa Laponia de Fondo', 'Fondo', 8),
('Memorial Tatras de Slalom', 'Slalom', 9),
('Gran Premio Kranjska Gora', 'Slalom', 10),
('Descenso Pirin Bansko', 'Descenso', 11),
('Copa Brasov de Nieve', 'Fondo', 12),
('Trofeo Caucaso Gudauri', 'Descenso', 13),
('Gran Premio Erzurum', 'Salto', 14),
('Copa Snowy Mountains', 'Fondo', 15),
('Desafio Queenstown', 'Slalom', 16),
('Copa Bariloche Catedral', 'Slalom', 17),
('Descenso Las Lenas', 'Descenso', 18),
('Trofeo Nevados de Chillan', 'SuperG', 19),
('Copa Valle Nevado', 'Slalom', 20),
('Clasica La Parva', 'Slalom', 21),
('Gran Premio Portillo', 'Descenso', 22),
('Copa Ushuaia Fin del Mundo', 'Fondo', 23),
('Desafio El Colorado', 'SuperG', 24),
('Copa Alpensia por Equipos', 'Slalom', 25),
('Trofeo Beidahu Invernal', 'Fondo', 26),
('Gran Premio Yabuli', 'Descenso', 27),
('Copa Gulmarg Himalaya', 'Slalom', 28),
('Desafio Atlas Oukaimeden', 'Salto', 29),
('Final Internacional de Montanas', 'Combinada', 30);

;WITH actuales AS (
    SELECT IdTPrueba, ROW_NUMBER() OVER (ORDER BY IdTPrueba) AS rn
    FROM Pruebas
    WHERE Nombre LIKE 'Prueba Complementaria %'
),
nuevos AS (
    SELECT Nombre, Tipo, ROW_NUMBER() OVER (ORDER BY Orden) AS rn
    FROM @PruebasExtra
)
UPDATE p
SET p.Nombre = n.Nombre,
    p.Tipo = n.Tipo
FROM Pruebas p
INNER JOIN actuales a ON a.IdTPrueba = p.IdTPrueba
INNER JOIN nuevos n ON n.rn = a.rn;

INSERT INTO Pruebas (Nombre, Tipo, Fecha_inicio_Prevista, fecha_fin_Previsra, Tiempo_Ganador, Codigo_Estacion, ID_Ganador)
SELECT TOP (50 - (SELECT COUNT(*) FROM Pruebas))
    px.Nombre,
    px.Tipo,
    DATEADD(DAY, px.Orden, '2026-03-15'),
    DATEADD(DAY, px.Orden + 1, '2026-03-15'),
    15000 + (px.Orden * 370),
    est.Codigo_Estacion,
    par.Id_participantes
FROM @PruebasExtra px
CROSS APPLY (
    SELECT TOP 1 Codigo_Estacion
    FROM [Estaciones de esqui]
    ORDER BY ABS(CHECKSUM(Codigo_Estacion, px.Orden))
) est
CROSS APPLY (
    SELECT TOP 1 Id_participantes
    FROM Participantes
    ORDER BY ABS(CHECKSUM(Id_participantes, px.Orden))
) par
WHERE NOT EXISTS (SELECT 1 FROM Pruebas p WHERE p.Nombre = px.Nombre)
ORDER BY px.Orden;

WHILE (SELECT COUNT(*) FROM Pertenece_Equipos) < 50
BEGIN
    SELECT TOP 1 @dni = e.DNI
    FROM Esquiadores e
    WHERE NOT EXISTS (SELECT 1 FROM Pertenece_Equipos pe WHERE pe.DNI = e.DNI)
    ORDER BY e.DNI;

    SELECT TOP 1 @equipo = Id_Equipo
    FROM Equipos
    ORDER BY ABS(CHECKSUM(Id_Equipo, @dni));

    INSERT INTO Pertenece_Equipos (DNI, ID_Equipo)
    VALUES (@dni, @equipo);
END;

WHILE (SELECT COUNT(*) FROM Pruebas_Pistas) < 50
BEGIN
    SELECT TOP 1 @prueba = pr.IdTPrueba, @pista = pi.[Num secuanecial], @estacion = pi.Codigo_Estacion
    FROM Pruebas pr
    INNER JOIN Pistas pi ON pi.Codigo_Estacion = pr.Codigo_Estacion
    WHERE NOT EXISTS (
        SELECT 1 FROM Pruebas_Pistas pp
        WHERE pp.ID_Prueba = pr.IdTPrueba
          AND pp.[Num secuanecial] = pi.[Num secuanecial]
          AND pp.Codigo_Estacion = pi.Codigo_Estacion
    )
    ORDER BY pr.IdTPrueba, pi.[Num secuanecial];

    INSERT INTO Pruebas_Pistas (ID_Prueba, [Num secuanecial], Codigo_Estacion)
    VALUES (@prueba, @pista, @estacion);
END;

WHILE (SELECT COUNT(*) FROM [Participante indivi]) < 50
BEGIN
    INSERT INTO Participantes (Tipo) VALUES ('INDIVIDUAL');
    SET @participante = SCOPE_IDENTITY();

    SELECT TOP 1 @dni = DNI
    FROM Esquiadores
    ORDER BY ABS(CHECKSUM(DNI, @participante));

    INSERT INTO [Participante indivi] (Id_participantes, DNI)
    VALUES (@participante, @dni);
END;

WHILE (SELECT COUNT(*) FROM ParticipanteEqupo) < 50
BEGIN
    INSERT INTO Participantes (Tipo) VALUES ('EQUIPO');
    SET @participante = SCOPE_IDENTITY();

    SELECT TOP 1 @equipo = Id_Equipo
    FROM Equipos
    ORDER BY ABS(CHECKSUM(Id_Equipo, @participante));

    INSERT INTO ParticipanteEqupo (Id_participantes, Id_Equipo)
    VALUES (@participante, @equipo);
END;

WHILE (SELECT COUNT(*) FROM Participacion) < 50
BEGIN
    SELECT TOP 1 @participante = p.Id_participantes, @prueba = pr.IdTPrueba
    FROM Participantes p
    CROSS JOIN Pruebas pr
    WHERE NOT EXISTS (
        SELECT 1 FROM Participacion pa
        WHERE pa.Id_participante = p.Id_participantes
          AND pa.IdPrueba = pr.IdTPrueba
    )
    ORDER BY p.Id_participantes, pr.IdTPrueba;

    INSERT INTO Participacion (Id_participante, IdPrueba, Posicion)
    VALUES (@participante, @prueba, ((@participante + @prueba) % 20) + 1);
END;

WHILE (SELECT COUNT(*) FROM Jornadas) < 50
BEGIN
    SET @i = (SELECT COUNT(*) FROM Jornadas) + 1;
    SET @fecha = DATEADD(DAY, @i, '2026-04-01');

    SELECT TOP 1 @participante = pa.Id_participante, @prueba = pa.IdPrueba
    FROM Participacion pa
    WHERE NOT EXISTS (
        SELECT 1 FROM Jornadas j
        WHERE j.Id_participante = pa.Id_participante
          AND j.IdPrueba = pa.IdPrueba
          AND j.fecha = @fecha
    )
    ORDER BY ABS(CHECKSUM(pa.Id_participante, pa.IdPrueba, @i));

    INSERT INTO Jornadas (Id_participante, IdPrueba, fecha, TiempoParcial)
    VALUES (@participante, @prueba, @fecha, 8000 + (@i * 215));
END;

WHILE (SELECT COUNT(*) FROM interviene) < 50
BEGIN
    SET @i = (SELECT COUNT(*) FROM interviene) + 1;

    SELECT TOP 1 @dni = pe.DNI, @participante = pte.Id_participantes, @prueba = pr.IdTPrueba
    FROM Pertenece_Equipos pe
    INNER JOIN ParticipanteEqupo pte ON pte.Id_Equipo = pe.ID_Equipo
    CROSS JOIN Pruebas pr
    WHERE NOT EXISTS (
        SELECT 1 FROM interviene iv
        WHERE iv.DNI = pe.DNI
          AND iv.IdTPrueba = pr.IdTPrueba
          AND iv.Id_participantes = pte.Id_participantes
    )
    ORDER BY ABS(CHECKSUM(pe.DNI, pte.Id_participantes, pr.IdTPrueba, @i));

    INSERT INTO interviene (DNI, IdTPrueba, Id_participantes, fecha, TiempoEmpleado, Posicion)
    VALUES (@dni, @prueba, @participante, DATEADD(DAY, @i, '2026-04-15'), 9000 + (@i * 180), ((@i - 1) % 20) + 1);
END;
GO

SELECT 'federaciones' AS Tabla, COUNT(*) AS Registros FROM federaciones
UNION ALL SELECT 'Estaciones de esqui', COUNT(*) FROM [Estaciones de esqui]
UNION ALL SELECT 'Participantes', COUNT(*) FROM Participantes
UNION ALL SELECT 'Esquiadores', COUNT(*) FROM Esquiadores
UNION ALL SELECT 'Equipos', COUNT(*) FROM Equipos
UNION ALL SELECT 'Administran', COUNT(*) FROM Administran
UNION ALL SELECT 'Pistas', COUNT(*) FROM Pistas
UNION ALL SELECT 'Pista_Compuesta', COUNT(*) FROM Pista_Compuesta
UNION ALL SELECT 'Pruebas', COUNT(*) FROM Pruebas
UNION ALL SELECT 'Pertenece_Equipos', COUNT(*) FROM Pertenece_Equipos
UNION ALL SELECT 'Pruebas_Pistas', COUNT(*) FROM Pruebas_Pistas
UNION ALL SELECT 'Jornadas', COUNT(*) FROM Jornadas
UNION ALL SELECT 'Participante indivi', COUNT(*) FROM [Participante indivi]
UNION ALL SELECT 'ParticipanteEqupo', COUNT(*) FROM ParticipanteEqupo
UNION ALL SELECT 'Participacion', COUNT(*) FROM Participacion
UNION ALL SELECT 'interviene', COUNT(*) FROM interviene
ORDER BY Tabla;
GO

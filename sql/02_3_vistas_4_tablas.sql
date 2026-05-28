USE esqui_olimpico;
GO

/* ============================================================
   2.3 DOS VISTAS CON INNER JOIN DONDE PARTICIPAN 4 TABLAS
   ============================================================ */

CREATE OR ALTER VIEW v_Pruebas_Estaciones_Pistas
AS
SELECT
    pr.IdTPrueba,
    pr.Nombre AS Prueba,
    pr.Tipo,
    ee.Nombre AS Estacion,
    pi.[Num secuanecial] AS Numero_Pista,
    pi.kilometros,
    pi.GradoDificultas
FROM Pruebas pr
INNER JOIN [Estaciones de esqui] ee
    ON ee.Codigo_Estacion = pr.Codigo_Estacion
INNER JOIN Pruebas_Pistas pp
    ON pp.ID_Prueba = pr.IdTPrueba
   AND pp.Codigo_Estacion = pr.Codigo_Estacion
INNER JOIN Pistas pi
    ON pi.Codigo_Estacion = pp.Codigo_Estacion
   AND pi.[Num secuanecial] = pp.[Num secuanecial];
GO

CREATE OR ALTER VIEW v_Jornadas_Participantes_Pruebas
AS
SELECT
    j.IdJornada,
    p.Id_participantes,
    p.Tipo AS Tipo_Participante,
    pr.Nombre AS Prueba,
    pa.Numero_Secuencial,
    pa.Posicion,
    j.fecha,
    j.TiempoParcial
FROM Jornadas j
INNER JOIN Participacion pa
    ON pa.Id_participante = j.Id_participante
   AND pa.IdPrueba = j.IdPrueba
INNER JOIN Participantes p
    ON p.Id_participantes = pa.Id_participante
INNER JOIN Pruebas pr
    ON pr.IdTPrueba = pa.IdPrueba;
GO

SELECT TOP 20 * FROM v_Pruebas_Estaciones_Pistas;
SELECT TOP 20 * FROM v_Jornadas_Participantes_Pruebas;
GO

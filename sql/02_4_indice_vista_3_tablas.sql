USE esqui_olimpico;
GO

/* ============================================================
   2.4 VISTA CON INNER JOIN DE 3 TABLAS
   Una tabla participante tiene atributo indexado:
   Esquiadores.ID_Federacion
   ============================================================ */

IF NOT EXISTS (
    SELECT 1
    FROM sys.indexes
    WHERE name = 'IX_Esquiadores_ID_Federacion'
      AND object_id = OBJECT_ID('Esquiadores')
)
BEGIN
    CREATE INDEX IX_Esquiadores_ID_Federacion
    ON Esquiadores (ID_Federacion);
END;
GO

CREATE OR ALTER VIEW v_Esquiadores_Federaciones_Individuales
AS
SELECT
    e.DNI,
    e.Nombre AS Esquiador,
    e.Edad,
    f.Nombre AS Federacion,
    pi.Id_participantes
FROM Esquiadores e
INNER JOIN federaciones f
    ON f.Id_Federacion = e.ID_Federacion
INNER JOIN [Participante indivi] pi
    ON pi.DNI = e.DNI;
GO

SELECT TOP 20 * FROM v_Esquiadores_Federaciones_Individuales;
GO

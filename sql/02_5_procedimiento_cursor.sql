USE esqui_olimpico;
GO

/* ============================================================
   2.5 PROCEDIMIENTO ALMACENADO CON CURSOR
   Recorre las pruebas y calcula matematicamente el menor tiempo
   total registrado en Jornadas e interviene.
   ============================================================ */

CREATE OR ALTER PROCEDURE sp_Recalcular_Tiempo_Ganador
AS
BEGIN
    SET NOCOUNT ON;

    DECLARE @IdPrueba int;
    DECLARE @TiempoGanador decimal(19,0);
    DECLARE @PruebasProcesadas int = 0;

    DECLARE cursor_pruebas CURSOR LOCAL FAST_FORWARD FOR
        SELECT IdTPrueba
        FROM Pruebas;

    OPEN cursor_pruebas;
    FETCH NEXT FROM cursor_pruebas INTO @IdPrueba;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        SELECT @TiempoGanador = MIN(TiempoTotal)
        FROM (
            SELECT
                Id_participante,
                SUM(TiempoParcial) AS TiempoTotal
            FROM Jornadas
            WHERE IdPrueba = @IdPrueba
            GROUP BY Id_participante

            UNION ALL

            SELECT
                Id_participantes,
                SUM(TiempoEmpleado) AS TiempoTotal
            FROM interviene
            WHERE IdTPrueba = @IdPrueba
            GROUP BY Id_participantes
        ) tiempos;

        IF @TiempoGanador IS NOT NULL
        BEGIN
            UPDATE Pruebas
            SET Tiempo_Ganador = @TiempoGanador
            WHERE IdTPrueba = @IdPrueba;

            SET @PruebasProcesadas = @PruebasProcesadas + 1;
        END;

        FETCH NEXT FROM cursor_pruebas INTO @IdPrueba;
    END;

    CLOSE cursor_pruebas;
    DEALLOCATE cursor_pruebas;

    SELECT @PruebasProcesadas AS PruebasProcesadas;
END;
GO

EXEC sp_Recalcular_Tiempo_Ganador;
GO

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
    DECLARE @NombrePrueba varchar(255);
    DECLARE @GanadorAnterior int;
    DECLARE @TiempoAnterior decimal(19,0);
    DECLARE @TiempoGanador decimal(19,0);
    DECLARE @IdGanador int;
    DECLARE @PruebasProcesadas int = 0;

    DECLARE @Cambios TABLE (
        IdPrueba int NOT NULL,
        Prueba varchar(255) NOT NULL,
        Ganador_Anterior int NOT NULL,
        Tiempo_Anterior decimal(19,0) NOT NULL,
        Ganador_Calculado int NOT NULL,
        Tiempo_Calculado decimal(19,0) NOT NULL,
        Estado varchar(40) NOT NULL
    );

    DECLARE cursor_pruebas CURSOR LOCAL FAST_FORWARD FOR
        SELECT IdTPrueba
        FROM Pruebas;

    OPEN cursor_pruebas;
    FETCH NEXT FROM cursor_pruebas INTO @IdPrueba;

    WHILE @@FETCH_STATUS = 0
    BEGIN
        SET @TiempoGanador = NULL;
        SET @IdGanador = NULL;

        SELECT
            @NombrePrueba = Nombre,
            @GanadorAnterior = ID_Ganador,
            @TiempoAnterior = Tiempo_Ganador
        FROM Pruebas
        WHERE IdTPrueba = @IdPrueba;

        SELECT TOP 1
            @IdGanador = Id_participante,
            @TiempoGanador = TiempoTotal
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
        ) tiempos
        ORDER BY TiempoTotal, Id_participante;

        IF @TiempoGanador IS NOT NULL
        BEGIN
            INSERT INTO @Cambios (
                IdPrueba, Prueba, Ganador_Anterior, Tiempo_Anterior,
                Ganador_Calculado, Tiempo_Calculado, Estado
            )
            VALUES (
                @IdPrueba,
                @NombrePrueba,
                @GanadorAnterior,
                @TiempoAnterior,
                @IdGanador,
                @TiempoGanador,
                CASE
                    WHEN @GanadorAnterior <> @IdGanador
                      OR @TiempoAnterior <> @TiempoGanador
                    THEN 'Actualizado'
                    ELSE 'Sin cambio'
                END
            );

            UPDATE Pruebas
            SET Tiempo_Ganador = @TiempoGanador,
                ID_Ganador = @IdGanador
            WHERE IdTPrueba = @IdPrueba;

            SET @PruebasProcesadas = @PruebasProcesadas + 1;
        END;

        FETCH NEXT FROM cursor_pruebas INTO @IdPrueba;
    END;

    CLOSE cursor_pruebas;
    DEALLOCATE cursor_pruebas;

    SELECT
        IdPrueba,
        Prueba,
        Ganador_Anterior,
        Tiempo_Anterior,
        Ganador_Calculado,
        Tiempo_Calculado,
        Estado,
        @PruebasProcesadas AS PruebasProcesadas
    FROM @Cambios
    ORDER BY
        CASE WHEN Estado = 'Actualizado' THEN 0 ELSE 1 END,
        IdPrueba;
END;
GO

EXEC sp_Recalcular_Tiempo_Ganador;
GO

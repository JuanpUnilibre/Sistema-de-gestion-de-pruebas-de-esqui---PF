USE esqui_olimpico;
GO

/* ============================================================
   2.2 DISPARADORES
   Tres tablas tienen:
   - Un trigger de actualizacion con auditoria.
   - Un trigger de insercion con una operacion definida.
   Tablas: Esquiadores, Pruebas, federaciones.
   ============================================================ */

IF OBJECT_ID('Auditoria_Esquiadores', 'U') IS NULL
BEGIN
    CREATE TABLE Auditoria_Esquiadores (
        Id_Auditoria int IDENTITY PRIMARY KEY,
        DNI int NOT NULL,
        Nombre_Anterior varchar(255) NOT NULL,
        Nombre_Nuevo varchar(255) NOT NULL,
        Edad_Anterior int NOT NULL,
        Edad_Nueva int NOT NULL,
        Federacion_Anterior int NOT NULL,
        Federacion_Nueva int NOT NULL,
        Accion varchar(20) NOT NULL,
        Fecha_Registro datetime NOT NULL DEFAULT GETDATE(),
        Usuario_BD sysname NOT NULL DEFAULT SUSER_SNAME()
    );
END;
GO

IF OBJECT_ID('Auditoria_Pruebas', 'U') IS NULL
BEGIN
    CREATE TABLE Auditoria_Pruebas (
        Id_Auditoria int IDENTITY PRIMARY KEY,
        IdTPrueba int NOT NULL,
        Tiempo_Anterior decimal(19,0) NOT NULL,
        Tiempo_Nuevo decimal(19,0) NOT NULL,
        Tipo_Anterior varchar(255) NOT NULL,
        Tipo_Nuevo varchar(255) NOT NULL,
        Accion varchar(20) NOT NULL,
        Fecha_Registro datetime NOT NULL DEFAULT GETDATE(),
        Usuario_BD sysname NOT NULL DEFAULT SUSER_SNAME()
    );
END;
GO

IF OBJECT_ID('Auditoria_Federaciones', 'U') IS NULL
BEGIN
    CREATE TABLE Auditoria_Federaciones (
        Id_Auditoria int IDENTITY PRIMARY KEY,
        Id_Federacion int NOT NULL,
        Nombre_Anterior varchar(255) NOT NULL,
        Nombre_Nuevo varchar(255) NOT NULL,
        Federados_Anterior int NOT NULL,
        Federados_Nuevo int NOT NULL,
        Accion varchar(20) NOT NULL,
        Fecha_Registro datetime NOT NULL DEFAULT GETDATE(),
        Usuario_BD sysname NOT NULL DEFAULT SUSER_SNAME()
    );
END;
GO

IF OBJECT_ID('Log_Inserciones_BD', 'U') IS NULL
BEGIN
    CREATE TABLE Log_Inserciones_BD (
        Id_Log int IDENTITY PRIMARY KEY,
        Tabla varchar(80) NOT NULL,
        Id_Registro varchar(80) NOT NULL,
        Descripcion varchar(500) NOT NULL,
        Fecha_Registro datetime NOT NULL DEFAULT GETDATE(),
        Usuario_BD sysname NOT NULL DEFAULT SUSER_SNAME()
    );
END;
GO

CREATE OR ALTER TRIGGER trg_Esquiadores_Auditoria_Update
ON Esquiadores
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Auditoria_Esquiadores (
        DNI, Nombre_Anterior, Nombre_Nuevo, Edad_Anterior, Edad_Nueva,
        Federacion_Anterior, Federacion_Nueva, Accion
    )
    SELECT
        i.DNI, d.Nombre, i.Nombre, d.Edad, i.Edad,
        d.ID_Federacion, i.ID_Federacion, 'UPDATE'
    FROM inserted i
    INNER JOIN deleted d ON d.DNI = i.DNI;
END;
GO

CREATE OR ALTER TRIGGER trg_Esquiadores_Log_Insert
ON Esquiadores
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    UPDATE f
    SET num_Federados = num_Federados + conteo.Total
    FROM federaciones f
    INNER JOIN (
        SELECT ID_Federacion, COUNT(*) AS Total
        FROM inserted
        GROUP BY ID_Federacion
    ) conteo ON conteo.ID_Federacion = f.Id_Federacion;

    INSERT INTO Log_Inserciones_BD (Tabla, Id_Registro, Descripcion)
    SELECT 'Esquiadores', CAST(DNI AS varchar(80)), CONCAT('Nuevo esquiador registrado: ', Nombre)
    FROM inserted;
END;
GO

CREATE OR ALTER TRIGGER trg_Pruebas_Auditoria_Update
ON Pruebas
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Auditoria_Pruebas (
        IdTPrueba, Tiempo_Anterior, Tiempo_Nuevo,
        Tipo_Anterior, Tipo_Nuevo, Accion
    )
    SELECT
        i.IdTPrueba, d.Tiempo_Ganador, i.Tiempo_Ganador,
        d.Tipo, i.Tipo, 'UPDATE'
    FROM inserted i
    INNER JOIN deleted d ON d.IdTPrueba = i.IdTPrueba;
END;
GO

CREATE OR ALTER TRIGGER trg_Pruebas_Log_Insert
ON Pruebas
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Log_Inserciones_BD (Tabla, Id_Registro, Descripcion)
    SELECT 'Pruebas', CAST(IdTPrueba AS varchar(80)), CONCAT('Nueva prueba registrada: ', Nombre, ' - ', Tipo)
    FROM inserted;
END;
GO

CREATE OR ALTER TRIGGER trg_Federaciones_Auditoria_Update
ON federaciones
AFTER UPDATE
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Auditoria_Federaciones (
        Id_Federacion, Nombre_Anterior, Nombre_Nuevo,
        Federados_Anterior, Federados_Nuevo, Accion
    )
    SELECT
        i.Id_Federacion, d.Nombre, i.Nombre,
        d.num_Federados, i.num_Federados, 'UPDATE'
    FROM inserted i
    INNER JOIN deleted d ON d.Id_Federacion = i.Id_Federacion;
END;
GO

CREATE OR ALTER TRIGGER trg_Federaciones_Log_Insert
ON federaciones
AFTER INSERT
AS
BEGIN
    SET NOCOUNT ON;

    INSERT INTO Log_Inserciones_BD (Tabla, Id_Registro, Descripcion)
    SELECT 'federaciones', CAST(Id_Federacion AS varchar(80)), CONCAT('Nueva federacion registrada: ', Nombre)
    FROM inserted;
END;
GO

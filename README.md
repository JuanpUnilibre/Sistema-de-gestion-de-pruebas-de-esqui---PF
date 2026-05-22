# Proyecto Base de Datos - Esqui Olimpico

Este proyecto usa la base de datos enviada en el archivo `script datos base.sql`.

La base de datos se llama:

`esqui_olimpico`

## Carpetas

- `sql`: scripts de SQL Server.
- `app`: aplicacion grafica en Python.
- `diagramas/visual_paradigm`: archivo para importar el modelo en Visual Paradigm.

## Orden para probar la base de datos

1. Abrir SQL Server Management Studio.
2. Ejecutar primero:

   `sql/01_script_base_original.sql`

3. Ejecutar despues, en este orden:

   `sql/02_1_datos_adicionales.sql`
   `sql/02_2_triggers_auditoria.sql`
   `sql/02_3_vistas_4_tablas.sql`
   `sql/02_4_indice_vista_3_tablas.sql`
   `sql/02_5_procedimiento_cursor.sql`

El primer script crea la base original.
Los scripts siguientes agregan datos, triggers, vistas, indice, auditorias y procedimiento.

## Consultas para probar

```sql
USE esqui_olimpico;
GO

SELECT * FROM v_Pruebas_Estaciones_Pistas;
SELECT * FROM v_Jornadas_Participantes_Pruebas;
SELECT * FROM v_Esquiadores_Federaciones_Individuales;

EXEC sp_Recalcular_Tiempo_Ganador;

SELECT * FROM Auditoria_Esquiadores;
SELECT * FROM Auditoria_Pruebas;
SELECT * FROM Auditoria_Federaciones;
SELECT * FROM Log_Inserciones_BD;
```
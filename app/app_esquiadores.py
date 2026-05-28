import re
import tkinter as tk
from datetime import date
from tkinter import ttk, messagebox
import pyodbc

SERVER = r".\SQLEXPRESS"
DATABASE = "esqui_olimpico"
DRIVER = "ODBC Driver 17 for SQL Server"


def conectar():
    cadena = (
        f"DRIVER={{{DRIVER}}};"
        f"SERVER={SERVER};"
        f"DATABASE={DATABASE};"
        "Trusted_Connection=yes;"
        "TrustServerCertificate=yes;"
    )
    return pyodbc.connect(cadena)


TABLAS_GESTION = {
    "Federaciones": {
        "tabla": "federaciones",
        "pk": ["Id_Federacion"],
        "identity": ["Id_Federacion"],
        "order": ["Id_Federacion"],
        "columnas": [
            ("Id_Federacion", "ID", "int"),
            ("Nombre", "Nombre", "text"),
            ("num_Federados", "Num. federados", "int"),
        ],
    },
    "Estaciones de esqui": {
        "tabla": "Estaciones de esqui",
        "pk": ["Codigo_Estacion"],
        "identity": ["Codigo_Estacion"],
        "order": ["Codigo_Estacion"],
        "columnas": [
            ("Codigo_Estacion", "Codigo", "int"),
            ("Nombre", "Nombre", "text"),
            ("Persona_Contacto", "Contacto", "text"),
            ("Dirrecion", "Direccion", "text"),
            ("Telefono", "Telefono", "int"),
            ("Km_Esquiables", "Km esquiables", "float"),
        ],
    },
    "Participantes": {
        "tabla": "Participantes",
        "pk": ["Id_participantes"],
        "identity": ["Id_participantes"],
        "order": ["Id_participantes"],
        "readonly": True,
        "readonly_reason": "Participantes es la tabla base de los subtipos. Cree participantes desde Participante individual o Participante equipo para conservar la regla INDIVIDUAL/EQUIPO.",
        "columnas": [
            ("Id_participantes", "ID", "int"),
            ("Tipo", "Tipo", "text"),
        ],
    },
    "Esquiadores": {
        "tabla": "Esquiadores",
        "pk": ["DNI"],
        "identity": [],
        "order": ["DNI"],
        "columnas": [
            ("DNI", "DNI", "int"),
            ("Nombre", "Nombre", "text"),
            ("Edad", "Edad", "int"),
            ("ID_Federacion", "ID Federacion", "int"),
        ],
    },
    "Equipos": {
        "tabla": "Equipos",
        "pk": ["Id_Equipo"],
        "identity": ["Id_Equipo"],
        "order": ["Id_Equipo"],
        "columnas": [
            ("Id_Equipo", "ID equipo", "int"),
            ("Nombre", "Nombre", "text"),
            ("DniCapitan", "DNI capitan", "int"),
        ],
    },
    "Administran": {
        "tabla": "Administran",
        "pk": ["ID_Federacion", "Codigo_Estacion"],
        "identity": [],
        "order": ["ID_Federacion", "Codigo_Estacion"],
        "columnas": [
            ("ID_Federacion", "ID Federacion", "int"),
            ("Codigo_Estacion", "Codigo estacion", "int"),
        ],
    },
    "Pistas": {
        "tabla": "Pistas",
        "pk": ["Num secuanecial", "Codigo_Estacion"],
        "identity": [],
        "order": ["Codigo_Estacion", "Num secuanecial"],
        "columnas": [
            ("Num secuanecial", "Num secuencial", "int"),
            ("Codigo_Estacion", "Codigo estacion", "int"),
            ("kilometros", "Kilometros", "float"),
            ("GradoDificultas", "Dificultad", "text"),
        ],
    },
    "Pista compuesta": {
        "tabla": "Pista_Compuesta",
        "pk": ["Codigo_Estacion", "Pista_Compuesta", "Pista_Componente"],
        "identity": [],
        "order": ["Codigo_Estacion", "Pista_Compuesta", "Pista_Componente"],
        "columnas": [
            ("Codigo_Estacion", "Codigo estacion", "int"),
            ("Pista_Compuesta", "Pista compuesta", "int"),
            ("Pista_Componente", "Pista componente", "int"),
        ],
    },
    "Pruebas": {
        "tabla": "Pruebas",
        "pk": ["IdTPrueba"],
        "identity": ["IdTPrueba"],
        "order": ["IdTPrueba"],
        "insert_disabled": True,
        "insert_disabled_reason": "Para crear una prueba nueva tambien debe registrar sus pistas, participantes y resultados relacionados.",
        "readonly_fields": ["Tiempo_Ganador", "Codigo_Estacion", "ID_Ganador"],
        "help": "Puede editar nombre, tipo y fechas. El ganador y el tiempo ganador se recalculan con el procedimiento; la estacion queda fija para no romper las pistas asociadas.",
        "columnas": [
            ("IdTPrueba", "ID prueba", "int"),
            ("Nombre", "Nombre", "text"),
            ("Tipo", "Tipo", "text"),
            ("Fecha_inicio_Prevista", "Fecha inicio", "date"),
            ("fecha_fin_Previsra", "Fecha fin", "date"),
            ("Tiempo_Ganador", "Tiempo ganador", "decimal"),
            ("Codigo_Estacion", "Codigo estacion", "int"),
            ("ID_Ganador", "ID ganador", "int"),
        ],
    },
    "Pertenece a equipos": {
        "tabla": "Pertenece_Equipos",
        "pk": ["DNI"],
        "identity": [],
        "order": ["DNI"],
        "columnas": [
            ("DNI", "DNI", "int"),
            ("ID_Equipo", "ID equipo", "int"),
        ],
    },
    "Pruebas por pistas": {
        "tabla": "Pruebas_Pistas",
        "pk": ["ID_Prueba", "Num secuanecial", "Codigo_Estacion"],
        "identity": [],
        "order": ["ID_Prueba", "Codigo_Estacion", "Num secuanecial"],
        "columnas": [
            ("ID_Prueba", "ID prueba", "int"),
            ("Num secuanecial", "Num secuencial", "int"),
            ("Codigo_Estacion", "Codigo estacion", "int"),
        ],
    },
    "Jornadas": {
        "tabla": "Jornadas",
        "pk": ["Id_participante", "IdPrueba", "fecha"],
        "identity": ["IdJornada"],
        "order": ["IdJornada"],
        "columnas": [
            ("IdJornada", "ID jornada", "int"),
            ("Id_participante", "ID participante", "int"),
            ("IdPrueba", "ID prueba", "int"),
            ("fecha", "Fecha", "date"),
            ("TiempoParcial", "Tiempo parcial", "decimal"),
        ],
    },
    "Participante individual": {
        "tabla": "Participante indivi",
        "pk": ["Id_participantes"],
        "identity": ["Id_participantes"],
        "auto_participante_tipo": "INDIVIDUAL",
        "order": ["Id_participantes"],
        "columnas": [
            ("Id_participantes", "ID participante", "int"),
            ("DNI", "DNI", "int"),
        ],
    },
    "Participante equipo": {
        "tabla": "ParticipanteEqupo",
        "pk": ["Id_participantes"],
        "identity": ["Id_participantes"],
        "auto_participante_tipo": "EQUIPO",
        "order": ["Id_participantes"],
        "columnas": [
            ("Id_participantes", "ID participante", "int"),
            ("Id_Equipo", "ID equipo", "int"),
        ],
    },
    "Participacion": {
        "tabla": "Participacion",
        "pk": ["Id_participante", "IdPrueba"],
        "identity": [],
        "order": ["Id_participante", "IdPrueba"],
        "columnas": [
            ("Id_participante", "ID participante", "int"),
            ("IdPrueba", "ID prueba", "int"),
            ("Numero_Secuencial", "Num. secuencial", "int"),
            ("Posicion", "Posicion", "int"),
        ],
    },
    "Intervenciones": {
        "tabla": "interviene",
        "pk": ["DNI", "IdTPrueba", "Id_participantes"],
        "identity": [],
        "order": ["IdTPrueba", "Id_participantes", "DNI"],
        "columnas": [
            ("DNI", "DNI", "int"),
            ("IdTPrueba", "ID prueba", "int"),
            ("Id_participantes", "ID participante", "int"),
            ("fecha", "Fecha", "date"),
            ("TiempoEmpleado", "Tiempo empleado", "decimal"),
            ("Posicion", "Posicion", "int"),
        ],
    },
}


MODULOS_GESTION = {
    "participantes": {
        "titulo": "Gestion de participantes",
        "subtitulo": "Administre esquiadores, participantes individuales, equipos participantes e intervenciones.",
        "tablas": [
            "Esquiadores",
            "Participantes",
            "Participante individual",
            "Participante equipo",
            "Equipos",
            "Pertenece a equipos",
            "Participacion",
            "Jornadas",
            "Intervenciones",
        ],
        "tabla_inicial": "Esquiadores",
    },
    "pruebas": {
        "titulo": "Gestion de pruebas",
        "subtitulo": "Administre pruebas, participaciones, jornadas, pistas usadas y resultados.",
        "tablas": [
            "Pruebas",
            "Participacion",
            "Jornadas",
            "Pruebas por pistas",
            "Intervenciones",
        ],
        "tabla_inicial": "Pruebas",
    },
    "pistas": {
        "titulo": "Gestion de pistas y estaciones",
        "subtitulo": "Administre estaciones de esqui, pistas, pistas compuestas y administracion por federacion.",
        "tablas": [
            "Estaciones de esqui",
            "Pistas",
            "Pista compuesta",
            "Pruebas por pistas",
            "Administran",
        ],
        "tabla_inicial": "Estaciones de esqui",
    },
    "federaciones": {
        "titulo": "Gestion de federaciones y equipos",
        "subtitulo": "Administre federaciones, equipos, capitanes y composicion de equipos.",
        "tablas": [
            "Federaciones",
            "Equipos",
            "Pertenece a equipos",
            "Administran",
        ],
        "tabla_inicial": "Federaciones",
    },
}


def q(nombre):
    return f"[{nombre.replace(']', ']]')}]"


REGLAS_SQL = {
    "Federa": "La federacion indicada no existe. Revise el campo ID Federacion.",
    "Es capitan": "El DNI del capitan no existe en Esquiadores.",
    "administra": "La federacion indicada no existe.",
    "administrada por": "La estacion indicada no existe.",
    "Tiene": "La estacion indicada para la pista no existe.",
    "pista compuesta existe": "La pista compuesta debe existir en Pistas para esa estacion.",
    "pista componente existe": "La pista componente debe existir en Pistas para esa estacion.",
    "sede de": "La estacion indicada para la prueba no existe.",
    "gana": "El ganador indicado no existe en Participantes.",
    "pertenece a": "El equipo indicado no existe.",
    "Integra": "El DNI indicado no existe en Esquiadores.",
    "se usa para": "La prueba indicada no existe.",
    "usa pistas de su estacion": "La pista debe pertenecer a la misma estacion de la prueba.",
    "es usada en": "La pista indicada no existe para esa estacion.",
    "pertenece": "El DNI indicado no existe en Esquiadores.",
    "subtiip": "El participante individual indicado no existe en Participantes.",
    "subtipo": "El participante de equipo indicado no existe en Participantes.",
    "compite": "El participante indicado no existe.",
    "FKParticipac554505": "La prueba indicada no existe.",
    "es en la": "La jornada debe corresponder a una participacion ya registrada.",
    "interve": "El DNI indicado no existe en Esquiadores.",
    "es prueba": "La prueba indicada no existe.",
    "FKinterviene214810": "El participante de equipo indicado no existe.",
    "equipo participa en prueba": "El equipo debe estar registrado en Participacion para esa prueba.",
    "FK_Pruebas_Ganador_Participacion": "El ganador debe estar registrado como participante de esa misma prueba.",
}


MENSAJES_NEGOCIO = (
    "El participante individual debe tener Tipo = INDIVIDUAL.",
    "Un esquiador de equipo no puede registrarse como participante individual.",
    "El participante de equipo debe tener Tipo = EQUIPO.",
    "Un esquiador individual no puede registrarse como miembro de equipo.",
    "Las jornadas solo registran tiempos de participantes individuales.",
    "El esquiador que interviene debe pertenecer al equipo participante.",
    "El capitan ya pertenece a otro equipo.",
    "Un capitan no puede asignarse a mas de un equipo.",
)


class AppEsquiadores(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Proyecto Esqui Olimpico")
        self.geometry("1120x680")
        self.minsize(980, 600)
        self.dni_seleccionado = None
        self.federaciones = {}
        self.pantalla_actual = None
        self.modulo_actual = "participantes"
        self.tabla_actual = MODULOS_GESTION[self.modulo_actual]["tabla_inicial"]
        self.registro_generico_seleccionado = None
        self.modo_generico = "nuevo"
        self.campos_genericos = {}
        self.crear_interfaz()
        self.cargar_federaciones()
        self.cargar_esquiadores()
        self.mostrar_pantalla("inicio")

    def crear_interfaz(self):
        self.config(bg="#f4f6f8")
        self.estilo = ttk.Style(self)
        self.estilo.theme_use("clam")
        self.estilo.configure("TFrame", background="#f4f6f8")
        self.estilo.configure("Menu.TFrame", background="#1f2937")
        self.estilo.configure("Card.TFrame", background="white", relief=tk.FLAT)
        self.estilo.configure("TLabel", background="#f4f6f8", foreground="#111827", font=("Segoe UI", 10))
        self.estilo.configure("Titulo.TLabel", background="#f4f6f8", foreground="#111827", font=("Segoe UI", 20, "bold"))
        self.estilo.configure("Subtitulo.TLabel", background="#f4f6f8", foreground="#4b5563", font=("Segoe UI", 10))
        self.estilo.configure("MenuTitulo.TLabel", background="#1f2937", foreground="white", font=("Segoe UI", 15, "bold"))
        self.estilo.configure("MenuTexto.TLabel", background="#1f2937", foreground="#cbd5e1", font=("Segoe UI", 9))
        self.estilo.configure("Menu.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 10))
        self.estilo.configure("Accent.TButton", font=("Segoe UI", 10, "bold"), padding=(12, 8))
        self.estilo.configure("TLabelframe", background="#f4f6f8", foreground="#111827")
        self.estilo.configure("TLabelframe.Label", background="#f4f6f8", foreground="#111827", font=("Segoe UI", 10, "bold"))
        self.estilo.configure("Treeview", rowheight=28, font=("Segoe UI", 10))
        self.estilo.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"))

        contenedor = ttk.Frame(self)
        contenedor.pack(fill=tk.BOTH, expand=True)

        self.menu = ttk.Frame(contenedor, width=245, padding=(18, 22), style="Menu.TFrame")
        self.menu.pack(side=tk.LEFT, fill=tk.Y)
        self.menu.pack_propagate(False)

        ttk.Label(self.menu, text="Esqui Olimpico", style="MenuTitulo.TLabel").pack(anchor="w")
        ttk.Label(
            self.menu,
            text="Panel principal del proyecto",
            style="MenuTexto.TLabel",
        ).pack(anchor="w", pady=(3, 24))

        self.botones_menu = {}
        opciones = (
            ("inicio", "Menu principal", self.mostrar_inicio),
            ("participantes", "Participantes", lambda: self.mostrar_modulo("participantes")),
            ("pruebas", "Pruebas", lambda: self.mostrar_modulo("pruebas")),
            ("pistas", "Pistas y estaciones", lambda: self.mostrar_modulo("pistas")),
            ("federaciones", "Federaciones y equipos", lambda: self.mostrar_modulo("federaciones")),
            ("procedimiento", "Procedimiento", self.mostrar_procedimiento),
        )
        for clave, texto, comando in opciones:
            boton = ttk.Button(self.menu, text=texto, style="Menu.TButton", command=comando)
            boton.pack(fill=tk.X, pady=5)
            self.botones_menu[clave] = boton

        ttk.Label(
            self.menu,
            text="Seleccione una opcion para trabajar sin perder de vista las funciones principales.",
            style="MenuTexto.TLabel",
            wraplength=195,
        ).pack(side=tk.BOTTOM, anchor="w", pady=(20, 0))

        self.contenido = ttk.Frame(contenedor, padding=24)
        self.contenido.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.paginas = {}
        for clave in ("inicio", "gestion", "lista", "modulo", "procedimiento"):
            pagina = ttk.Frame(self.contenido)
            pagina.grid(row=0, column=0, sticky="nsew")
            self.paginas[clave] = pagina

        self.contenido.columnconfigure(0, weight=1)
        self.contenido.rowconfigure(0, weight=1)

        self.crear_pagina_inicio()
        self.crear_pagina_gestion()
        self.crear_pagina_lista()
        self.crear_pagina_modulo()
        self.crear_pagina_procedimiento()

    def crear_encabezado(self, pagina, titulo, subtitulo):
        ttk.Label(pagina, text=titulo, style="Titulo.TLabel").pack(anchor="w")
        ttk.Label(pagina, text=subtitulo, style="Subtitulo.TLabel").pack(anchor="w", pady=(2, 18))

    def crear_pagina_inicio(self):
        pagina = self.paginas["inicio"]
        self.crear_encabezado(
            pagina,
            "Menu principal",
            "Acceda rapidamente a cada funcionalidad del sistema.",
        )

        tarjetas = ttk.Frame(pagina)
        tarjetas.pack(fill=tk.BOTH, expand=True)
        tarjetas.columnconfigure((0, 1), weight=1, uniform="tarjetas")
        tarjetas.rowconfigure((0, 1), weight=1, uniform="tarjetas")

        self.crear_tarjeta(
            tarjetas,
            0,
            0,
            "Participantes",
            "Gestionar esquiadores, participantes individuales, equipos participantes y jornadas.",
            "Abrir modulo",
            lambda: self.mostrar_modulo("participantes"),
        )
        self.crear_tarjeta(
            tarjetas,
            0,
            1,
            "Pruebas",
            "Gestionar pruebas, resultados, participaciones y pistas usadas.",
            "Abrir modulo",
            lambda: self.mostrar_modulo("pruebas"),
        )
        self.crear_tarjeta(
            tarjetas,
            1,
            0,
            "Pistas y estaciones",
            "Gestionar estaciones, pistas normales, pistas compuestas y administraciones.",
            "Abrir modulo",
            lambda: self.mostrar_modulo("pistas"),
        )
        self.crear_tarjeta(
            tarjetas,
            1,
            1,
            "Federaciones y equipos",
            "Gestionar federaciones, equipos, capitanes y composicion de equipos.",
            "Abrir modulo",
            lambda: self.mostrar_modulo("federaciones"),
        )

    def crear_tarjeta(self, padre, fila, columna, titulo, descripcion, texto_boton, comando):
        tarjeta = ttk.Frame(padre, padding=18, style="Card.TFrame")
        tarjeta.grid(row=fila, column=columna, sticky="nsew", padx=8, pady=8)
        ttk.Label(tarjeta, text=titulo, background="white", font=("Segoe UI", 13, "bold")).pack(anchor="w")
        ttk.Label(
            tarjeta,
            text=descripcion,
            background="white",
            foreground="#4b5563",
            wraplength=330,
            justify=tk.LEFT,
        ).pack(anchor="w", pady=(8, 20))
        ttk.Button(tarjeta, text=texto_boton, style="Accent.TButton", command=comando).pack(anchor="w")

    def crear_pagina_gestion(self):
        pagina = self.paginas["gestion"]
        self.crear_encabezado(
            pagina,
            "Gestionar esquiadores",
            "Complete el formulario para crear o actualizar un registro.",
        )

        formulario = ttk.LabelFrame(pagina, text="Datos del esquiador", padding=14)
        formulario.pack(fill=tk.X)
        formulario.columnconfigure(1, weight=1)
        formulario.columnconfigure(3, weight=1)

        ttk.Label(formulario, text="DNI").grid(row=0, column=0, sticky="w")
        self.txt_dni = ttk.Entry(formulario, width=25)
        self.txt_dni.grid(row=1, column=0, padx=(0, 12), pady=6, sticky="ew")

        ttk.Label(formulario, text="Nombre").grid(row=0, column=1, sticky="w")
        self.txt_nombre = ttk.Entry(formulario, width=35)
        self.txt_nombre.grid(row=1, column=1, padx=(0, 12), pady=6, sticky="ew")

        ttk.Label(formulario, text="Edad").grid(row=0, column=2, sticky="w")
        self.txt_edad = ttk.Entry(formulario, width=15)
        self.txt_edad.grid(row=1, column=2, padx=(0, 12), pady=6, sticky="ew")

        ttk.Label(formulario, text="Federacion").grid(row=0, column=3, sticky="w")
        self.cbo_federacion = ttk.Combobox(formulario, width=35, state="readonly")
        self.cbo_federacion.grid(row=1, column=3, pady=6, sticky="ew")

        botones = ttk.Frame(pagina)
        botones.pack(fill=tk.X, pady=14)

        ttk.Button(botones, text="Nuevo", command=self.limpiar).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(botones, text="Guardar", style="Accent.TButton", command=self.guardar).pack(side=tk.LEFT, padx=(0, 8))

        ayuda = ttk.LabelFrame(pagina, text="Uso rapido", padding=14)
        ayuda.pack(fill=tk.X, pady=(4, 0))
        ttk.Label(
            ayuda,
            text="Para editar, abra Consultar lista, seleccione un esquiador y vuelva a esta pantalla con los datos cargados.",
            wraplength=780,
        ).pack(anchor="w")

    def crear_pagina_lista(self):
        pagina = self.paginas["lista"]
        self.crear_encabezado(
            pagina,
            "Consultar lista",
            "Seleccione un registro para editarlo o actualice la tabla cuando lo necesite.",
        )

        acciones = ttk.Frame(pagina)
        acciones.pack(fill=tk.X, pady=(0, 10))
        ttk.Button(acciones, text="Actualizar tabla", command=self.cargar_esquiadores).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(acciones, text="Editar seleccionado", style="Accent.TButton", command=self.editar_seleccionado).pack(side=tk.LEFT, padx=(0, 8))
        ttk.Button(acciones, text="Nuevo esquiador", command=self.nuevo_desde_inicio).pack(side=tk.LEFT, padx=(0, 8))

        tabla_marco = ttk.LabelFrame(pagina, text="Lista de esquiadores", padding=10)
        tabla_marco.pack(fill=tk.BOTH, expand=True)

        columnas = ("DNI", "Nombre", "Edad", "ID_Federacion", "Federacion")
        self.tabla = ttk.Treeview(tabla_marco, columns=columnas, show="headings")
        for col in columnas:
            self.tabla.heading(col, text=col)
            self.tabla.column(col, width=150)
        self.tabla.column("Nombre", width=230)
        self.tabla.column("Federacion", width=230)

        scroll_y = ttk.Scrollbar(tabla_marco, orient=tk.VERTICAL, command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scroll_y.set)
        self.tabla.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scroll_y.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def crear_pagina_modulo(self):
        pagina = self.paginas["modulo"]
        self.lbl_modulo_titulo = ttk.Label(pagina, text="", style="Titulo.TLabel")
        self.lbl_modulo_titulo.pack(anchor="w")
        self.lbl_modulo_subtitulo = ttk.Label(pagina, text="", style="Subtitulo.TLabel")
        self.lbl_modulo_subtitulo.pack(anchor="w", pady=(2, 18))

        selector = ttk.Frame(pagina)
        selector.pack(fill=tk.X, pady=(0, 10))
        ttk.Label(selector, text="Gestionar").pack(side=tk.LEFT, padx=(0, 8))
        self.cbo_tablas = ttk.Combobox(selector, state="readonly", width=34)
        self.cbo_tablas["values"] = MODULOS_GESTION[self.modulo_actual]["tablas"]
        self.cbo_tablas.set(self.tabla_actual)
        self.cbo_tablas.pack(side=tk.LEFT, padx=(0, 8))
        self.cbo_tablas.bind("<<ComboboxSelected>>", self.cambiar_tabla_generica)
        ttk.Button(selector, text="Actualizar", command=self.cargar_tabla_generica).pack(side=tk.LEFT, padx=(0, 8))
        self.btn_nuevo_generico = ttk.Button(selector, text="Nuevo", command=self.nuevo_generico)
        self.btn_nuevo_generico.pack(side=tk.LEFT, padx=(0, 8))
        self.btn_guardar_generico = ttk.Button(selector, text="Guardar nuevo", style="Accent.TButton", command=self.guardar_generico)
        self.btn_guardar_generico.pack(side=tk.LEFT, padx=(0, 8))
        self.lbl_modo_generico = ttk.Label(selector, text="Modo: nuevo")
        self.lbl_modo_generico.pack(side=tk.LEFT, padx=(8, 0))

        cuerpo = ttk.Frame(pagina)
        cuerpo.pack(fill=tk.BOTH, expand=True)
        cuerpo.columnconfigure(0, weight=3,minsize=0)
        cuerpo.columnconfigure(1, weight=2, minsize=280)
        cuerpo.rowconfigure(0, weight=1)

        tabla_marco = ttk.LabelFrame(cuerpo, text="Registros", padding=10)
        tabla_marco.grid(row=0, column=0, sticky="nsew", padx=(0, 10))
        self.tabla_generica = ttk.Treeview(tabla_marco, show="headings")
        scroll_y = ttk.Scrollbar(tabla_marco, orient=tk.VERTICAL, command=self.tabla_generica.yview)
        scroll_x = ttk.Scrollbar(tabla_marco, orient=tk.HORIZONTAL, command=self.tabla_generica.xview)
        self.tabla_generica.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla_generica.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        tabla_marco.columnconfigure(0, weight=1)
        tabla_marco.rowconfigure(0, weight=1)
        self.tabla_generica.bind("<<TreeviewSelect>>", self.seleccionar_generico)

        self.formulario_generico = ttk.LabelFrame(cuerpo, text="Formulario", padding=12)
        self.formulario_generico.grid(row=0, column=1, sticky="nsew")
        self.formulario_generico.columnconfigure(0, weight=1)

        self.ayuda_generica = ttk.Label(
            self.formulario_generico,
            text="Use los ID existentes para campos relacionados. Ejemplo: ID_Federacion debe existir en federaciones.",
            wraplength=310,
            foreground="#4b5563",
        )
        self.ayuda_generica.grid(row=99, column=0, sticky="ew", pady=(14, 0))

        self.construir_formulario_generico()

    def crear_pagina_procedimiento(self):
        pagina = self.paginas["procedimiento"]
        self.crear_encabezado(
            pagina,
            "Procedimiento almacenado",
            "Ejecute el recalculo de tiempo ganador desde una pantalla dedicada.",
        )

        panel = ttk.Frame(pagina, padding=22, style="Card.TFrame")
        panel.pack(fill=tk.X)
        ttk.Label(
            panel,
            text="Recalcular tiempo ganador",
            background="white",
            font=("Segoe UI", 14, "bold"),
        ).pack(anchor="w")
        ttk.Label(
            panel,
            text="Esta accion compara el ganador guardado con el menor tiempo calculado y muestra el antes y despues.",
            background="white",
            foreground="#4b5563",
            wraplength=760,
            justify=tk.LEFT,
        ).pack(anchor="w", pady=(8, 20))
        ttk.Button(
            panel,
            text="Ejecutar procedimiento",
            style="Accent.TButton",
            command=self.ejecutar_procedimiento,
        ).pack(anchor="w")

        self.lbl_procedimiento_resumen = ttk.Label(
            pagina,
            text="Ejecute el procedimiento para ver aqui los cambios.",
            style="Subtitulo.TLabel",
        )
        self.lbl_procedimiento_resumen.pack(anchor="w", pady=(16, 8))

        resultado_marco = ttk.LabelFrame(pagina, text="Resultado del recalculo", padding=10)
        resultado_marco.pack(fill=tk.BOTH, expand=True)
        self.tabla_procedimiento = ttk.Treeview(resultado_marco, show="headings")
        scroll_y = ttk.Scrollbar(resultado_marco, orient=tk.VERTICAL, command=self.tabla_procedimiento.yview)
        scroll_x = ttk.Scrollbar(resultado_marco, orient=tk.HORIZONTAL, command=self.tabla_procedimiento.xview)
        self.tabla_procedimiento.configure(yscrollcommand=scroll_y.set, xscrollcommand=scroll_x.set)
        self.tabla_procedimiento.grid(row=0, column=0, sticky="nsew")
        scroll_y.grid(row=0, column=1, sticky="ns")
        scroll_x.grid(row=1, column=0, sticky="ew")
        resultado_marco.columnconfigure(0, weight=1)
        resultado_marco.rowconfigure(0, weight=1)

    def mostrar_pantalla(self, clave):
        self.pantalla_actual = clave
        self.paginas[clave].tkraise()

    def mostrar_inicio(self):
        self.mostrar_pantalla("inicio")

    def mostrar_gestion(self):
        self.mostrar_pantalla("gestion")

    def mostrar_lista(self):
        self.cargar_esquiadores()
        self.mostrar_pantalla("lista")

    def mostrar_modulo(self, modulo):
        self.modulo_actual = modulo
        config = MODULOS_GESTION[modulo]
        self.tabla_actual = config["tabla_inicial"]
        if hasattr(self, "lbl_modulo_titulo"):
            self.lbl_modulo_titulo.configure(text=config["titulo"])
            self.lbl_modulo_subtitulo.configure(text=config["subtitulo"])
            self.cbo_tablas["values"] = config["tablas"]
            self.cbo_tablas.set(self.tabla_actual)
            self.registro_generico_seleccionado = None
            self.actualizar_modo_generico("nuevo")
            self.construir_formulario_generico()
        self.cargar_tabla_generica()
        self.mostrar_pantalla("modulo")

    def mostrar_procedimiento(self):
        self.mostrar_pantalla("procedimiento")

    def nuevo_desde_inicio(self):
        self.limpiar()
        self.mostrar_gestion()

    def editar_seleccionado(self):
        if not self.tabla.selection():
            messagebox.showwarning("Aviso", "Seleccione un esquiador de la tabla")
            return
        self.seleccionar(None)
        self.mostrar_gestion()

    def config_tabla_actual(self):
        return TABLAS_GESTION[self.tabla_actual]

    def cambiar_tabla_generica(self, evento=None):
        self.tabla_actual = self.cbo_tablas.get()
        self.registro_generico_seleccionado = None
        self.modo_generico = "nuevo"
        self.construir_formulario_generico()
        self.cargar_tabla_generica()

    def actualizar_modo_generico(self, modo):
        self.modo_generico = modo
        config = self.config_tabla_actual()
        solo_lectura = config.get("readonly", False)
        solo_edicion = config.get("insert_disabled", False)
        if hasattr(self, "lbl_modo_generico"):
            if solo_lectura:
                texto = "Modo: solo lectura"
            elif modo == "nuevo" and solo_edicion:
                texto = "Modo: edicion solamente"
            else:
                texto = "Modo: nuevo" if modo == "nuevo" else "Modo: edicion"
            self.lbl_modo_generico.configure(text=texto)
        if hasattr(self, "btn_nuevo_generico"):
            self.btn_nuevo_generico.configure(state="disabled" if solo_lectura or solo_edicion else "normal")
        if hasattr(self, "btn_guardar_generico"):
            texto = "Guardar nuevo" if modo == "nuevo" else "Guardar cambios"
            guardar_bloqueado = solo_lectura or (modo == "nuevo" and solo_edicion)
            self.btn_guardar_generico.configure(
                text=texto,
                state="disabled" if guardar_bloqueado else "normal",
            )

    def construir_formulario_generico(self):
        for widget in self.formulario_generico.grid_slaves():
            if int(widget.grid_info()["row"]) != 99:
                widget.destroy()

        self.campos_genericos = {}
        config = self.config_tabla_actual()

        if hasattr(self, "ayuda_generica"):
            self.ayuda_generica.configure(
                text=config.get(
                    "help",
                    "Use los ID existentes para campos relacionados. Las reglas de negocio se validan antes de guardar.",
                ),
            )

        if config.get("readonly", False):
            ttk.Label(
                self.formulario_generico,
                text=config.get("readonly_reason", "Esta tabla se consulta en solo lectura."),
                wraplength=310,
                foreground="#4b5563",
            ).grid(row=0, column=0, sticky="ew", pady=(0, 8))
            self.actualizar_modo_generico("solo lectura")
            return

        for fila, (columna, etiqueta, tipo) in enumerate(config["columnas"]):
            ttk.Label(self.formulario_generico, text=etiqueta).grid(row=fila * 2, column=0, sticky="w", pady=(0, 2))
            entrada = ttk.Entry(self.formulario_generico)
            entrada.grid(row=(fila * 2) + 1, column=0, sticky="ew", pady=(0, 8))
            self.campos_genericos[columna] = entrada

        self.limpiar_generico()

    def columnas_actuales(self):
        return [columna for columna, _, _ in self.config_tabla_actual()["columnas"]]

    def cargar_tabla_generica(self):
        if not hasattr(self, "tabla_generica"):
            return

        config = self.config_tabla_actual()
        columnas = self.columnas_actuales()
        self.tabla_generica.delete(*self.tabla_generica.get_children())
        self.tabla_generica["columns"] = columnas

        for columna, etiqueta, _ in config["columnas"]:
            self.tabla_generica.heading(columna, text=etiqueta)
            self.tabla_generica.column(columna, width=135, minwidth=95, stretch=False)

        select_cols = ", ".join(q(col) for col in columnas)
        order_cols = ", ".join(q(col) for col in config["order"])
        sql = f"SELECT {select_cols} FROM {q(config['tabla'])} ORDER BY {order_cols}"

        try:
            with conectar() as conn:
                filas = conn.cursor().execute(sql).fetchall()

            for fila in filas:
                valores = []
                for valor in fila:
                    valores.append("" if valor is None else str(valor))
                self.tabla_generica.insert("", tk.END, values=valores)
        except Exception as e:
            self.mostrar_error(e)

    def limpiar_generico(self):
        self.registro_generico_seleccionado = None
        self.actualizar_modo_generico("nuevo")
        config = self.config_tabla_actual()
        solo_edicion = config.get("insert_disabled", False)
        campos_bloqueados = set(config["identity"]) | set(config.get("readonly_fields", []))

        for columna, entrada in self.campos_genericos.items():
            entrada.configure(state="normal")
            entrada.delete(0, tk.END)
            if solo_edicion or columna in campos_bloqueados:
                entrada.configure(state="disabled")

        if hasattr(self, "tabla_generica"):
            seleccion = self.tabla_generica.selection()
            if seleccion:
                self.tabla_generica.selection_remove(*seleccion)
            self.tabla_generica.focus("")

    def nuevo_generico(self):
        config = self.config_tabla_actual()
        if config.get("readonly", False):
            messagebox.showinfo("Solo lectura", "Esta tabla no se registra manualmente desde la aplicacion.")
            return
        if config.get("insert_disabled", False):
            messagebox.showinfo("Edicion solamente", config.get("insert_disabled_reason", "Esta tabla solo permite editar registros existentes."))
            return
        self.limpiar_generico()
        for columna, entrada in self.campos_genericos.items():
            if columna not in config["identity"] and columna not in config.get("readonly_fields", []):
                entrada.focus_set()
                break

    def seleccionar_generico(self, evento=None):
        seleccion = self.tabla_generica.selection()
        if not seleccion:
            return

        config = self.config_tabla_actual()
        valores = self.tabla_generica.item(seleccion[0], "values")
        columnas = self.columnas_actuales()
        datos = dict(zip(columnas, valores))
        self.registro_generico_seleccionado = {pk: datos[pk] for pk in config["pk"]}
        self.actualizar_modo_generico("editar")
        campos_bloqueados = set(config["identity"]) | set(config["pk"]) | set(config.get("readonly_fields", []))

        for columna, entrada in self.campos_genericos.items():
            entrada.configure(state="normal")
            entrada.delete(0, tk.END)
            entrada.insert(0, datos.get(columna, ""))
            if columna in campos_bloqueados:
                entrada.configure(state="disabled")

    def mensaje_error_usuario(self, error):
        texto = " ".join(str(error).replace("\r", " ").replace("\n", " ").split())

        for mensaje in MENSAJES_NEGOCIO:
            if mensaje in texto:
                return mensaje

        for restriccion, mensaje in REGLAS_SQL.items():
            if restriccion in texto:
                return mensaje

        if "PRIMARY KEY constraint" in texto or "UNIQUE KEY constraint" in texto:
            duplicado = re.search(r"The duplicate key value is \\((.*?)\\)", texto)
            detalle = f" Valor repetido: {duplicado.group(1)}." if duplicado else ""
            return f"Ya existe un registro con la misma clave o valor unico.{detalle}"

        if "FOREIGN KEY constraint" in texto or "REFERENCE constraint" in texto:
            return "El registro usa un ID relacionado que no existe, o intenta eliminar un dato que ya esta siendo usado por otra tabla."

        if "CHECK constraint" in texto:
            return "El valor ingresado no cumple una regla de validacion. Revise que numeros sean positivos, dificultad sea Azul/Verde/Roja/Negra y fechas sean coherentes."

        if "Conversion failed" in texto or "converting" in texto:
            return "Hay un valor con formato incorrecto. Revise numeros enteros, decimales y fechas con formato AAAA-MM-DD."

        if "Login timeout" in texto or "SQL Server" in texto and "connection" in texto.lower():
            return "No se pudo conectar con SQL Server. Verifique que SQLEXPRESS este iniciado y que la base esqui_olimpico exista."

        return f"No se pudo completar la operacion. Detalle: {texto}"

    def mostrar_error(self, error):
        messagebox.showerror("Error", self.mensaje_error_usuario(error))

    def validar_valores_basicos(self, valores):
        if "num_Federados" in valores and valores["num_Federados"] < 0:
            raise ValueError("Num. federados no puede ser negativo.")
        if "Edad" in valores and valores["Edad"] <= 0:
            raise ValueError("Edad debe ser mayor que cero.")
        if "Km_Esquiables" in valores and valores["Km_Esquiables"] <= 0:
            raise ValueError("Km esquiables debe ser mayor que cero.")
        if "kilometros" in valores and valores["kilometros"] <= 0:
            raise ValueError("Kilometros debe ser mayor que cero.")
        if "Tiempo_Ganador" in valores and valores["Tiempo_Ganador"] <= 0:
            raise ValueError("Tiempo ganador debe ser mayor que cero.")
        if "TiempoParcial" in valores and valores["TiempoParcial"] <= 0:
            raise ValueError("Tiempo parcial debe ser mayor que cero.")
        if "TiempoEmpleado" in valores and valores["TiempoEmpleado"] <= 0:
            raise ValueError("Tiempo empleado debe ser mayor que cero.")
        if "Numero_Secuencial" in valores and valores["Numero_Secuencial"] <= 0:
            raise ValueError("Num. secuencial debe ser mayor que cero.")
        if "Posicion" in valores and valores["Posicion"] <= 0:
            raise ValueError("Posicion debe ser mayor que cero.")
        if "GradoDificultas" in valores and valores["GradoDificultas"] not in ("Azul", "Verde", "Roja", "Negra"):
            raise ValueError("Dificultad debe ser Azul, Verde, Roja o Negra.")
        if "Fecha_inicio_Prevista" in valores and "fecha_fin_Previsra" in valores:
            if valores["Fecha_inicio_Prevista"] > valores["fecha_fin_Previsra"]:
                raise ValueError("Fecha inicio no puede ser posterior a Fecha fin.")

    def convertir_valor(self, valor, tipo, etiqueta):
        valor = valor.strip()
        if valor == "":
            raise ValueError(f"El campo {etiqueta} no puede estar vacio")
        if tipo == "int":
            try:
                return int(valor)
            except ValueError as exc:
                raise ValueError(f"El campo {etiqueta} debe ser un numero entero.") from exc
        if tipo in ("float", "decimal"):
            try:
                return float(valor)
            except ValueError as exc:
                raise ValueError(f"El campo {etiqueta} debe ser un numero valido.") from exc
        if tipo == "date":
            try:
                return date.fromisoformat(valor)
            except ValueError as exc:
                raise ValueError(f"El campo {etiqueta} debe tener formato AAAA-MM-DD.") from exc
        return valor

    def valores_formulario_generico(self, incluir_pk=False):
        config = self.config_tabla_actual()
        valores = {}

        for columna, etiqueta, tipo in config["columnas"]:
            if columna in config["identity"]:
                continue
            if columna in config.get("readonly_fields", []):
                continue
            if not incluir_pk and self.registro_generico_seleccionado is not None and columna in config["pk"]:
                continue

            entrada = self.campos_genericos[columna]
            valores[columna] = self.convertir_valor(entrada.get(), tipo, etiqueta)

        return valores

    def validar_reglas_negocio(self, cursor, valores):
        self.validar_valores_basicos(valores)
        tabla = self.tabla_actual

        if tabla == "Equipos":
            equipo = valores.get("Id_Equipo")
            capitan = valores["DniCapitan"]
            if cursor.execute("SELECT 1 FROM Esquiadores WHERE DNI = ?", capitan).fetchone() is None:
                raise ValueError("El DNI del capitan no existe en Esquiadores.")
            if cursor.execute("SELECT 1 FROM [Participante indivi] WHERE DNI = ?", capitan).fetchone():
                raise ValueError("El capitan no puede estar registrado como participante individual.")
            fila = cursor.execute("SELECT ID_Equipo FROM Pertenece_Equipos WHERE DNI = ?", capitan).fetchone()
            if fila is not None and (equipo is None or int(fila.ID_Equipo) != int(equipo)):
                raise ValueError("El capitan ya pertenece a otro equipo.")

        elif tabla == "Participante individual":
            participante = valores["Id_participantes"]
            dni = valores["DNI"]
            fila = cursor.execute(
                "SELECT Tipo FROM Participantes WHERE Id_participantes = ?",
                participante,
            ).fetchone()
            if fila is None or fila.Tipo != "INDIVIDUAL":
                raise ValueError("El ID participante debe existir en Participantes con Tipo = INDIVIDUAL")
            if cursor.execute("SELECT 1 FROM Pertenece_Equipos WHERE DNI = ?", dni).fetchone():
                raise ValueError("Ese DNI ya pertenece a un equipo y no puede actuar como individual")

        elif tabla == "Participante equipo":
            participante = valores["Id_participantes"]
            fila = cursor.execute(
                "SELECT Tipo FROM Participantes WHERE Id_participantes = ?",
                participante,
            ).fetchone()
            if fila is None or fila.Tipo != "EQUIPO":
                raise ValueError("El ID participante debe existir en Participantes con Tipo = EQUIPO")

        elif tabla == "Pertenece a equipos":
            dni = valores["DNI"]
            if cursor.execute("SELECT 1 FROM [Participante indivi] WHERE DNI = ?", dni).fetchone():
                raise ValueError("Ese esquiador ya participa a titulo individual y no puede pertenecer a un equipo")

        elif tabla == "Participacion":
            participante = valores["Id_participante"]
            prueba = valores["IdPrueba"]
            numero = valores["Numero_Secuencial"]
            if cursor.execute(
                """
                SELECT 1
                FROM Participacion
                WHERE IdPrueba = ?
                  AND Numero_Secuencial = ?
                  AND Id_participante <> ?
                """,
                prueba,
                numero,
                participante,
            ).fetchone():
                raise ValueError("El numero secuencial ya esta usado por otro participante en esa prueba")

        elif tabla == "Jornadas":
            participante = valores["Id_participante"]
            if cursor.execute(
                "SELECT 1 FROM [Participante indivi] WHERE Id_participantes = ?",
                participante,
            ).fetchone() is None:
                raise ValueError("Las jornadas solo aceptan participantes individuales")

        elif tabla == "Intervenciones":
            dni = valores["DNI"]
            prueba = valores["IdTPrueba"]
            participante = valores["Id_participantes"]
            if cursor.execute(
                """
                SELECT 1
                FROM ParticipanteEqupo pte
                INNER JOIN Pertenece_Equipos pe ON pe.ID_Equipo = pte.Id_Equipo
                WHERE pte.Id_participantes = ?
                  AND pe.DNI = ?
                """,
                participante,
                dni,
            ).fetchone() is None:
                raise ValueError("El DNI debe pertenecer al equipo asociado a ese participante")
            if cursor.execute(
                """
                SELECT 1
                FROM Participacion
                WHERE Id_participante = ?
                  AND IdPrueba = ?
                """,
                participante,
                prueba,
            ).fetchone() is None:
                raise ValueError("El equipo debe estar registrado en Participacion para esa prueba")

        elif tabla == "Pruebas por pistas":
            prueba = valores["ID_Prueba"]
            estacion = valores["Codigo_Estacion"]
            fila = cursor.execute(
                "SELECT Codigo_Estacion FROM Pruebas WHERE IdTPrueba = ?",
                prueba,
            ).fetchone()
            if fila is None or int(fila.Codigo_Estacion) != int(estacion):
                raise ValueError("La pista debe pertenecer a la misma estacion de la prueba")

        elif tabla == "Pista compuesta":
            estacion = valores["Codigo_Estacion"]
            compuesta = valores["Pista_Compuesta"]
            componente = valores["Pista_Componente"]
            if int(compuesta) == int(componente):
                raise ValueError("Una pista compuesta no puede componerse de si misma")
            for pista, etiqueta in ((compuesta, "compuesta"), (componente, "componente")):
                if cursor.execute(
                    """
                    SELECT 1
                    FROM Pistas
                    WHERE [Num secuanecial] = ?
                      AND Codigo_Estacion = ?
                    """,
                    pista,
                    estacion,
                ).fetchone() is None:
                    raise ValueError(f"La pista {etiqueta} debe existir en la misma estacion")

    def guardar_generico(self):
        config = self.config_tabla_actual()
        if config.get("readonly", False):
            messagebox.showinfo("Solo lectura", "Esta tabla no se modifica manualmente desde la aplicacion.")
            return
        if self.modo_generico == "nuevo" and config.get("insert_disabled", False):
            messagebox.showinfo("Edicion solamente", config.get("insert_disabled_reason", "Esta tabla solo permite editar registros existentes."))
            return

        try:
            with conectar() as conn:
                cursor = conn.cursor()

                if self.modo_generico == "nuevo":
                    valores = self.valores_formulario_generico(incluir_pk=True)
                    if config.get("auto_participante_tipo"):
                        cursor.execute(
                            "INSERT INTO Participantes (Tipo) OUTPUT INSERTED.Id_participantes VALUES (?)",
                            config["auto_participante_tipo"],
                        )
                        valores["Id_participantes"] = int(cursor.fetchone()[0])
                    self.validar_reglas_negocio(cursor, valores)
                    columnas = list(valores.keys())
                    parametros = ", ".join("?" for _ in columnas)
                    sql = f"INSERT INTO {q(config['tabla'])} ({', '.join(q(c) for c in columnas)}) VALUES ({parametros})"
                    cursor.execute(sql, [valores[c] for c in columnas])
                    mensaje = "Registro insertado correctamente"
                else:
                    if self.registro_generico_seleccionado is None:
                        messagebox.showwarning("Aviso", "Seleccione un registro para actualizar o presione Nuevo")
                        return
                    valores = self.valores_formulario_generico(incluir_pk=False)
                    if not valores:
                        messagebox.showwarning("Aviso", "No hay campos editables para actualizar")
                        return
                    datos_completos = {**self.registro_generico_seleccionado, **valores}
                    self.validar_reglas_negocio(cursor, datos_completos)
                    sets = ", ".join(f"{q(c)} = ?" for c in valores)
                    where = " AND ".join(f"{q(pk)} = ?" for pk in config["pk"])
                    sql = f"UPDATE {q(config['tabla'])} SET {sets} WHERE {where}"
                    params = [valores[c] for c in valores] + [self.registro_generico_seleccionado[pk] for pk in config["pk"]]
                    cursor.execute(sql, params)
                    mensaje = "Registro actualizado correctamente"

                conn.commit()

            messagebox.showinfo("Correcto", mensaje)
            self.cargar_tabla_generica()
            self.limpiar_generico()
            self.cargar_federaciones()
            self.cargar_esquiadores()
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            self.mostrar_error(e)

    def eliminar_generico(self):
        config = self.config_tabla_actual()
        if self.registro_generico_seleccionado is None:
            messagebox.showwarning("Aviso", "Seleccione un registro para eliminar")
            return

        confirmado = messagebox.askyesno(
            "Confirmar eliminacion",
            "Esta accion eliminara el registro seleccionado. Si tiene datos relacionados, SQL Server puede impedirlo.",
        )
        if not confirmado:
            return

        try:
            where = " AND ".join(f"{q(pk)} = ?" for pk in config["pk"])
            sql = f"DELETE FROM {q(config['tabla'])} WHERE {where}"
            params = [self.registro_generico_seleccionado[pk] for pk in config["pk"]]

            with conectar() as conn:
                conn.cursor().execute(sql, params)
                conn.commit()

            messagebox.showinfo("Correcto", "Registro eliminado correctamente")
            self.cargar_tabla_generica()
            self.limpiar_generico()
            self.cargar_federaciones()
            self.cargar_esquiadores()
        except Exception as e:
            self.mostrar_error(e)

    def cargar_federaciones(self):
        try:
            with conectar() as conn:
                filas = conn.cursor().execute(
                    "SELECT Id_Federacion, Nombre FROM federaciones ORDER BY Id_Federacion"
                ).fetchall()
            self.federaciones = {f"{f.Id_Federacion} - {f.Nombre}": f.Id_Federacion for f in filas}
            self.cbo_federacion["values"] = list(self.federaciones.keys())
            if filas:
                self.cbo_federacion.current(0)
        except Exception as e:
            self.mostrar_error(e)

    def cargar_esquiadores(self):
        try:
            with conectar() as conn:
                filas = conn.cursor().execute("""
                    SELECT e.DNI, e.Nombre, e.Edad, e.ID_Federacion, f.Nombre AS Federacion
                    FROM Esquiadores e
                    INNER JOIN federaciones f ON e.ID_Federacion = f.Id_Federacion
                    ORDER BY e.DNI
                """).fetchall()

            self.tabla.delete(*self.tabla.get_children())
            for f in filas:
                self.tabla.insert("", tk.END, values=(f.DNI, f.Nombre, f.Edad, f.ID_Federacion, f.Federacion))
        except Exception as e:
            self.mostrar_error(e)

    def limpiar(self):
        self.dni_seleccionado = None
        self.txt_dni.delete(0, tk.END)
        self.txt_nombre.delete(0, tk.END)
        self.txt_edad.delete(0, tk.END)
        if self.cbo_federacion["values"]:
            self.cbo_federacion.current(0)

    def seleccionar(self, evento):
        item = self.tabla.selection()
        if not item:
            return
        datos = self.tabla.item(item[0], "values")
        self.dni_seleccionado = int(datos[0])
        self.txt_dni.delete(0, tk.END)
        self.txt_dni.insert(0, datos[0])
        self.txt_nombre.delete(0, tk.END)
        self.txt_nombre.insert(0, datos[1])
        self.txt_edad.delete(0, tk.END)
        self.txt_edad.insert(0, datos[2])
        for texto, id_fed in self.federaciones.items():
            if id_fed == int(datos[3]):
                self.cbo_federacion.set(texto)
                break

    def guardar(self):
        try:
            dni = self.convertir_valor(self.txt_dni.get(), "int", "DNI")
            nombre = self.txt_nombre.get().strip()
            edad = self.convertir_valor(self.txt_edad.get(), "int", "Edad")
            self.validar_valores_basicos({"Edad": edad})
            if self.cbo_federacion.get() not in self.federaciones:
                messagebox.showwarning("Aviso", "Seleccione una federacion valida.")
                return
            id_federacion = self.federaciones[self.cbo_federacion.get()]

            if nombre == "":
                messagebox.showwarning("Aviso", "El nombre no puede estar vacio")
                return

            with conectar() as conn:
                cursor = conn.cursor()
                if self.dni_seleccionado is None:
                    cursor.execute(
                        "INSERT INTO Esquiadores (DNI, Nombre, Edad, ID_Federacion) VALUES (?, ?, ?, ?)",
                        dni, nombre, edad, id_federacion
                    )
                    mensaje = "Esquiador insertado"
                else:
                    cursor.execute(
                        "UPDATE Esquiadores SET Nombre=?, Edad=?, ID_Federacion=? WHERE DNI=?",
                        nombre, edad, id_federacion, self.dni_seleccionado
                    )
                    mensaje = "Esquiador actualizado"
                conn.commit()

            messagebox.showinfo("Correcto", mensaje)
            self.cargar_esquiadores()
            self.limpiar()
        except ValueError as e:
            messagebox.showwarning("Aviso", str(e))
        except Exception as e:
            self.mostrar_error(e)

    def ejecutar_procedimiento(self):
        try:
            with conectar() as conn:
                cursor = conn.cursor()
                cursor.execute("EXEC sp_Recalcular_Tiempo_Ganador")
                filas = cursor.fetchall()
                columnas = [columna[0] for columna in cursor.description] if cursor.description else []
                conn.commit()

            self.tabla_procedimiento.delete(*self.tabla_procedimiento.get_children())
            self.tabla_procedimiento["columns"] = columnas

            anchos = {
                "IdPrueba": 80,
                "Prueba": 260,
                "Ganador_Anterior": 130,
                "Tiempo_Anterior": 130,
                "Ganador_Calculado": 140,
                "Tiempo_Calculado": 140,
                "Estado": 110,
                "PruebasProcesadas": 140,
            }
            for columna in columnas:
                self.tabla_procedimiento.heading(columna, text=columna)
                self.tabla_procedimiento.column(
                    columna,
                    width=anchos.get(columna, 130),
                    minwidth=80,
                    stretch=columna == "Prueba",
                )

            actualizados = 0
            procesadas = 0
            for fila in filas:
                datos = dict(zip(columnas, fila))
                if datos.get("Estado") == "Actualizado":
                    actualizados += 1
                if "PruebasProcesadas" in datos:
                    procesadas = datos["PruebasProcesadas"]
                self.tabla_procedimiento.insert(
                    "",
                    tk.END,
                    values=["" if valor is None else str(valor) for valor in fila],
                )

            self.lbl_procedimiento_resumen.configure(
                text=f"Pruebas procesadas: {procesadas}. Cambios realizados: {actualizados}."
            )
            self.cargar_esquiadores()
            messagebox.showinfo(
                "Procedimiento",
                "Recalculo terminado. Revise la tabla de resultados para ver el antes y despues.",
            )
        except Exception as e:
            self.mostrar_error(e)


if __name__ == "__main__":
    app = AppEsquiadores()
    app.mainloop()

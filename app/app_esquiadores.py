import tkinter as tk
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
        "pk": ["PistasCodigo_Estacion", "Pista_1", "Pista_2"],
        "identity": [],
        "order": ["PistasCodigo_Estacion", "Pista_1", "Pista_2"],
        "columnas": [
            ("PistasCodigo_Estacion", "Codigo estacion", "int"),
            ("Pista_1", "Pista 1", "int"),
            ("Pista_2", "Pista 2", "int"),
        ],
    },
    "Pruebas": {
        "tabla": "Pruebas",
        "pk": ["IdTPrueba"],
        "identity": ["IdTPrueba"],
        "order": ["IdTPrueba"],
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
        "identity": [],
        "order": ["Id_participantes"],
        "columnas": [
            ("Id_participantes", "ID participante", "int"),
            ("DNI", "DNI", "int"),
        ],
    },
    "Participante equipo": {
        "tabla": "ParticipanteEqupo",
        "pk": ["Id_participantes"],
        "identity": [],
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
        ttk.Button(selector, text="Nuevo", command=self.nuevo_generico).pack(side=tk.LEFT, padx=(0, 8))
        self.btn_guardar_generico = ttk.Button(selector, text="Guardar nuevo", style="Accent.TButton", command=self.guardar_generico)
        self.btn_guardar_generico.pack(side=tk.LEFT, padx=(0, 8))
        self.lbl_modo_generico = ttk.Label(selector, text="Modo: nuevo")
        self.lbl_modo_generico.pack(side=tk.LEFT, padx=(8, 0))

        cuerpo = ttk.Frame(pagina)
        cuerpo.pack(fill=tk.BOTH, expand=True)
        cuerpo.columnconfigure(0, weight=3)
        cuerpo.columnconfigure(1, weight=2)
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

        ayuda = ttk.Label(
            self.formulario_generico,
            text="Use los ID existentes para campos relacionados. Ejemplo: ID_Federacion debe existir en federaciones.",
            wraplength=310,
            foreground="#4b5563",
        )
        ayuda.grid(row=99, column=0, sticky="ew", pady=(14, 0))

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
            text="Esta accion ejecuta sp_Recalcular_Tiempo_Ganador y muestra cuantas pruebas fueron procesadas.",
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
        if hasattr(self, "lbl_modo_generico"):
            texto = "Modo: nuevo" if modo == "nuevo" else "Modo: edicion"
            self.lbl_modo_generico.configure(text=texto)
        if hasattr(self, "btn_guardar_generico"):
            texto = "Guardar nuevo" if modo == "nuevo" else "Guardar cambios"
            self.btn_guardar_generico.configure(text=texto)

    def construir_formulario_generico(self):
        for widget in self.formulario_generico.grid_slaves():
            if int(widget.grid_info()["row"]) != 99:
                widget.destroy()

        self.campos_genericos = {}
        config = self.config_tabla_actual()

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
            self.tabla_generica.column(columna, width=135, minwidth=95)

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
            messagebox.showerror("Error", str(e))

    def limpiar_generico(self):
        self.registro_generico_seleccionado = None
        self.actualizar_modo_generico("nuevo")
        config = self.config_tabla_actual()

        for columna, entrada in self.campos_genericos.items():
            entrada.configure(state="normal")
            entrada.delete(0, tk.END)
            if columna in config["identity"]:
                entrada.configure(state="disabled")

        if hasattr(self, "tabla_generica"):
            seleccion = self.tabla_generica.selection()
            if seleccion:
                self.tabla_generica.selection_remove(*seleccion)
            self.tabla_generica.focus("")

    def nuevo_generico(self):
        self.limpiar_generico()
        for columna, entrada in self.campos_genericos.items():
            if columna not in self.config_tabla_actual()["identity"]:
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

        for columna, entrada in self.campos_genericos.items():
            entrada.configure(state="normal")
            entrada.delete(0, tk.END)
            entrada.insert(0, datos.get(columna, ""))
            if columna in config["identity"] or columna in config["pk"]:
                entrada.configure(state="disabled")

    def convertir_valor(self, valor, tipo, etiqueta):
        valor = valor.strip()
        if valor == "":
            raise ValueError(f"El campo {etiqueta} no puede estar vacio")
        if tipo == "int":
            return int(valor)
        if tipo in ("float", "decimal"):
            return float(valor)
        return valor

    def valores_formulario_generico(self, incluir_pk=False):
        config = self.config_tabla_actual()
        valores = {}

        for columna, etiqueta, tipo in config["columnas"]:
            if columna in config["identity"]:
                continue
            if not incluir_pk and self.registro_generico_seleccionado is not None and columna in config["pk"]:
                continue

            entrada = self.campos_genericos[columna]
            valores[columna] = self.convertir_valor(entrada.get(), tipo, etiqueta)

        return valores

    def guardar_generico(self):
        config = self.config_tabla_actual()

        try:
            with conectar() as conn:
                cursor = conn.cursor()

                if self.modo_generico == "nuevo":
                    valores = self.valores_formulario_generico(incluir_pk=True)
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
            messagebox.showerror("Error", str(e))

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
            messagebox.showerror("Error", str(e))

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
            messagebox.showerror("Error", str(e))

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
            messagebox.showerror("Error", str(e))

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
            dni = int(self.txt_dni.get())
            nombre = self.txt_nombre.get().strip()
            edad = int(self.txt_edad.get())
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
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def ejecutar_procedimiento(self):
        try:
            with conectar() as conn:
                fila = conn.cursor().execute("EXEC sp_Recalcular_Tiempo_Ganador").fetchone()
                conn.commit()
            messagebox.showinfo("Procedimiento", f"Pruebas procesadas: {fila.PruebasProcesadas}")
        except Exception as e:
            messagebox.showerror("Error", str(e))


if __name__ == "__main__":
    app = AppEsquiadores()
    app.mainloop()

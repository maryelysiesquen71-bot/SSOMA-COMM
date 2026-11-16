# -*- coding: utf-8 -*-
"""
========================================================================================
PLAN ANUAL DE SEGURIDAD Y SALUD EN EL TRABAJO (PASST) - UNMSM | EPISST
CURSO: Prevención y Control de Riesgos Laborales y Ambientales
GRUPO 8 | EMPRESA: Communications and Systems Development SAC (COMM)
DOCENTE: Dr. Edito Luis Rojas Linares
FUENTE DOCUMENTAL: SEG.pdf | DOCUMENTOS COMPLEMENTARIOS: MDR (Mapa de Riesgos) y RISST
INTERFAZ GRÁFICA EN PyQt6 - BANNER PANORÁMICO ESTILO NOTION
========================================================================================
"""

import os
import subprocess
import sys
from pathlib import Path

from PyQt6.QtCore import Qt, QUrl
from PyQt6.QtGui import QAction, QDesktopServices, QPixmap
from PyQt6.QtWidgets import (
    QApplication,
    QFrame,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QSizePolicy,
    QStackedWidget,
    QTextBrowser,
    QVBoxLayout,
    QWidget,
)

# ==========================================================
# 1. CONFIGURACIÓN GENERAL Y PALETA DE COLORES (SEGURIDAD)
# ==========================================================

CARPETA = Path(__file__).parent.resolve() if "__file__" in locals() else Path.cwd()

# Paleta Institucional Azul Petróleo / Seguridad Industrial
AZUL_OSCURO = "#0F2942"       # Azul marino profundo institucional
AZUL_ACCENTO = "#1D4ED8"      # Azul cobalto profesional
AZUL_CLARO = "#3B82F6"        # Azul vibrante de resalte
AZUL_SUAVE = "#EFF6FF"        # Fondo suave azul para tarjetas
AZUL_HEADER = "#0A1C2E"       # Azul muy oscuro para menubar

DORADO_UNMSM = "#B45309"      # Acento institucional
GRIS_FONDO = "#F4F6F9"
BLANCO = "#FFFFFF"
GRIS_BORDE = "#CBD5E1"
TEXTO_PRINCIPAL = "#1E293B"
TEXTO_MUTED = "#475569"


def buscar_archivo(nombre, extensiones=None):
    if extensiones is None:
        extensiones = [".png", ".jpg", ".jpeg", ".bmp", ".webp", ".PNG", ".JPG"]
    for ext in extensiones:
        ruta = CARPETA / f"{nombre}{ext}"
        if ruta.is_file():
            return ruta

    ruta_sin_ext = CARPETA / nombre
    if ruta_sin_ext.is_file():
        return ruta_sin_ext

    return None


# Búsqueda de recursos gráficos
RUTA_FOTO_GRUPAL = buscar_archivo("foto_grupal")
RUTA_LOGO_FII = buscar_archivo("logoFII")
RUTA_LOGO_EPISST = buscar_archivo("logoEPISST")
RUTA_COMM = buscar_archivo("COMM")

# Búsqueda de documentos complementarios (SEG, MDR y RISST)
EXTS_DOCS = [".pdf", ".PDF", ".png", ".jpg", ".jpeg", ".docx", ".DOCX"]
RUTA_DOC_SEG = buscar_archivo("SEG", EXTS_DOCS)
RUTA_DOC_MDR = buscar_archivo("MDR", EXTS_DOCS)
RUTA_DOC_RISST = buscar_archivo("RISST", EXTS_DOCS)


# ==========================================================
# 2. VENTANA PRINCIPAL PyQt6
# ==========================================================

class VentanaPlanSeguridad(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plan Anual de Seguridad y Salud en el Trabajo (PASST) - UNMSM | EPISST | Grupo 8")
        self.resize(1320, 960)
        self.setMinimumSize(1000, 720)

        self.imagenes_redimensionables = []

        self.crear_menu()
        self.crear_interfaz()

        estilo_ventana = (
            f"QMainWindow {{ background-color: {AZUL_OSCURO}; }} "
            f"QMenuBar {{ background-color: {AZUL_HEADER}; color: #F8FAFC; padding: 6px; font-size: 13px; font-weight: 600; }} "
            f"QMenuBar::item {{ background: transparent; padding: 6px 14px; border-radius: 4px; }} "
            f"QMenuBar::item:selected {{ background-color: {AZUL_ACCENTO}; }} "
            f"QMenu {{ background-color: {BLANCO}; color: {TEXTO_PRINCIPAL}; border: 1px solid {GRIS_BORDE}; }} "
            f"QMenu::item {{ padding: 8px 24px; font-size: 12px; }} "
            f"QMenu::item:selected {{ background-color: {AZUL_SUAVE}; color: {AZUL_OSCURO}; font-weight: bold; }} "
            f"QScrollArea {{ border: none; background-color: {AZUL_OSCURO}; }} "
            f"QScrollBar:vertical {{ background: #071320; width: 10px; margin: 0px; }} "
            f"QScrollBar::handle:vertical {{ background: {AZUL_ACCENTO}; min-height: 25px; border-radius: 5px; }}"
        )
        self.setStyleSheet(estilo_ventana)

    # ======================================================
    # 3. MENÚ SUPERIOR INTERACTIVO
    # ======================================================

    def crear_menu(self):
        barra = self.menuBar()

        menu_inicio = barra.addMenu("Inicio")
        menu_capitulos = barra.addMenu("Capítulos del Plan (SEG)")
        menu_documentos = barra.addMenu("Documentos Adjuntos (MDR / RISST)")
        menu_anexos = barra.addMenu("Anexos")
        menu_ayuda = barra.addMenu("Ayuda")

        # Inicio
        accion_portada = QAction("Portada Oficial del Plan SST", self)
        accion_portada.triggered.connect(lambda: self.cambiar_vista(0))
        menu_inicio.addAction(accion_portada)

        menu_inicio.addSeparator()
        accion_salir = QAction("Salir del Aplicativo", self)
        accion_salir.triggered.connect(self.close)
        menu_inicio.addAction(accion_salir)

        # Capítulos del Plan Anual de SST (SEG.pdf)
        secciones = [
            ("Capítulo 1: Alcance, Línea Base, Política, Objetivos y CSST", 1),
            ("Capítulo 2: Gestión de Riesgos (IPERC), Organización, Capacitaciones y PETS", 2),
            ("Capítulo 3: Vigilancia Médica (EMO), Inspecciones, Terceros y Emergencias", 3),
            ("Capítulo 4 y 5: Evaluación, Auditorías, Incidentes y Registros Obligatorios", 4),
            ("Capítulo 6 y 7: Conclusiones y Anexos del Programa Anual SST", 5),
        ]
        for titulo_sec, idx in secciones:
            act = QAction(titulo_sec, self)
            act.triggered.connect(lambda checked, i=idx: self.cambiar_vista(i))
            menu_capitulos.addAction(act)

        # Documentos Complementarios: MDR, RISST y SEG
        accion_visor_docs = QAction("Panel de Visor Documental (MDR y RISST)", self)
        accion_visor_docs.triggered.connect(lambda: self.cambiar_vista(6))
        menu_documentos.addAction(accion_visor_docs)

        menu_documentos.addSeparator()

        accion_abrir_mdr = QAction("Abrir Mapa de Riesgos (MDR)", self)
        accion_abrir_mdr.triggered.connect(lambda: self.abrir_documento_externo(RUTA_DOC_MDR, "MDR (Mapa de Riesgos)"))
        menu_documentos.addAction(accion_abrir_mdr)

        accion_abrir_risst = QAction("Abrir Reglamento Interno de SST (RISST)", self)
        accion_abrir_risst.triggered.connect(lambda: self.abrir_documento_externo(RUTA_DOC_RISST, "RISST (Reglamento Interno de SST)"))
        menu_documentos.addAction(accion_abrir_risst)

        accion_abrir_seg = QAction("Abrir Documento Base Completo (SEG.pdf)", self)
        accion_abrir_seg.triggered.connect(lambda: self.abrir_documento_externo(RUTA_DOC_SEG, "SEG (Plan Anual SST)"))
        menu_documentos.addAction(accion_abrir_seg)

        # Anexos
        accion_anexos = QAction("Ver Resumen de Anexos y Cronogramas 2025", self)
        accion_anexos.triggered.connect(lambda: self.cambiar_vista(5))
        menu_anexos.addAction(accion_anexos)

        # Ayuda
        accion_acerca = QAction("Acerca de", self)
        accion_acerca.triggered.connect(self.mostrar_acerca)
        menu_ayuda.addAction(accion_acerca)

    # ======================================================
    # 4. CONSTRUCCIÓN DE LA ESTRUCTURA CENTRAL
    # ======================================================

    def crear_interfaz(self):
        self.scroll = QScrollArea()
        self.scroll.setWidgetResizable(True)
        self.setCentralWidget(self.scroll)

        self.contenido = QWidget()
        self.contenido.setStyleSheet(f"background-color: {AZUL_OSCURO};")
        self.scroll.setWidget(self.contenido)

        self.layout_principal = QVBoxLayout(self.contenido)
        self.layout_principal.setContentsMargins(24, 16, 24, 28)
        self.layout_principal.setSpacing(18)

        # Banner Panorámico con foto_grupal en formato Cover de Notion
        self.crear_banner_notion()

        # Pila de Vistas (QStackedWidget)
        self.vistas_stack = QStackedWidget()
        self.layout_principal.addWidget(self.vistas_stack)

        # Construir páginas
        self.vista_portada = self.construir_pagina_portada()
        self.vista_cap1 = self.construir_pagina_documento(
            "CAPÍTULO 1: ALCANCE, LÍNEA BASE, POLÍTICA INTEGRADA, OBJETIVOS Y COMITÉ DE SST",
            self.obtener_contenido_cap1()
        )
        self.vista_cap2 = self.construir_pagina_documento(
            "CAPÍTULO 2: GESTIÓN DE RIESGOS (IPERC), RESPONSABILIDADES, CAPACITACIÓN Y PETS",
            self.obtener_contenido_cap2()
        )
        self.vista_cap3 = self.construir_pagina_documento(
            "CAPÍTULO 3: INSPECCIONES INTERNAS, VIGILANCIA MÉDICA (EMO), TERCEROS Y EMERGENCIAS",
            self.obtener_contenido_cap3()
        )
        self.vista_cap4_5 = self.construir_pagina_documento(
            "CAPÍTULOS 4 Y 5: AUDITORÍAS, INVESTIGACIÓN DE INCIDENTES Y REGISTROS OBLIGATORIOS",
            self.obtener_contenido_cap4_5()
        )
        self.vista_cap6_7 = self.construir_pagina_documento(
            "CAPÍTULOS 6 Y 7: CONCLUSIONES Y ANEXOS DEL PROGRAMA ANUAL DE SST 2025",
            self.obtener_contenido_cap6_7()
        )
        self.vista_documentos_externos = self.construir_pagina_documentos_externos()

        self.vistas_stack.addWidget(self.vista_portada)             # 0
        self.vistas_stack.addWidget(self.vista_cap1)                # 1
        self.vistas_stack.addWidget(self.vista_cap2)                # 2
        self.vistas_stack.addWidget(self.vista_cap3)                # 3
        self.vistas_stack.addWidget(self.vista_cap4_5)              # 4
        self.vistas_stack.addWidget(self.vista_cap6_7)              # 5
        self.vistas_stack.addWidget(self.vista_documentos_externos) # 6

        # Pie de página institucional
        self.crear_pie_pagina()

    # ======================================================
    # 5. BANNER PANORÁMICO ESTILO NOTION CON FOTO GRUPAL
    # ======================================================

    def crear_banner_notion(self):
        contenedor_banner = QFrame()
        contenedor_banner.setStyleSheet(
            f"QFrame {{ background-color: {BLANCO}; border-radius: 14px; border: 1px solid {GRIS_BORDE}; }}"
        )
        layout_banner_general = QVBoxLayout(contenedor_banner)
        layout_banner_general.setContentsMargins(0, 0, 0, 16)
        layout_banner_general.setSpacing(12)

        # 1. Imagen panorámica del banner (Cover de Notion con foto_grupal)
        self.label_cover = QLabel()
        self.label_cover.setFixedHeight(220)
        self.label_cover.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.label_cover.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_cover.setStyleSheet(
            f"border-top-left-radius: 13px; border-top-right-radius: 13px; border-bottom: 3px solid {AZUL_CLARO}; overflow: hidden;"
        )

        if RUTA_FOTO_GRUPAL:
            pix = QPixmap(str(RUTA_FOTO_GRUPAL))
            if not pix.isNull():
                self.imagenes_redimensionables.append((self.label_cover, pix))
                self.actualizar_imagen_banner(self.label_cover, pix)
            else:
                self.label_cover.setText("Error al abrir archivo de foto grupal")
        else:
            self.label_cover.setText("No se encontró el archivo 'foto_grupal'")
            self.label_cover.setStyleSheet(
                "QLabel { background: #FEF2F2; color: #B5121B; font-weight: bold; border-top-left-radius: 13px; border-top-right-radius: 13px; }"
            )

        layout_banner_general.addWidget(self.label_cover)

        # 2. Barra de Datos Institucionales y Logos
        fila_datos = QHBoxLayout()
        fila_datos.setContentsMargins(20, 6, 20, 0)
        fila_datos.setSpacing(16)

        # Logo FII
        self.label_logo_fii = QLabel()
        self.label_logo_fii.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_logo_fii.setFixedSize(140, 70)
        self.label_logo_fii.setStyleSheet(f"background-color: {BLANCO}; border: 1px solid {GRIS_BORDE}; border-radius: 8px; padding: 4px;")
        self.cargar_imagen_en_label(self.label_logo_fii, RUTA_LOGO_FII, "logoFII")
        fila_datos.addWidget(self.label_logo_fii, stretch=0)

        # Membrete Oficial Central
        layout_central = QVBoxLayout()
        layout_central.setSpacing(3)

        lbl_univ = QLabel("UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS")
        lbl_univ.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_univ.setStyleSheet(f"color: {AZUL_OSCURO}; font-size: 15px; font-weight: 900; letter-spacing: 0.5px;")

        lbl_decana = QLabel("Universidad del Perú, DECANA DE AMÉRICA • FACULTAD DE INGENIERÍA INDUSTRIAL")
        lbl_decana.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_decana.setStyleSheet(f"color: {DORADO_UNMSM}; font-size: 11px; font-weight: 700; font-style: italic;")

        lbl_escuela = QLabel("Escuela Profesional de Ingeniería de Seguridad y Salud en el Trabajo (EPISST)")
        lbl_escuela.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_escuela.setStyleSheet(f"color: {AZUL_ACCENTO}; font-size: 12px; font-weight: 800;")

        layout_central.addWidget(lbl_univ)
        layout_central.addWidget(lbl_decana)
        layout_central.addWidget(lbl_escuela)
        fila_datos.addLayout(layout_central, stretch=4)

        # Logo EPISST
        self.label_logo_episst = QLabel()
        self.label_logo_episst.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_logo_episst.setFixedSize(130, 70)
        self.label_logo_episst.setStyleSheet(f"background-color: {BLANCO}; border: 1px solid {GRIS_BORDE}; border-radius: 8px; padding: 4px;")
        self.cargar_imagen_en_label(self.label_logo_episst, RUTA_LOGO_EPISST, "logoEPISST")
        fila_datos.addWidget(self.label_logo_episst, stretch=0)

        # Logo COMM
        self.label_comm = QLabel()
        self.label_comm.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.label_comm.setFixedSize(130, 70)
        self.label_comm.setStyleSheet(f"background-color: {BLANCO}; border: 1px solid {GRIS_BORDE}; border-radius: 8px; padding: 4px;")
        self.cargar_imagen_en_label(self.label_comm, RUTA_COMM, "Logo COMM")
        fila_datos.addWidget(self.label_comm, stretch=0)

        layout_banner_general.addLayout(fila_datos)

        # 3. Franja del Título del Plan Anual de SST
        lbl_lema = QLabel("PLAN ANUAL DE SEGURIDAD Y SALUD EN EL TRABAJO (PASST)  |  U.M. SAN CRISTÓBAL - CARAHUACRA (VOLCAN CÍA. MINERA S.A.A.)")
        lbl_lema.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_lema.setStyleSheet(
            f"QLabel {{ background-color: {AZUL_SUAVE}; color: {AZUL_OSCURO}; border: 1px solid {AZUL_CLARO}; "
            f"border-radius: 8px; padding: 7px 12px; font-size: 12.5px; font-weight: 800; margin: 4px 18px 0px 18px; }}"
        )
        layout_banner_general.addWidget(lbl_lema)

        self.layout_principal.addWidget(contenedor_banner)

    # ======================================================
    # 6. PORTADA INTERACTIVA CON INTEGRANTES Y ACCESOS RÁPIDOS
    # ======================================================

    def construir_pagina_portada(self):
        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            f"QFrame {{ background-color: {BLANCO}; border-radius: 12px; border: 1px solid {GRIS_BORDE}; }}"
        )

        layout_general = QVBoxLayout(tarjeta)
        layout_general.setContentsMargins(22, 18, 22, 22)
        layout_general.setSpacing(16)

        titulo = QLabel("PORTADA OFICIAL: PLAN ANUAL DE SEGURIDAD Y SALUD EN EL TRABAJO (DOCUMENTO BASE: SEG)")
        titulo.setStyleSheet(
            f"QLabel {{ color: {AZUL_OSCURO}; font-size: 15px; font-weight: 800; "
            f"letter-spacing: 0.6px; padding-bottom: 6px; border-bottom: 2px solid {AZUL_CLARO}; }}"
        )
        layout_general.addWidget(titulo)

        columnas = QHBoxLayout()
        columnas.setSpacing(20)

        # Columna Izquierda: Información Académica del Proyecto
        panel_datos = QFrame()
        panel_datos.setStyleSheet(
            f"QFrame {{ background-color: {GRIS_FONDO}; border: 1px solid {GRIS_BORDE}; border-radius: 10px; }}"
        )
        layout_datos = QVBoxLayout(panel_datos)
        layout_datos.setContentsMargins(16, 14, 16, 14)
        layout_datos.setSpacing(10)

        lbl_tit_datos = QLabel("DATOS GENERALES DE LA ASIGNATURA Y EMPRESA")
        lbl_tit_datos.setStyleSheet(f"color: {AZUL_OSCURO}; font-size: 12px; font-weight: 900; border: none; background: transparent;")
        layout_datos.addWidget(lbl_tit_datos)

        datos = [
            ("CURSO", "Prevención y Control de Riesgos Laborales y Ambientales"),
            ("DOCENTE", "Dr. Edito Luis Rojas Linares"),
            ("EMPRESA CONTRATISTA", "Communications and Systems Development S.A.C. (COMM - RUC 20544048164)"),
            ("TITULAR MINERO", "Unidad Minera San Cristóbal - Carahuacra (Volcan Compañía Minera S.A.A.)"),
            ("LUGAR Y AÑO", "LIMA - PERÚ | 2026"),
        ]

        for etiqueta, valor in datos:
            fila = QFrame()
            fila.setStyleSheet(
                f"QFrame {{ background-color: {BLANCO}; border: 1px solid #E2E8F0; "
                f"border-left: 4px solid {AZUL_ACCENTO}; border-radius: 6px; }}"
            )
            fila_layout = QVBoxLayout(fila)
            fila_layout.setContentsMargins(10, 6, 10, 6)
            fila_layout.setSpacing(2)

            lbl_etiqueta = QLabel(etiqueta)
            lbl_etiqueta.setStyleSheet(f"QLabel {{ color: {TEXTO_MUTED}; font-size: 10px; font-weight: 700; border: none; background: transparent; }}")

            lbl_valor = QLabel(valor)
            lbl_valor.setWordWrap(True)
            lbl_valor.setStyleSheet(f"QLabel {{ color: {TEXTO_PRINCIPAL}; font-size: 12px; font-weight: 700; border: none; background: transparent; }}")

            fila_layout.addWidget(lbl_etiqueta)
            fila_layout.addWidget(lbl_valor)
            layout_datos.addWidget(fila)

        columnas.addWidget(panel_datos, stretch=1)

        # Columna Derecha: Integrantes del Grupo 8 y Acceso Directo MDR / RISST
        columna_derecha = QVBoxLayout()
        columna_derecha.setSpacing(14)

        marco_grupo = QFrame()
        marco_grupo.setStyleSheet(f"QFrame {{ background-color: {GRIS_FONDO}; border: 1px solid {GRIS_BORDE}; border-radius: 10px; }}")
        layout_grupo = QVBoxLayout(marco_grupo)
        layout_grupo.setContentsMargins(16, 14, 16, 14)
        layout_grupo.setSpacing(8)

        lbl_tit_grupo = QLabel("GRUPO 8 — INTEGRANTES EPISST")
        lbl_tit_grupo.setStyleSheet(f"color: {AZUL_OSCURO}; font-size: 12px; font-weight: 900; border: none; background: transparent;")
        layout_grupo.addWidget(lbl_tit_grupo)

        integrantes = [
            ("Condorcuya Flores, Gerardo Manuel", "23170109"),
            ("Siesquen Roman, Gina Maryely", "23170304"),
            ("Arias Benavides, Leonardo Miguel", "23170278"),
            ("Delgado Jonis, Kassandra Mirella", "23170288"),
            ("Vite Pimentel, Emmy Hilary", "23170122"),
        ]

        for nombre, codigo in integrantes:
            fila_int = QFrame()
            fila_int.setStyleSheet(
                f"QFrame {{ background-color: {BLANCO}; border: 1px solid #E2E8F0; "
                f"border-left: 4px solid {AZUL_CLARO}; border-radius: 6px; }}"
            )
            f_item = QHBoxLayout(fila_int)
            f_item.setContentsMargins(10, 6, 10, 6)

            lbl_n = QLabel(f"• {nombre}")
            lbl_n.setStyleSheet(f"color: {TEXTO_PRINCIPAL}; font-size: 12px; font-weight: 600; border: none; background: transparent;")
            lbl_c = QLabel(codigo)
            lbl_c.setStyleSheet(f"color: {AZUL_ACCENTO}; font-size: 11.5px; font-weight: 800; border: none; background: transparent;")

            f_item.addWidget(lbl_n)
            f_item.addStretch()
            f_item.addWidget(lbl_c)
            layout_grupo.addWidget(fila_int)

        columna_derecha.addWidget(marco_grupo)

        # Tarjeta de Acceso Rápido a Documentos Complementarios (MDR y RISST)
        marco_docs = QFrame()
        marco_docs.setStyleSheet(f"QFrame {{ background-color: {AZUL_SUAVE}; border: 1.5px solid {AZUL_CLARO}; border-radius: 10px; }}")
        layout_docs = QVBoxLayout(marco_docs)
        layout_docs.setContentsMargins(14, 12, 14, 12)
        layout_docs.setSpacing(8)

        lbl_docs_tit = QLabel("ACCESO DIRECTO A DOCUMENTOS COMPLEMENTARIOS")
        lbl_docs_tit.setStyleSheet(f"color: {AZUL_OSCURO}; font-size: 11.5px; font-weight: 900; border: none; background: transparent;")
        layout_docs.addWidget(lbl_docs_tit)

        fila_botones = QHBoxLayout()
        fila_botones.setSpacing(10)

        btn_mdr = QPushButton("🗺️ Abrir Mapa de Riesgos (MDR)")
        btn_mdr.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_mdr.setStyleSheet(
            f"QPushButton {{ background-color: {AZUL_ACCENTO}; color: {BLANCO}; border-radius: 6px; padding: 8px 12px; font-weight: bold; font-size: 12px; }} "
            f"QPushButton:hover {{ background-color: {AZUL_OSCURO}; }}"
        )
        btn_mdr.clicked.connect(lambda: self.abrir_documento_externo(RUTA_DOC_MDR, "MDR (Mapa de Riesgos)"))

        btn_risst = QPushButton("📘 Abrir Reglamento Interno (RISST)")
        btn_risst.setCursor(Qt.CursorShape.PointingHandCursor)
        btn_risst.setStyleSheet(
            f"QPushButton {{ background-color: {DORADO_UNMSM}; color: {BLANCO}; border-radius: 6px; padding: 8px 12px; font-weight: bold; font-size: 12px; }} "
            f"QPushButton:hover {{ background-color: #78350F; }}"
        )
        btn_risst.clicked.connect(lambda: self.abrir_documento_externo(RUTA_DOC_RISST, "RISST (Reglamento Interno de SST)"))

        fila_botones.addWidget(btn_mdr)
        fila_botones.addWidget(btn_risst)
        layout_docs.addLayout(fila_botones)

        columna_derecha.addWidget(marco_docs)
        columnas.addLayout(columna_derecha, stretch=1)

        layout_general.addLayout(columnas)

        # Nota de navegación
        nota_nav = QLabel("🛡️ Explora los capítulos del Plan Anual de SST (SEG) o abre los archivos MDR y RISST desde el menú superior o los botones de acceso directo.")
        nota_nav.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nota_nav.setStyleSheet(f"background-color: {AZUL_SUAVE}; color: {AZUL_OSCURO}; border: 1px dashed {AZUL_CLARO}; border-radius: 6px; padding: 8px; font-size: 12px; font-weight: 700;")
        layout_general.addWidget(nota_nav)

        return tarjeta

    # ======================================================
    # 7. PÁGINA VISOR DE DOCUMENTOS COMPLEMENTARIOS (MDR / RISST / SEG)
    # ======================================================

    def construir_pagina_documentos_externos(self):
        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            f"QFrame {{ background-color: {BLANCO}; border-radius: 12px; border: 1px solid {GRIS_BORDE}; }}"
        )
        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(24, 20, 24, 22)
        layout.setSpacing(16)

        lbl_tit = QLabel("GESTOR DE DOCUMENTOS DEL SISTEMA DE GESTIÓN DE SST (SEG, MDR Y RISST)")
        lbl_tit.setStyleSheet(
            f"QLabel {{ color: {AZUL_OSCURO}; font-size: 15px; font-weight: 900; "
            f"letter-spacing: 0.5px; padding-bottom: 6px; border-bottom: 2px solid {AZUL_CLARO}; }}"
        )
        layout.addWidget(lbl_tit)

        desc = QLabel(
            "Selecciona cualquiera de los documentos oficiales almacenados en la carpeta del proyecto para abrirlos en su visor predeterminado:"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {TEXTO_PRINCIPAL}; font-size: 13px; border: none;")
        layout.addWidget(desc)

        documentos_info = [
            (
                "1. Mapa de Riesgos (MDR)",
                "Representación gráfica de los peligros y riesgos localizados en las áreas de trabajo, talleres, oficinas y labores subterráneas (RP 742 - Nivel 820) de COMM en U.M. San Cristóbal - Carahuacra.",
                RUTA_DOC_MDR,
                "MDR",
                AZUL_ACCENTO,
            ),
            (
                "2. Reglamento Interno de Seguridad y Salud en el Trabajo (RISST)",
                "Normativa interna de cumplimiento obligatorio aprobada por el Comité de SST (CSST) que establece derechos, obligaciones, estándares y sanciones preventivas para todos los colaboradores y subcontratistas.",
                RUTA_DOC_RISST,
                "RISST",
                DORADO_UNMSM,
            ),
            (
                "3. Plan Anual de Seguridad y Salud en el Trabajo (SEG.pdf)",
                "Documento matriz completo (179 páginas) con la Línea Base 2024, Política RD-PL-01 v.08, Matrices IPERC, Compendio de PETS-COM-MIN-01 al 08, Plan de Emergencias y Registros Obligatorios.",
                RUTA_DOC_SEG,
                "SEG",
                AZUL_OSCURO,
            ),
        ]

        for titulo_doc, detalle_doc, ruta_doc, nombre_corto, color_btn in documentos_info:
            card_doc = QFrame()
            card_doc.setStyleSheet(
                f"QFrame {{ background-color: {GRIS_FONDO}; border: 1px solid {GRIS_BORDE}; "
                f"border-left: 5px solid {color_btn}; border-radius: 8px; }}"
            )
            l_card = QHBoxLayout(card_doc)
            l_card.setContentsMargins(16, 14, 16, 14)
            l_card.setSpacing(16)

            l_texto = QVBoxLayout()
            l_texto.setSpacing(4)

            t_lbl = QLabel(titulo_doc)
            t_lbl.setStyleSheet(f"color: {AZUL_OSCURO}; font-size: 14px; font-weight: 800; border: none; background: transparent;")

            d_lbl = QLabel(detalle_doc)
            d_lbl.setWordWrap(True)
            d_lbl.setStyleSheet(f"color: {TEXTO_PRINCIPAL}; font-size: 12.5px; border: none; background: transparent;")

            estado_txt = f"Archivo detectado: {ruta_doc.name}" if ruta_doc else f"Archivo '{nombre_corto}' pendiente en la carpeta del script"
            estado_color = "#15803D" if ruta_doc else "#B91C1C"
            e_lbl = QLabel(estado_txt)
            e_lbl.setStyleSheet(f"color: {estado_color}; font-size: 11px; font-weight: 700; border: none; background: transparent;")

            l_texto.addWidget(t_lbl)
            l_texto.addWidget(d_lbl)
            l_texto.addWidget(e_lbl)

            btn_abrir = QPushButton(f"Abrir {nombre_corto}")
            btn_abrir.setFixedSize(140, 42)
            btn_abrir.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_abrir.setStyleSheet(
                f"QPushButton {{ background-color: {color_btn}; color: {BLANCO}; border-radius: 8px; font-weight: bold; font-size: 12.5px; }} "
                f"QPushButton:hover {{ opacity: 0.9; }}"
            )
            btn_abrir.clicked.connect(lambda checked, r=ruta_doc, n=nombre_corto: self.abrir_documento_externo(r, n))

            l_card.addLayout(l_texto, stretch=4)
            l_card.addWidget(btn_abrir, stretch=0)
            layout.addWidget(card_doc)

        layout.addStretch()
        return tarjeta

    def abrir_documento_externo(self, ruta, nombre_doc):
        if ruta is None or not ruta.exists():
            QMessageBox.warning(
                self,
                "Archivo no encontrado",
                f"No se encontró el archivo '{nombre_doc}' en la carpeta del proyecto:\n{CARPETA}\n\n"
                f"Asegúrate de guardar '{nombre_doc}.pdf' (o .png/.jpg/.docx) junto al script."
            )
            return

        url = QUrl.fromLocalFile(str(ruta))
        if not QDesktopServices.openUrl(url):
            try:
                if sys.platform.startswith("win"):
                    os.startfile(str(ruta))
                elif sys.platform.startswith("darwin"):
                    subprocess.run(["open", str(ruta)], check=False)
                else:
                    subprocess.run(["xdg-open", str(ruta)], check=False)
            except Exception as exc:
                QMessageBox.critical(self, "Error al abrir documento", f"No se pudo abrir '{ruta.name}':\n{exc}")

    # ======================================================
    # 8. CONSTRUCTOR DE PÁGINAS DE CONTENIDO DEL DOCUMENTO
    # ======================================================

    def construir_pagina_documento(self, titulo, contenido_html):
        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            f"QFrame {{ background-color: {BLANCO}; border-radius: 12px; border: 1px solid {GRIS_BORDE}; }}"
        )

        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(24, 20, 24, 22)
        layout.setSpacing(14)

        lbl_tit = QLabel(titulo)
        lbl_tit.setStyleSheet(
            f"QLabel {{ color: {AZUL_OSCURO}; font-size: 15px; font-weight: 900; "
            f"letter-spacing: 0.5px; padding-bottom: 6px; border-bottom: 2px solid {AZUL_CLARO}; }}"
        )
        layout.addWidget(lbl_tit)

        visor = QTextBrowser()
        visor.setHtml(contenido_html)
        visor.setOpenExternalLinks(True)
        visor.setStyleSheet(
            f"QTextBrowser {{ background-color: {GRIS_FONDO}; border: 1px solid {GRIS_BORDE}; "
            f"border-radius: 8px; padding: 16px; color: {TEXTO_PRINCIPAL}; font-size: 13px; line-height: 1.5; }}"
        )
        layout.addWidget(visor)

        return tarjeta

    # ======================================================
    # 9. PIE DE PÁGINA
    # ======================================================

    def crear_pie_pagina(self):
        pie = QLabel(
            "UNIVERSIDAD NACIONAL MAYOR DE SAN MARCOS  •  FACULTAD DE INGENIERÍA INDUSTRIAL  •  EPISST  •  2026"
        )
        pie.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pie.setStyleSheet(
            "color: #DBEAFE; font-size: 11px; font-weight: 700; letter-spacing: 1px; padding: 4px;"
        )
        self.layout_principal.addWidget(pie)

    # ======================================================
    # 10. GESTOR DE NAVEGACIÓN Y CARGA DE IMÁGENES
    # ======================================================

    def cambiar_vista(self, indice):
        self.vistas_stack.setCurrentIndex(indice)
        self.scroll.verticalScrollBar().setValue(0)

    def cargar_imagen_en_label(self, label, ruta, nombre):
        if ruta is None:
            label.setText(f"Archivo no encontrado:\n'{nombre}'")
            label.setStyleSheet(
                f"QLabel {{ background-color: #FEF2F2; color: #B5121B; "
                f"border: 1px dashed #B5121B; border-radius: 6px; font-size: 11px; font-weight: bold; padding: 6px; }}"
            )
            return

        pixmap = QPixmap(str(ruta))
        if pixmap.isNull():
            label.setText(f"Error al abrir:\n{nombre}")
            return

        self.imagenes_redimensionables.append((label, pixmap))
        self.actualizar_imagen(label, pixmap)

    def actualizar_imagen(self, label, pixmap):
        if label.width() <= 0 or label.height() <= 0:
            return
        escalada = pixmap.scaled(
            label.size(),
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
        label.setPixmap(escalada)

    def actualizar_imagen_banner(self, label, pixmap):
        """Escala la foto grupal como un banner panorámico tipo cover de Notion."""
        if label.width() <= 0 or label.height() <= 0:
            return
        escalada = pixmap.scaled(
            label.size(),
            Qt.AspectRatioMode.KeepAspectRatioByExpanding,
            Qt.TransformationMode.SmoothTransformation,
        )
        label.setPixmap(escalada)

    def resizeEvent(self, event):
        for label, pixmap in self.imagenes_redimensionables:
            if label == self.label_cover:
                self.actualizar_imagen_banner(label, pixmap)
            else:
                self.actualizar_imagen(label, pixmap)
        super().resizeEvent(event)

    def mostrar_acerca(self):
        QMessageBox.about(
            self,
            "Acerca del Plan Anual de SST (PASST)",
            "Plan Anual de Seguridad y Salud en el Trabajo (PASST)\n"
            "Documento Fuente: SEG.pdf | Documentos Anexos: MDR y RISST\n"
            "Curso: Prevención y Control de Riesgos Laborales y Ambientales\n"
            "Escuela Profesional de Ingeniería de Seguridad y Salud en el Trabajo (EPISST)\n"
            "Facultad de Ingeniería Industrial - UNMSM\n\n"
            "Docente: Dr. Edito Luis Rojas Linares\n"
            "Grupo 8 | Empresa: Communications and Systems Development SAC (COMM)\n"
            "Operación: U.M. San Cristóbal - Carahuacra (Volcan Cía. Minera S.A.A.)\n"
            "Año Académico: 2026",
        )

    # ======================================================
    # 11. CONTENIDO FORMALIZADO DEL DOCUMENTO BASE (SEG.pdf)
    # ======================================================

    def obtener_contenido_cap1(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>1.1 Alcance y Ficha Técnica de la Operación</h3>
            <p>El Plan Anual de Seguridad y Salud en el Trabajo (PASST) abarca de manera integral y obligatoria todos los procesos de ingeniería, tendido de fibra óptica dieléctrica (monomodo/multimodo), instalación de sistemas Leaky Feeder, montaje de bandejas portacables, gabinetes herméticos, antenas VHF/UHF, telemetría y mantenimiento eléctrico/electrónico desarrollados por <b>Communications and Systems Development S.A.C. (COMM)</b> en la <b>Unidad Minera San Cristóbal - Carahuacra</b> de <b>Volcan Compañía Minera S.A.A.</b> (Yauli, Junín, entre 4,000 y 4,750 m.s.n.m.).</p>
            <p><b>Frentes Críticos:</b> Labores subterráneas en socavón (Rampa Principal RP 742, Nivel 820, galerías, subestaciones, chimeneas y refugios mineros) e instalaciones de superficie (salas de control, cuartos de servidores, talleres electromecánicos y almacenes).</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>1.2 Elaboración de la Línea Base del Sistema de Gestión (2023 - 2024)</h3>
            <p>Al cierre del ejercicio operativo 2024, COMM registró los siguientes resultados estadísticos en el proyecto:</p>
            <ul>
                <li><b>Horas Hombre Trabajadas (HHT):</b> 51,550.45 HHT (2023) y 46,558.40 HHT (2024).</li>
                <li><b>Accidentes Mortales e Incapacitantes:</b> 0 eventos registrados (0 días perdidos).</li>
                <li><b>Índices de Siniestralidad 2024:</b> LTIFR (Frecuencia) = <b>0.00</b> | DISR/DSIFR (Severidad) = <b>0.00</b> | TRIFR (Accidentabilidad Total) = <b>0.00</b>.</li>
            </ul>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>1.3 Política Integrada de Gestión (Código RD-PL-01, Versión 08)</h3>
            <p>Aprobada el 15/10/2025 por Filiberto Jesús Revilla Delgado (CEO Director) y Sergio David Gonzales Mendívil (Gerente General). Respaldada por certificaciones internacionales <b>ISO 9001:2015, ISO 14001:2015 e ISO 45001:2018</b> y cumplimiento estricto de la Ley N.° 29783, D.S. 005-2012-TR y D.S. 024-2016-EM (mod. D.S. 023-2017-EM).</p>
            <ol>
                <li>Brindar servicio de calidad, rapidez y confiabilidad técnica a los clientes mineros.</li>
                <li><b>Eliminar peligros y reducir riesgos</b> aplicando prioritariamente la jerarquía de controles.</li>
                <li>Proteger el ambiente y prevenir la contaminación mediante gestión responsable de residuos.</li>
                <li>Cumplir rigurosamente la normativa legal vigente y estándares corporativos de Volcan.</li>
                <li>Promover la capacitación, sensibilización, consulta y participación activa de los trabajadores.</li>
                <li>Mejorar continuamente el Sistema Integrado de Gestión mediante evaluaciones periódicas.</li>
            </ol>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>1.4 Objetivos y Metas del SGSST (Metodología SMART)</h3>
            <table border='1' cellpadding='5' cellspacing='0' style='border-collapse:collapse; width:100%; border-color:{GRIS_BORDE};'>
                <tr style='background-color:{AZUL_SUAVE}; font-weight:bold; color:{AZUL_OSCURO};'>
                    <td>Objetivo</td><td>Indicador</td><td>Meta 2025</td><td>Frecuencia</td><td>Responsable</td>
                </tr>
                <tr><td>Reducir a cero los accidentes incapacitantes</td><td>LTIFR (Lost Time Injury Frequency)</td><td><b>0</b></td><td>Mensual</td><td>Área de SST</td></tr>
                <tr><td>Reducir la severidad de los accidentes</td><td>DSIFR (Disabling Injury Severity Rate)</td><td><b>0</b></td><td>Mensual</td><td>Área de SST</td></tr>
                <tr><td>Reducir la accidentabilidad total</td><td>TRIFR (Total Recordable Injury Rate)</td><td><b>0</b></td><td>Mensual</td><td>Área de SST</td></tr>
                <tr><td>Asegurar operatividad de ambientes y equipos</td><td>% Inspecciones realizadas / programadas</td><td><b>100%</b></td><td>Mensual</td><td>Supervisores</td></tr>
                <tr><td>Fortalecer el conocimiento en seguridad</td><td>Capacitaciones ejecutadas / programadas</td><td><b>&ge; 90%</b></td><td>Mensual</td><td>Supervisores</td></tr>
                <tr><td>Ejecución de simulacros de emergencia</td><td>% Simulacros ejecutados / programados</td><td><b>&ge; 80%</b></td><td>Semestral</td><td>Supervisor SST</td></tr>
            </table>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>1.5 Comité de Seguridad y Salud en el Trabajo (CSST Periodo 2025 - 2027)</h3>
            <p>Órgano bipartito y paritario constituido bajo Registro <b>SIG/GSS/REG-14 (v.02)</b> con <b>8 miembros</b> (4 titulares y 4 suplentes). Sesiona ordinariamente una vez al mes (convocatoria mínima 24 h antes) y envía copias de actas en un plazo improrrogable de 72 horas. Cuenta con <b>Libro de Actas (REG-TA-GLO-06-05)</b> y <b>Libro de Seguridad foliado de 200 páginas</b> legalizado por Juez de Paz (Art. 61 D.S. 024-2016-EM).</p>
            <ul>
                <li><b>Miembros Titulares:</b> Paul Avila (Presidente), Fernanda Salome (Secretaria), Santos Ramirez (Miembro Titular) y Jorge Asencios (Miembro Titular).</li>
                <li><b>Miembros Suplentes:</b> Luis Revilla, Danny Romero (y vacantes paritarias designadas).</li>
                <li><b>Atribuciones clave:</b> Aprobar el PASST y el <b>RISST (Reglamento Interno de SST)</b>, realizar inspecciones mensuales (REG-TA-GLO-08-07), investigar accidentes y vigilar los indicadores de SST.</li>
            </ul>
        </div>
        """

    def obtener_contenido_cap2(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>2.1 Identificación de Peligros, Evaluación de Riesgos y Controles (IPERC)</h3>
            <p>En cumplimiento del Art. 57 de la Ley 29783 y Arts. 95-97 del D.S. 024-2016-EM, COMM emplea una matriz bidimensional <b>5 &times; 5</b> (Riesgo Puro vs. Riesgo Residual) complementada diariamente en campo con el <b>IPERC Continuo</b> y el <b>Análisis de Trabajo Seguro (ATS)</b>.</p>
            <table border='1' cellpadding='5' cellspacing='0' style='border-collapse:collapse; width:100%; border-color:{GRIS_BORDE};'>
                <tr style='background-color:{AZUL_SUAVE}; font-weight:bold; color:{AZUL_OSCURO};'>
                    <td>Nivel de Riesgo</td><td>Rango (D.S. 024-2016-EM)</td><td>Descripción y Acción</td><td>Plazo Corrección</td>
                </tr>
                <tr><td style='color:#B91C1C; font-weight:bold;'>ALTO (Intolerable)</td><td>1 - 8 (Rojo)</td><td>Requiere controles inmediatos. Si no puede controlarse, se paraliza el trabajo.</td><td>0 - 24 horas (Inmediato)</td></tr>
                <tr><td style='color:#B45309; font-weight:bold;'>MEDIO (Moderado)</td><td>9 - 15 (Amarillo)</td><td>Iniciar medidas para eliminar o reducir el riesgo.</td><td>0 - 72 horas</td></tr>
                <tr><td style='color:#15803D; font-weight:bold;'>BAJO (Tolerable)</td><td>16 - 25 (Verde)</td><td>Riesgo tolerable; mantener monitoreo y cumplimiento de estándares.</td><td>1 mes</td></tr>
            </table>
            <p><b>Jerarquía de Controles (Orden Obligatorio):</b> (1) Eliminación &rarr; (2) Sustitución &rarr; (3) Controles de Ingeniería (LOTO, líneas de vida, guardas) &rarr; (4) Controles Administrativos (PETS, PETAR, señalización, <b>Mapa de Riesgos MDR</b>) &rarr; (5) EPP certificados.</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>2.2 Organización, Responsabilidades y Derecho a Decir NO</h3>
            <ul>
                <li><b>Gerencia General:</b> Liderar el SGSST, aprobar el PASST, asignar presupuesto y presidir la Revisión por la Dirección.</li>
                <li><b>Área de SST / Jefe de Seguridad:</b> Gestionar el SGSST, asesorar al CSST, consolidar estadísticas, coordinar auditorías y monitoreos ocupacionales.</li>
                <li><b>Supervisores de Campo:</b> Validar presencialmente el IPERC Continuo antes de cada guardia, verificar PETS/PETAR, inspeccionar herramientas y dirigir las charlas de 5 minutos.</li>
                <li><b>Trabajadores (Primera línea de defensa):</b> Cumplir el <b>RISST</b> y los PETS, usar correctamente sus EPP, elaborar el IPERC Continuo grupal y ejercer el <b>«Derecho a Decir NO»</b> ante cualquier peligro grave e inminente sin temor a represalias.</li>
            </ul>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>2.3 Programa de Formación y Capacitación (Meta &ge; 90% | Presupuesto: S/ 3,500)</h3>
            <ol>
                <li><b>Nivel 1 - Inducción General y Específica:</b> Política SST, <b>RISST</b>, <b>Mapa de Riesgos (MDR)</b>, Plan de Emergencias y reconocimiento en RP 742 y Nivel 820 (Anexos 4 y 5 D.S. 024-2016-EM).</li>
                <li><b>Nivel 2 - Cursos Básicos Obligatorios (Anexo 6):</b> Legislación minera, IPERC, investigación de incidentes, primeros auxilios (RCP), lucha contra incendios y trabajos de alto riesgo.</li>
                <li><b>Nivel 3 - Capacitación Técnica Especializada:</b> Tendido y empalme de fibra óptica, montaje de gabinetes/racks, bloqueo LOTO, trabajos en altura (&ge; 1.80 m) e inspección de escaleras dieléctricas.</li>
                <li><b>Nivel 4 - Charlas Diarias de 5 Minutos:</b> Antes de cada turno, revisando condiciones geomecánicas, tránsito de scooptrams y lecciones aprendidas.</li>
            </ol>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>2.4 Procedimientos Escritos de Trabajo Seguro (PETS) y Permisos (PETAR)</h3>
            <p>Estructurados bajo el <b>Anexo N.° 10 del D.S. 024-2016-EM</b> (Objetivo, Personal, EPP, Equipos/Herramientas, Procedimiento Paso a Paso y Restricciones Operativas):</p>
            <ul>
                <li><b>PETS-COM-MIN-01:</b> Inspección, traslado y transporte de personal, herramientas de fibra óptica y equipos en interior mina.</li>
                <li><b>PETS-COM-MIN-02:</b> Desate preventivo de rocas sueltas en hastiales y techos previo a instalación de soportería.</li>
                <li><b>PETS-COM-MIN-03:</b> Tendido aéreo, grapado y fijación de cable de fibra óptica y par trenzado en galerías y chimeneas.</li>
                <li><b>PETS-COM-MIN-04:</b> Trabajos de fusión, empalme y conectorización óptica en mufas y cajas de distribución.</li>
                <li><b>PETS-COM-MIN-05:</b> Instalación, anclaje y puesta en marcha de gabinetes de comunicación, racks y sistemas UPS.</li>
                <li><b>PETS-COM-MIN-06:</b> Conexionado y energización de equipos en tableros eléctricos secundarios (con bloqueo LOTO).</li>
                <li><b>PETS-COM-MIN-07:</b> Montaje, orientación y mantenimiento de antenas de radioenlace y repetidoras.</li>
                <li><b>PETS-COM-MIN-08:</b> Uso técnico e inspección preoperacional de escaleras portátiles dieléctricas en galerías mineras.</li>
            </ul>
            <p><b>Permisos Escritos de Trabajo de Alto Riesgo (PETAR - Art. 128 D.S. 024-2016-EM):</b> Obligatorios por turno para Trabajos en Altura (&ge; 1.80 m, anclaje 5,000 lbf), Energía Eléctrica (5 reglas de oro + LOTO) y Espacios Confinados (monitoreo multigás continuo).</p>
        </div>
        """

    def obtener_contenido_cap3(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>3.1 Programa Anual de Inspecciones Internas (120 Inspecciones | Meta: 100%)</h3>
            <p>Ejecutadas bajo modalidades <b>Diaria (Preoperacional)</b>, <b>Planeada Mensual</b> e <b>Inopinada</b> mediante el formato oficial <b>REG-TA-GLO-08-07</b> sobre 10 categorías críticas (12 rondas/año cada una):</p>
            <ol>
                <li>Oficinas técnicas y administrativas (orden, iluminación, ergonomía).</li>
                <li>Vestuarios y servicios higiénicos.</li>
                <li>Extintores portátiles contra incendios (manómetro, precinto, tarjeta).</li>
                <li>Almacenes y talleres de mantenimiento (rotulación SDS/MSDS, estanterías).</li>
                <li>Escaleras portátiles dieléctricas de fibra de vidrio (tijera y extensión).</li>
                <li>Equipos de protección contra caídas (arneses, líneas de vida, anillos en "D").</li>
                <li>Equipos y vehículos móviles (frenos, luces, circulina, pértiga LED, alarma de retroceso).</li>
                <li>Herramientas manuales aisladas (1000 V) y equipos eléctricos portátiles (código de colores del mes).</li>
                <li>Botiquines de primeros auxilios.</li>
                <li>Equipos de Protección Personal (EPP minero y dieléctrico).</li>
            </ol>
            <p><b>Plazos de cierre de hallazgos:</b> Máximo <b>24 a 48 horas</b> para Riesgos Altos (con paralización inmediata) y <b>7 días calendario</b> para Riesgos Medios, con evidencia fotográfica "Antes y Después".</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>3.2 Salud Ocupacional y Vigilancia Médica (EMO)</h3>
            <ul>
                <li><b>Evaluaciones Médico-Ocupacionales (EMO):</b> Preocupacional (ingreso para altitud &gt; 4,000 m.s.n.m. con espirometría ATS, audiometría, radiografía OIT y EKG), Periódica Anual y de Retiro.</li>
                <li><b>Límites de Ruido Mecánico (D.S. 024-2016-EM):</b> 82 dB (16 h), 85 dB (8 h), 88 dB (4 h), 91 dB (1.5 h), 94 dB (1 h), 97 dB (30 min), 100 dB (15 min). Doble protección auditiva obligatoria sobre 100 dB(A).</li>
                <li><b>Riesgos Disergonómicos y Psicosociales:</b> Control en manipulación de bobinas, trabajo sobre escaleras, fatiga por turnos atípicos y aislamiento subterráneo.</li>
            </ul>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>3.3 Control de Terceros, Subcontratistas y Proveedores</h3>
            <p>Bajo el principio de responsabilidad solidaria (Art. 68 Ley 29783 y Cláusula 8.1.4 ISO 45001), todo proveedor o subcontratista pasa por homologación previa: historial de siniestralidad de 3 años, pólizas <b>SCTR Salud y Pensión</b> vigentes, PETS/IPERC aprobados, EMO homologado por Volcan e inducción obligatoria Anexos 4 y 5.</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>3.5 Plan de Preparación y Respuesta a Emergencias (COMM.SSGAC.PPREC.01)</h3>
            <ul>
                <li><b>Niveles de Alerta:</b> <b>Nivel 1 (Amarilla - Menor)</b> control local con extintor/botiquín; <b>Nivel 2 (Anaranjada - Moderada)</b> intervención de Brigada interna COMM; <b>Nivel 3 (Roja - Crítica)</b> activación de Brigada de Rescate Minero de Volcan, Bomberos (116) y ambulancias.</li>
                <li><b>Canales de Alerta (24 h):</b> Central de Emergencias Volcan <b>Anexo 7911</b> y radio troncalizada de Seguridad Mina.</li>
                <li><b>Protocolos Específicos:</b> Incendios eléctricos (corte de energía + extintor CO<sub>2</sub>/PQS), tormentas eléctricas en superficie (refugio en vehículos/jaula Faraday ante Alerta Roja), gaseamiento/derrumbes (repliegue a Refugio Minero) y <b>Rescate en Altura (COMM.SSOMA.PC.01)</b> con tiempo máximo de rescate de <b>15 minutos</b> para prevenir el Síndrome del Arnés.</li>
            </ul>
        </div>
        """

    def obtener_contenido_cap4_5(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>4.1 Auditorías Internas y 4.4 Revisión por la Alta Dirección</h3>
            <ul>
                <li><b>Auditorías Internas (ISO 45001 / Art. 43 Ley 29783):</b> Ejecutadas como mínimo 1 vez al año por auditores independientes (meta de cumplimiento: <b>100%</b>), clasificando hallazgos en Conformidades, No Conformidades Menores, No Conformidades Mayores y Oportunidades de Mejora.</li>
                <li><b>Acciones Correctivas y Preventivas (SAC / SAP):</b> Protocolo de 4 fases (Contención inmediata &rarr; Análisis de Causa Raíz mediante 5 Porqués / Ishikawa &rarr; Plan de acción en 48-72 h para críticos o 15 días para medios &rarr; Verificación de eficacia en terreno a los 30-60 días).</li>
                <li><b>Revisión por la Alta Dirección:</b> Conducida anualmente por el Gerente General y CEO Director para evaluar KPIs, cumplimiento legal, auditorías y asignar nuevos recursos presupuestales.</li>
            </ul>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>4.2 Investigación de Incidentes y Accidentes (Formato REG-COM-COP-05)</h3>
            <p>Notificación inmediata en campo al Supervisor de Turno y SST. Accidentes mortales e incidentes peligrosos se reportan en un plazo máximo de <b>24 horas</b> al MTPE y MINEM/Osinergmin (plataforma SAT) y a Volcan. Se aplica el <b>Modelo Causal de Pérdidas de Frank Bird</b> (Falta de Control &rarr; Causas Básicas &rarr; Causas Inmediatas), los 5 Porqués y el Árbol de Causas.</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>5. Consolidación de los 8 Registros Obligatorios del SGSST (R.M. 050-2013-TR)</h3>
            <table border='1' cellpadding='5' cellspacing='0' style='border-collapse:collapse; width:100%; border-color:{GRIS_BORDE};'>
                <tr style='background-color:{AZUL_SUAVE}; font-weight:bold; color:{AZUL_OSCURO};'>
                    <td>N.°</td><td>Registro Obligatorio</td><td>Plazo Legal de Custodia</td><td>Responsable / Formato</td>
                </tr>
                <tr><td>5.1</td><td>Accidentes de Trabajo, Incidentes Peligrosos e Incidentes</td><td><b>10 años</b></td><td>Área de SST (REG-COM-COP-05)</td></tr>
                <tr><td>5.2</td><td>Enfermedades Ocupacionales</td><td><b>20 años</b></td><td>Médico Ocupacional (Confidencial)</td></tr>
                <tr><td>5.3</td><td>Exámenes Médicos Ocupacionales (EMO)</td><td><b>20 años</b></td><td>Área de SST / Servicio Médico</td></tr>
                <tr><td>5.4</td><td>Monitoreos de Agentes Ocupacionales (Ruido, Luz, Ergonomía, Psicosocial)</td><td><b>20 años</b></td><td>Área de SST</td></tr>
                <tr><td>5.5</td><td>Inspecciones Internas de Seguridad y Salud en el Trabajo</td><td><b>5 años</b></td><td>Supervisores / SST (REG-TA-GLO-08-07)</td></tr>
                <tr><td>5.6</td><td>Estadísticas de Seguridad y Salud (LTIFR, DSIFR, TRIFR, HHT)</td><td><b>5 años</b></td><td>Área de SST / CSST</td></tr>
                <tr><td>5.7</td><td>Equipos de Seguridad o Emergencia (Entrega de EPP)</td><td><b>5 años</b></td><td>Área de SST (PR-SSOMA-04)</td></tr>
                <tr><td>5.8</td><td>Inducción, Capacitación, Entrenamiento y Simulacros</td><td><b>5 años</b></td><td>Supervisores / Área de SST</td></tr>
            </table>
        </div>
        """

    def obtener_contenido_cap6_7(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>6. Conclusión General del Plan Anual de SST</h3>
            <p>El Plan y Programa Anual de Seguridad y Salud en el Trabajo de <b>Communications and Systems Development S.A.C. (COMM)</b> establece una hoja de ruta técnica, preventiva y auditable que garantiza operaciones seguras en la Unidad Minera San Cristóbal - Carahuacra bajo cumplimiento estricto de la <b>Ley N.° 29783</b>, su Reglamento (<b>D.S. N.° 005-2012-TR</b>) y el Reglamento de Seguridad y Salud Ocupacional en Minería (<b>D.S. N.° 024-2016-EM</b> y modificatoria <b>D.S. N.° 023-2017-EM</b>).</p>
            <p>Mediante la articulación entre la evaluación continua de peligros (IPERC Línea Base y Continuo), la estandarización operativa con los procedimientos <b>PETS-COM-MIN-01 al 08</b>, el control de trabajos críticos mediante <b>PETAR</b>, la ejecución de 120 inspecciones anuales, la vigilancia médica ocupacional y el seguimiento de los 8 registros obligatorios, se consolida una cultura preventiva orientada al objetivo institucional de <b>cero daños</b>.</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {AZUL_OSCURO}; margin-bottom: 4px;'>7. Anexos y Programas Presupuestados del Sistema de Gestión SST</h3>
            <ul>
                <li><b>Anexo 1:</b> Matriz de Objetivos Específicos, Metas e Indicadores Operativos de Seguridad y Liderazgo en Campo.</li>
                <li><b>Anexo 2:</b> Programa Anual de Capacitaciones 2025 (49 temas programados, meta &ge; 90%, presupuesto S/ 3,500.00) y Campañas de Seguridad (Cuidado de Ojos, Oído y Manos - presupuesto S/ 600.00).</li>
                <li><b>Anexo 3:</b> Programa Anual de Inspecciones Internas 2025 (10 categorías &times; 12 meses = 120 inspecciones, meta 100%, presupuesto S/ 1,000.00).</li>
                <li><b>Anexo 4:</b> Programa de Seguimiento de Herramientas de Gestión (OPT, ACS/IPS, IPERC Continuo - S/ 400.00), Programa de Simulacros Multipeligro y Rescate en Altura (S/ 600.00), Programa de Auditorías Internas y Externas (S/ 2,000.00), Programa de Monitoreo de Salud e Higiene Ocupacional (EMO, ruido, iluminación, gases NO<sub>2</sub>/CO<sub>2</sub>/CO/H<sub>2</sub>S, ergonomía y psicosocial - S/ 5,000.00) y Programa de Visitas Gerenciales (S/ 2,000.00).</li>
                <li><b>Documentos Complementarios Integrados:</b> <b>MDR</b> (Mapa de Riesgos de las instalaciones y frentes) y <b>RISST</b> (Reglamento Interno de Seguridad y Salud en el Trabajo).</li>
            </ul>
        </div>
        """


# ==========================================================
# 12. EJECUCIÓN DEL APLICATIVO
# ==========================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ventana = VentanaPlanSeguridad()
    ventana.show()
    sys.exit(app.exec())
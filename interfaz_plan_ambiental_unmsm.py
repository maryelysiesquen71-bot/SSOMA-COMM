# -*- coding: utf-8 -*-
"""
========================================================================================
PLAN DE MANEJO AMBIENTAL (PMA) - UNMSM | EPISST
CURSO: Prevención y Control de Riesgos Laborales y Ambientales
GRUPO 8 | EMPRESA: Communications and Systems Development SAC (COMM)
DOCENTE: Dr. Edito Luis Rojas Linares
FUENTE DOCUMENTAL: ambiental.pdf
DOCUMENTOS ADJUNTOS: Controles AM, EVAAMAM, EVAL, EVASOAM, MITI, PRAM, PSIG
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
    QGridLayout,
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
# 1. CONFIGURACIÓN GENERAL Y PALETA DE COLORES (AMBIENTAL)
# ==========================================================

CARPETA = Path(__file__).parent.resolve() if "__file__" in locals() else Path.cwd()

# Paleta Institucional Verde Bosque / Ambiental Ecológica
VERDE_OSCURO = "#1B4D3E"      # Verde bosque profundo institucional
VERDE_ACCENTO = "#2D6A4F"     # Verde esmeralda medio
VERDE_CLARO = "#52B788"       # Verde vibrante de resalte
VERDE_SUAVE = "#E8F5E9"       # Fondo suave verde para tarjetas
VERDE_HEADER = "#13382C"      # Verde muy oscuro para menubar

AZUL_PETROLEO = "#102A43"
DORADO_UNMSM = "#B45309"
GRIS_FONDO = "#F4F6F9"
BLANCO = "#FFFFFF"
GRIS_BORDE = "#C8D6CF"
TEXTO_PRINCIPAL = "#1F2937"
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


# Búsqueda de recursos gráficos (mismos nombres de archivo)
RUTA_FOTO_GRUPAL = buscar_archivo("foto_grupal")
RUTA_LOGO_FII = buscar_archivo("logoFII")
RUTA_LOGO_EPISST = buscar_archivo("logoEPISST")
RUTA_COMM = buscar_archivo("COMM")

# Búsqueda de documentos técnicos (PDF / imágenes / Office)
EXTS_DOCS = [".pdf", ".PDF", ".png", ".jpg", ".jpeg", ".xlsx", ".docx"]
RUTA_DOC_AMBIENTAL = buscar_archivo("ambiental", EXTS_DOCS)
RUTA_DOC_CONTROLES_AM = buscar_archivo("Controles AM", EXTS_DOCS)
RUTA_DOC_EVAAMAM = buscar_archivo("EVAAMAM", EXTS_DOCS)
RUTA_DOC_EVAL = buscar_archivo("EVAL", EXTS_DOCS)
RUTA_DOC_EVASOAM = buscar_archivo("EVASOAM", EXTS_DOCS)
RUTA_DOC_MITI = buscar_archivo("MITI", EXTS_DOCS)
RUTA_DOC_PRAM = buscar_archivo("PRAM", EXTS_DOCS)
RUTA_DOC_PSIG = buscar_archivo("PSIG", EXTS_DOCS)


# ==========================================================
# 2. VENTANA PRINCIPAL PyQt6
# ==========================================================

class VentanaPlanAmbiental(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Plan de Manejo Ambiental (PMA) - UNMSM | EPISST | Grupo 8")
        self.resize(1340, 960)
        self.setMinimumSize(1020, 740)

        self.imagenes_redimensionables = []

        self.crear_menu()
        self.crear_interfaz()

        estilo_ventana = (
            f"QMainWindow {{ background-color: {VERDE_OSCURO}; }} "
            f"QMenuBar {{ background-color: {VERDE_HEADER}; color: #F8FAFC; padding: 6px; font-size: 13px; font-weight: 600; }} "
            f"QMenuBar::item {{ background: transparent; padding: 6px 14px; border-radius: 4px; }} "
            f"QMenuBar::item:selected {{ background-color: {VERDE_ACCENTO}; }} "
            f"QMenu {{ background-color: {BLANCO}; color: {TEXTO_PRINCIPAL}; border: 1px solid {GRIS_BORDE}; }} "
            f"QMenu::item {{ padding: 8px 24px; font-size: 12px; }} "
            f"QMenu::item:selected {{ background-color: {VERDE_SUAVE}; color: {VERDE_OSCURO}; font-weight: bold; }} "
            f"QScrollArea {{ border: none; background-color: {VERDE_OSCURO}; }} "
            f"QScrollBar:vertical {{ background: #0E271F; width: 10px; margin: 0px; }} "
            f"QScrollBar::handle:vertical {{ background: {VERDE_ACCENTO}; min-height: 25px; border-radius: 5px; }}"
        )
        self.setStyleSheet(estilo_ventana)

    # ======================================================
    # 3. MENÚ SUPERIOR INTERACTIVO
    # ======================================================

    def crear_menu(self):
        barra = self.menuBar()

        menu_inicio = barra.addMenu("Inicio")
        menu_capitulos = barra.addMenu("Capítulos del Plan Ambiental")
        menu_documentos = barra.addMenu("Documentos Adjuntos (7 Anexos Técnicos)")
        menu_anexos = barra.addMenu("Cronograma y Anexos")
        menu_ayuda = barra.addMenu("Ayuda")

        # Inicio
        accion_portada = QAction("Portada Oficial del Plan de Manejo Ambiental", self)
        accion_portada.triggered.connect(lambda: self.cambiar_vista(0))
        menu_inicio.addAction(accion_portada)

        menu_inicio.addSeparator()
        accion_salir = QAction("Salir del Aplicativo", self)
        accion_salir.triggered.connect(self.close)
        menu_inicio.addAction(accion_salir)

        # Capítulos del Plan de Manejo Ambiental (ambiental.pdf)
        secciones = [
            ("Capítulo 1: Introducción, Diagnóstico de 4 Brechas, Objetivos, Alcance y Marco Legal", 1),
            ("Capítulo 2: Descripción del Proyecto, Política RD-PL-01 v.08 y Línea Base", 2),
            ("Capítulo 3: Identificación y Evaluación Cuantitativa de 12 Impactos (S × P)", 3),
            ("Capítulo 4, 5 y 6: Programas Ambientales (PMIR, RAEE), KPIs y Auditorías", 4),
            ("Capítulo 7 y 8: Cronograma 12 Meses, Presupuesto ($10,800) y Anexos", 5),
        ]
        for titulo_sec, idx in secciones:
            act = QAction(titulo_sec, self)
            act.triggered.connect(lambda checked, i=idx: self.cambiar_vista(i))
            menu_capitulos.addAction(act)

        # Documentos Adjuntos (Controles AM, EVAAMAM, EVAL, EVASOAM, MITI, PRAM, PSIG)
        accion_panel_docs = QAction("Panel de Visor Documental Completo", self)
        accion_panel_docs.triggered.connect(lambda: self.cambiar_vista(6))
        menu_documentos.addAction(accion_panel_docs)

        menu_documentos.addSeparator()

        docs_menu = [
            ("Abrir Controles AM (Niveles de Control Residual)", RUTA_DOC_CONTROLES_AM, "Controles AM"),
            ("Abrir EVAAMAM (Evaluación del Riesgo Ambiental)", RUTA_DOC_EVAAMAM, "EVAAMAM"),
            ("Abrir EVAL (Clasificación de Riesgo Residual A–E)", RUTA_DOC_EVAL, "EVAL"),
            ("Abrir EVASOAM (Evaluación de Riesgo de Salud)", RUTA_DOC_EVASOAM, "EVASOAM"),
            ("Abrir MITI (Matriz de Control y Mitigación SSOMAC)", RUTA_DOC_MITI, "MITI"),
            ("Abrir PRAM (Programa Anual de Gestión Ambiental 2025)", RUTA_DOC_PRAM, "PRAM"),
            ("Abrir PSIG (Política Integrada de Gestión RD-PL-01)", RUTA_DOC_PSIG, "PSIG"),
        ]
        for etiqueta_m, ruta_m, nombre_m in docs_menu:
            act_doc = QAction(etiqueta_m, self)
            act_doc.triggered.connect(lambda checked, r=ruta_m, n=nombre_m: self.abrir_documento_externo(r, n))
            menu_documentos.addAction(act_doc)

        menu_documentos.addSeparator()
        act_base = QAction("Abrir Documento Base Completo (ambiental.pdf)", self)
        act_base.triggered.connect(lambda: self.abrir_documento_externo(RUTA_DOC_AMBIENTAL, "ambiental"))
        menu_documentos.addAction(act_base)

        # Cronograma y Anexos
        accion_anexos = QAction("Ver Cronograma Maestro, Presupuesto y Anexos", self)
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
        self.contenido.setStyleSheet(f"background-color: {VERDE_OSCURO};")
        self.scroll.setWidget(self.contenido)

        self.layout_principal = QVBoxLayout(self.contenido)
        self.layout_principal.setContentsMargins(24, 16, 24, 28)
        self.layout_principal.setSpacing(18)

        # Banner Panorámico estilo Notion con foto_grupal
        self.crear_banner_notion()

        # Pila de Vistas (QStackedWidget)
        self.vistas_stack = QStackedWidget()
        self.layout_principal.addWidget(self.vistas_stack)

        # Construir cada vista
        self.vista_portada = self.construir_pagina_portada()
        self.vista_cap1 = self.construir_pagina_documento(
            "CAPÍTULO 1: INTRODUCCIÓN, BRECHAS DETECTADAS, OBJETIVOS, ALCANCE Y MARCO LEGAL",
            self.obtener_contenido_cap1()
        )
        self.vista_cap2 = self.construir_pagina_documento(
            "CAPÍTULO 2: DESCRIPCIÓN DEL PROYECTO, POLÍTICA RD-PL-01 v.08 Y LÍNEA BASE SOCIOAMBIENTAL",
            self.obtener_contenido_cap2()
        )
        self.vista_cap3 = self.construir_pagina_documento(
            "CAPÍTULO 3: IDENTIFICACIÓN Y EVALUACIÓN DE IMPACTOS AMBIENTALES (12 ASPECTOS | S × P)",
            self.obtener_contenido_cap3()
        )
        self.vista_cap4_5_6 = self.construir_pagina_documento(
            "CAPÍTULOS 4, 5 Y 6: PROGRAMAS AMBIENTALES (PMIR, RAEE), KPIs Y AUDITORÍAS",
            self.obtener_contenido_cap4_5_6()
        )
        self.vista_cap7_8 = self.construir_pagina_documento(
            "CAPÍTULOS 7 Y 8: CRONOGRAMA DE 12 MESES, PRESUPUESTO ($10,800) Y ANEXOS",
            self.obtener_contenido_cap7_8()
        )
        self.vista_documentos_externos = self.construir_pagina_documentos_externos()

        self.vistas_stack.addWidget(self.vista_portada)             # 0
        self.vistas_stack.addWidget(self.vista_cap1)                # 1
        self.vistas_stack.addWidget(self.vista_cap2)                # 2
        self.vistas_stack.addWidget(self.vista_cap3)                # 3
        self.vistas_stack.addWidget(self.vista_cap4_5_6)            # 4
        self.vistas_stack.addWidget(self.vista_cap7_8)              # 5
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
            f"border-top-left-radius: 13px; border-top-right-radius: 13px; border-bottom: 3px solid {VERDE_CLARO}; overflow: hidden;"
        )

        if RUTA_FOTO_GRUPAL:
            pix = QPixmap(str(RUTA_FOTO_GRUPAL))
            if not pix.isNull():
                self.imagenes_redimensionables.append((self.label_cover, pix))
                self.actualizar_imagen_banner(self.label_cover, pix)
            else:
                self.label_cover.setText("Error al abrir archivo 'foto_grupal'")
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
        lbl_univ.setStyleSheet(f"color: {VERDE_OSCURO}; font-size: 15px; font-weight: 900; letter-spacing: 0.5px;")

        lbl_decana = QLabel("(Universidad del Perú, DECANA DE AMÉRICA) • FACULTAD DE INGENIERÍA INDUSTRIAL")
        lbl_decana.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_decana.setStyleSheet(f"color: {DORADO_UNMSM}; font-size: 11px; font-weight: 700; font-style: italic;")

        lbl_escuela = QLabel("Escuela Profesional de Ingeniería de Seguridad y Salud en el Trabajo (EPISST)")
        lbl_escuela.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_escuela.setStyleSheet(f"color: {VERDE_ACCENTO}; font-size: 12px; font-weight: 800;")

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

        # 3. Franja del Título del Plan de Manejo Ambiental
        lbl_lema = QLabel("PLAN DE MANEJO AMBIENTAL (PMA)  |  U.M. SAN CRISTÓBAL - CARAHUACRA (VOLCAN COMPAÑÍA MINERA S.A.A.)")
        lbl_lema.setAlignment(Qt.AlignmentFlag.AlignCenter)
        lbl_lema.setStyleSheet(
            f"QLabel {{ background-color: {VERDE_SUAVE}; color: {VERDE_OSCURO}; border: 1px solid {VERDE_CLARO}; "
            f"border-radius: 8px; padding: 7px 12px; font-size: 12.5px; font-weight: 800; margin: 4px 18px 0px 18px; }}"
        )
        layout_banner_general.addWidget(lbl_lema)

        self.layout_principal.addWidget(contenedor_banner)

    # ======================================================
    # 6. PORTADA INTERACTIVA CON INTEGRANTES Y ACCESOS DIRECTOS
    # ======================================================

    def construir_pagina_portada(self):
        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            f"QFrame {{ background-color: {BLANCO}; border-radius: 12px; border: 1px solid {GRIS_BORDE}; }}"
        )

        layout_general = QVBoxLayout(tarjeta)
        layout_general.setContentsMargins(22, 18, 22, 22)
        layout_general.setSpacing(16)

        titulo = QLabel("PORTADA OFICIAL: PLAN DE MANEJO AMBIENTAL (FUENTE: ambiental.pdf)")
        titulo.setStyleSheet(
            f"QLabel {{ color: {VERDE_OSCURO}; font-size: 15px; font-weight: 800; "
            f"letter-spacing: 0.6px; padding-bottom: 6px; border-bottom: 2px solid {VERDE_CLARO}; }}"
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
        lbl_tit_datos.setStyleSheet(f"color: {VERDE_OSCURO}; font-size: 12px; font-weight: 900; border: none; background: transparent;")
        layout_datos.addWidget(lbl_tit_datos)

        datos = [
            ("CURSO", "Prevención y Control de Riesgos Laborales y Ambientales"),
            ("DOCENTE", "Dr. Edito Luis Rojas Linares"),
            ("EMPRESA CONTRATISTA", "Communications and Systems Development S.A.C. (COMM)"),
            ("OPERACIÓN Y CUENCA", "U.M. San Cristóbal - Carahuacra (Volcan) | Subcuenca alta del río Yauli (4,000 - 4,700 m.s.n.m.)"),
            ("LUGAR Y AÑO", "LIMA – PERÚ | 2026"),
        ]

        for etiqueta, valor in datos:
            fila = QFrame()
            fila.setStyleSheet(
                f"QFrame {{ background-color: {BLANCO}; border: 1px solid #E2E8F0; "
                f"border-left: 4px solid {VERDE_ACCENTO}; border-radius: 6px; }}"
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

        # Columna Derecha: Integrantes del Grupo 8 y Botones de Acceso Rápido
        columna_derecha = QVBoxLayout()
        columna_derecha.setSpacing(12)

        marco_grupo = QFrame()
        marco_grupo.setStyleSheet(f"QFrame {{ background-color: {GRIS_FONDO}; border: 1px solid {GRIS_BORDE}; border-radius: 10px; }}")
        layout_grupo = QVBoxLayout(marco_grupo)
        layout_grupo.setContentsMargins(16, 12, 16, 12)
        layout_grupo.setSpacing(7)

        lbl_tit_grupo = QLabel("GRUPO 8 — INTEGRANTES EPISST")
        lbl_tit_grupo.setStyleSheet(f"color: {VERDE_OSCURO}; font-size: 12px; font-weight: 900; border: none; background: transparent;")
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
                f"border-left: 4px solid {VERDE_CLARO}; border-radius: 6px; }}"
            )
            f_item = QHBoxLayout(fila_int)
            f_item.setContentsMargins(10, 5, 10, 5)

            lbl_n = QLabel(f"• {nombre}")
            lbl_n.setStyleSheet(f"color: {TEXTO_PRINCIPAL}; font-size: 12px; font-weight: 600; border: none; background: transparent;")
            lbl_c = QLabel(codigo)
            lbl_c.setStyleSheet(f"color: {VERDE_ACCENTO}; font-size: 11.5px; font-weight: 800; border: none; background: transparent;")

            f_item.addWidget(lbl_n)
            f_item.addStretch()
            f_item.addWidget(lbl_c)
            layout_grupo.addWidget(fila_int)

        columna_derecha.addWidget(marco_grupo)

        # Tarjeta de Acceso Directo a los 7 Documentos Complementarios
        marco_docs = QFrame()
        marco_docs.setStyleSheet(f"QFrame {{ background-color: {VERDE_SUAVE}; border: 1.5px solid {VERDE_CLARO}; border-radius: 10px; }}")
        layout_docs = QVBoxLayout(marco_docs)
        layout_docs.setContentsMargins(14, 10, 14, 10)
        layout_docs.setSpacing(8)

        lbl_docs_tit = QLabel("ACCESO DIRECTO A DOCUMENTOS COMPLEMENTARIOS SSOMAC")
        lbl_docs_tit.setStyleSheet(f"color: {VERDE_OSCURO}; font-size: 11.5px; font-weight: 900; border: none; background: transparent;")
        layout_docs.addWidget(lbl_docs_tit)

        grid_botones = QGridLayout()
        grid_botones.setSpacing(6)

        botones_rapidos = [
            ("Controles AM", RUTA_DOC_CONTROLES_AM, "Controles AM", VERDE_ACCENTO, 0, 0),
            ("EVAAMAM", RUTA_DOC_EVAAMAM, "EVAAMAM", VERDE_OSCURO, 0, 1),
            ("EVAL", RUTA_DOC_EVAL, "EVAL", AZUL_PETROLEO, 0, 2),
            ("EVASOAM", RUTA_DOC_EVASOAM, "EVASOAM", VERDE_ACCENTO, 1, 0),
            ("MITI", RUTA_DOC_MITI, "MITI", DORADO_UNMSM, 1, 1),
            ("PRAM", RUTA_DOC_PRAM, "PRAM", VERDE_OSCURO, 1, 2),
            ("PSIG", RUTA_DOC_PSIG, "PSIG", AZUL_PETROLEO, 2, 0),
            ("Ver Todos (7)", None, "PANEL", "#065F46", 2, 1),
        ]

        for texto_b, ruta_b, nom_b, color_b, fila_g, col_g in botones_rapidos:
            btn = QPushButton(texto_b)
            btn.setCursor(Qt.CursorShape.PointingHandCursor)
            btn.setStyleSheet(
                f"QPushButton {{ background-color: {color_b}; color: {BLANCO}; border-radius: 5px; padding: 6px 8px; font-weight: bold; font-size: 11.5px; }} "
                f"QPushButton:hover {{ opacity: 0.88; }}"
            )
            if nom_b == "PANEL":
                btn.clicked.connect(lambda: self.cambiar_vista(6))
            else:
                btn.clicked.connect(lambda checked, r=ruta_b, n=nom_b: self.abrir_documento_externo(r, n))
            grid_botones.addWidget(btn, fila_g, col_g)

        layout_docs.addLayout(grid_botones)
        columna_derecha.addWidget(marco_docs)

        columnas.addLayout(columna_derecha, stretch=1)
        layout_general.addLayout(columnas)

        # Nota de navegación
        nota_nav = QLabel("🌱 Navega por los capítulos del Plan de Manejo Ambiental (ambiental.pdf) o abre cualquiera de los 7 documentos adjuntos desde el menú superior o los accesos directos.")
        nota_nav.setAlignment(Qt.AlignmentFlag.AlignCenter)
        nota_nav.setStyleSheet(f"background-color: {VERDE_SUAVE}; color: {VERDE_OSCURO}; border: 1px dashed {VERDE_CLARO}; border-radius: 6px; padding: 8px; font-size: 12px; font-weight: 700;")
        layout_general.addWidget(nota_nav)

        return tarjeta

    # ======================================================
    # 7. PÁGINA VISOR DE DOCUMENTOS COMPLEMENTARIOS (7 ANEXOS + BASE)
    # ======================================================

    def construir_pagina_documentos_externos(self):
        tarjeta = QFrame()
        tarjeta.setStyleSheet(
            f"QFrame {{ background-color: {BLANCO}; border-radius: 12px; border: 1px solid {GRIS_BORDE}; }}"
        )
        layout = QVBoxLayout(tarjeta)
        layout.setContentsMargins(24, 20, 24, 22)
        layout.setSpacing(12)

        lbl_tit = QLabel("GESTOR DE DOCUMENTOS AMBIENTALES Y SSOMAC (7 DOCUMENTOS ADJUNTOS + BASE)")
        lbl_tit.setStyleSheet(
            f"QLabel {{ color: {VERDE_OSCURO}; font-size: 15px; font-weight: 900; "
            f"letter-spacing: 0.5px; padding-bottom: 6px; border-bottom: 2px solid {VERDE_CLARO}; }}"
        )
        layout.addWidget(lbl_tit)

        desc = QLabel(
            "Haz clic en el botón de cada documento para abrirlo directamente en su visor predeterminado:"
        )
        desc.setWordWrap(True)
        desc.setStyleSheet(f"color: {TEXTO_PRINCIPAL}; font-size: 13px; border: none;")
        layout.addWidget(desc)

        documentos_info = [
            (
                "1. Controles AM (Niveles de Control sobre Riesgo Residual)",
                "Jerarquía de controles según nivel residual (A: Estudios Urgentes >1000, B: Bloqueo Físico 700–999, C: Documentación Formal 400–699, D: Procedimiento Operacional 100–399, E: Tolerar <99).",
                RUTA_DOC_CONTROLES_AM,
                "Controles AM",
                VERDE_ACCENTO,
            ),
            (
                "2. EVAAMAM (Evaluación del Riesgo Ambiental - Criterios SEV × PROB × EXP)",
                "Tabla oficial de ponderación de Severidad ambiental (4 a 64: No Significativo hasta Catastrófico), Probabilidad (2 a 32) y Exposición legal/imagen (1 a 5).",
                RUTA_DOC_EVAAMAM,
                "EVAAMAM",
                VERDE_OSCURO,
            ),
            (
                "3. EVAL (Clasificación de Tipo de Riesgo Residual A–E)",
                "Matriz de categorización del Riesgo Residual: Tipo A Intolerable (>1000), Tipo B Muy Alto (700–999), Tipo C Alto (400–699), Tipo D Medio (100–399) y Tipo E Bajo (<99).",
                RUTA_DOC_EVAL,
                "EVAL",
                AZUL_PETROLEO,
            ),
            (
                "4. EVASOAM (Evaluación de Riesgo de Salud Ocupacional)",
                "Escalas de Severidad médica (4 a 64), Probabilidad de ocurrencia (2 a 32) y Exposición respecto al Límite de Exposición Ocupacional LEO (1 a 5).",
                RUTA_DOC_EVASOAM,
                "EVASOAM",
                VERDE_ACCENTO,
            ),
            (
                "5. MITI (Matriz de Control y Mitigación SSOMAC)",
                "Estándares de mitigación por nivel A–E (99% a 3%) en 6 ejes: Equipo/Tecnología, Monitoreo/Mantenimiento, Personal/Entrenamiento, Método/PETS, Gerenciamiento y No Conformidades.",
                RUTA_DOC_MITI,
                "MITI",
                DORADO_UNMSM,
            ),
            (
                "6. PRAM (Programa Anual de Gestión Ambiental 2025 - COMM)",
                "Cronograma mensual programado y ejecutado (Ene–Dic 2025) de 12 capacitaciones ambientales, 24 inspecciones (internas y cruzadas), kits antiderrame, simulacros y residuos sólidos.",
                RUTA_DOC_PRAM,
                "PRAM",
                VERDE_OSCURO,
            ),
            (
                "7. PSIG (Política Integrada de Gestión RD-PL-01 Versión 08)",
                "Política corporativa trinorma (ISO 9001, ISO 14001, ISO 45001) firmada el 15/10/2025 por Filiberto Revilla (CEO) y Sergio Gonzales (Gerente General).",
                RUTA_DOC_PSIG,
                "PSIG",
                AZUL_PETROLEO,
            ),
            (
                "8. Documento Base Completo: Plan de Manejo Ambiental (ambiental.pdf)",
                "Informe técnico integral de 256 páginas con diagnóstico de 4 brechas, línea base física/biológica/social de Yauli, 12 aspectos ambientales, PMIR, RAEE y presupuesto ($10,800.00 USD).",
                RUTA_DOC_AMBIENTAL,
                "ambiental",
                "#065F46",
            ),
        ]

        for titulo_doc, detalle_doc, ruta_doc, nombre_corto, color_btn in documentos_info:
            card_doc = QFrame()
            card_doc.setStyleSheet(
                f"QFrame {{ background-color: {GRIS_FONDO}; border: 1px solid {GRIS_BORDE}; "
                f"border-left: 5px solid {color_btn}; border-radius: 8px; }}"
            )
            l_card = QHBoxLayout(card_doc)
            l_card.setContentsMargins(14, 10, 14, 10)
            l_card.setSpacing(14)

            l_texto = QVBoxLayout()
            l_texto.setSpacing(3)

            t_lbl = QLabel(titulo_doc)
            t_lbl.setStyleSheet(f"color: {VERDE_OSCURO}; font-size: 13.5px; font-weight: 800; border: none; background: transparent;")

            d_lbl = QLabel(detalle_doc)
            d_lbl.setWordWrap(True)
            d_lbl.setStyleSheet(f"color: {TEXTO_PRINCIPAL}; font-size: 12px; border: none; background: transparent;")

            estado_txt = f"Archivo detectado: {ruta_doc.name}" if ruta_doc else f"Archivo '{nombre_corto}' pendiente en la carpeta del proyecto"
            estado_color = "#15803D" if ruta_doc else "#B91C1C"
            e_lbl = QLabel(estado_txt)
            e_lbl.setStyleSheet(f"color: {estado_color}; font-size: 11px; font-weight: 700; border: none; background: transparent;")

            l_texto.addWidget(t_lbl)
            l_texto.addWidget(d_lbl)
            l_texto.addWidget(e_lbl)

            btn_abrir = QPushButton(f"Abrir {nombre_corto}")
            btn_abrir.setFixedSize(150, 38)
            btn_abrir.setCursor(Qt.CursorShape.PointingHandCursor)
            btn_abrir.setStyleSheet(
                f"QPushButton {{ background-color: {color_btn}; color: {BLANCO}; border-radius: 8px; font-weight: bold; font-size: 12px; }} "
                f"QPushButton:hover {{ opacity: 0.9; }}"
            )
            btn_abrir.clicked.connect(lambda checked, r=ruta_doc, n=nombre_corto: self.abrir_documento_externo(r, n))

            l_card.addLayout(l_texto, stretch=4)
            l_card.addWidget(btn_abrir, stretch=0)
            layout.addWidget(card_doc)

        return tarjeta

    def abrir_documento_externo(self, ruta, nombre_doc):
        if ruta is None or not ruta.exists():
            QMessageBox.warning(
                self,
                "Archivo no encontrado",
                f"No se encontró el archivo '{nombre_doc}' en la carpeta del proyecto:\n{CARPETA}\n\n"
                f"Verifica que '{nombre_doc}.pdf' (o .png/.jpg/.xlsx/.docx) esté guardado en la misma carpeta."
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
            f"QLabel {{ color: {VERDE_OSCURO}; font-size: 15px; font-weight: 900; "
            f"letter-spacing: 0.5px; padding-bottom: 6px; border-bottom: 2px solid {VERDE_CLARO}; }}"
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
            "color: #D8F3DC; font-size: 11px; font-weight: 700; letter-spacing: 1px; padding: 4px;"
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
            "Acerca del Plan de Manejo Ambiental (PMA)",
            "Plan de Manejo Ambiental Integral (PMA)\n"
            "Documento Fuente: ambiental.pdf\n"
            "Documentos Adjuntos: Controles AM, EVAAMAM, EVAL, EVASOAM, MITI, PRAM y PSIG\n"
            "Curso: Prevención y Control de Riesgos Laborales y Ambientales\n"
            "Escuela Profesional de Ingeniería de Seguridad y Salud en el Trabajo (EPISST)\n"
            "Facultad de Ingeniería Industrial - UNMSM\n\n"
            "Docente: Dr. Edito Luis Rojas Linares\n"
            "Grupo 8 | Empresa: Communications and Systems Development SAC (COMM)\n"
            "Operación: U.M. San Cristóbal - Carahuacra (Volcan Cía. Minera S.A.A.)\n"
            "Año Académico: 2026",
        )

    # ======================================================
    # 11. CONTENIDO FORMALIZADO DEL DOCUMENTO BASE (ambiental.pdf)
    # ======================================================

    def obtener_contenido_cap1(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>1.1 Presentación y Diagnóstico de 4 Brechas Críticas</h3>
            <p><b>Communications and Systems Development S.A.C. (COMM)</b> —con 14 años de trayectoria, más de 1,000 proyectos y certificación trinorma <b>ISO 9001:2015, ISO 14001:2015 e ISO 45001:2018</b>, además de Huella de Carbono Perú (MINAM), ESR, ABE y GPTW— ejecuta servicios de redes, fibra óptica, cable radiante (Leaky Feeder) y SCADA en la <b>Unidad Minera San Cristóbal - Carahuacra</b> de <b>Volcan Compañía Minera S.A.A.</b> (Yauli, Junín, 4,000 a 4,700 m.s.n.m., subcuenca alta del río Yauli).</p>
            <p>La evaluación académica UNMSM del programa precursor (<b>PL-COMM-GLO-08-01 v.01</b>) detectó <b>4 brechas críticas</b> subsanadas por este PMA Integral:</p>
            <ol>
                <li><b>Insuficiente caracterización de la línea base socioambiental:</b> Omitía receptores sensibles como bofedales altoandinos, fuentes hídricas glaciares y pastizales de puna.</li>
                <li><b>Limitaciones de la metodología de evaluación:</b> Carecía de matriz cuantitativa (S &times; P) para jerarquizar gasto y controles prioritarios.</li>
                <li><b>Ausencia total de procedimiento para RAEE:</b> Omitía la gestión de switches, routers, baterías UPS y módulos SFP bajo el <b>D.S. 009-2019-MINAM</b>.</li>
                <li><b>Desarticulación entre SST (Ley 29783) e ISO 14001:2015:</b> Aislaba los riesgos físicos/químicos ocupacionales del impacto sobre suelo, agua y aire.</li>
            </ol>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>1.6 Objetivos del Plan de Manejo Ambiental</h3>
            <p><b>Objetivo General:</b> Establecer, ejecutar y fiscalizar los lineamientos, programas de ingeniería, manejo de residuos y protocolos de contingencia para prevenir, mitigar y controlar los impactos ambientales derivados de los servicios de telecomunicaciones de COMM en interior mina y superficie.</p>
            <ul>
                <li><b>OE-1:</b> Valorar cuantitativamente los 12 aspectos ambientales mediante Matriz de Importancia (S &times; P) bajo ISO 14001:2015.</li>
                <li><b>OE-2:</b> Reestructurar el PMIR bajo D.L. 1278, D.S. 014-2017-MINAM y NTP 900.058:2019, incorporando un subprograma especializado RAEE con EO-RS autorizadas.</li>
                <li><b>OE-3:</b> Prevenir la contaminación de suelos, bofedales y la subcuenca del río Yauli por hidrocarburos y químicos (meta: <b>0 incidentes ambientales significativos</b>).</li>
                <li><b>OE-4:</b> Institucionalizar <b>8 KPIs ambientales cuantitativos</b> con cierre perentorio de condiciones subestándar (&lt;24 h, &lt;72 h o 2 semanas).</li>
                <li><b>OE-5:</b> Articular el Plan de Contingencias con el Sistema de Comando de Incidentes de Volcan mediante simulacros semestrales.</li>
                <li><b>OE-6:</b> Consolidar el presupuesto anual analítico de <b>$10,800.00 USD</b> y cronograma maestro de 12 meses.</li>
            </ul>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>1.7 – 1.8 Alcance, Delimitación Territorial y Exclusiones</h3>
            <p><b>Alcance y Dotación:</b> Obligatorio para los <b>14 colaboradores destacados</b> de COMM (1 Residente, 1 Ingeniero Supervisor SCCA, 2 Supervisores de Operaciones y 10 Técnicos Especialistas/conductores) en oficinas técnicas, laboratorio de fibra, almacén, estacionamiento en superficie y labores subterráneas.</p>
            <p><b>Exclusiones Operacionales:</b> Quedan excluidos los procesos productivos propios del titular minero Volcan: perforación/voladura masiva, desatado y sostenimiento pesado, acarreo con scooptrams/dumpers, planta concentradora, gestión de relaves, plantas de tratamiento de agua ácida/PTARD y mantenimiento mecánico mayor de maquinaria pesada.</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>1.9 – 1.10 Marco Legal e Institucional</h3>
            <p>Constitución Política (Art. 2 inc. 22), Ley N.° 28611 (Ley General del Ambiente), Ley N.° 28245 (SNGA), Ley N.° 29783 (SST), D.L. 1278 / D.S. 014-2017-MINAM (Residuos y SIGERSOL), D.S. 009-2019-MINAM (RAEE), D.S. 024-2016-EM (Minería), Ley N.° 29338 (Recursos Hídricos), NTP 900.058:2019 (Código de Colores) y ECAs de Aire (D.S. 003-2017), Agua Cat. 3 y 4 (D.S. 004-2017), Suelo (D.S. 011-2017) y Ruido (D.S. 085-2003-PCM). Fiscalizado por Superintendencia de Medio Ambiente de Volcan, OEFA y OSINERGMIN.</p>
        </div>
        """

    def obtener_contenido_cap2(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>2.1 – 2.3 Descripción Técnica del Proyecto, Flota e Insumos Químicos</h3>
            <ul>
                <li><b>Componente Operativo de Campo:</b> Tendido de fibra óptica monomodo dieléctrica (12, 24 y 48 hilos, norma ITU-T G.652.D con Kevlar y chaqueta LSZH), cable blindado Cat 6A, bandejas portacables galvanizadas, gabinetes herméticos NEMA 4X / IP66, switches industriales (-40 °C a +75 °C), sistemas UPS (baterías VRLA o ion-litio), empalmes por fusión con arco voltaico y pruebas OTDR (&le; 0.1 dB).</li>
                <li><b>Componente de Gabinete Técnico y Almacén:</b> Preconfiguración lógica (VLAN, RSTP/MRP), planos As-Built en AutoCAD y custodia metrológica de materiales.</li>
                <li><b>Flota Vehicular y Equipos:</b> 2 camionetas pick-up 4&times;4 turbodiésel intercooler con sistema SCR (AdBlue), jaula antivuelco y pértiga de 4 m; rotomartillos electroportátiles a batería y fusionadora óptica.</li>
                <li><b>Insumos Químicos Inventariados:</b> Combustible Diésel B5-S50, aceites SAE 15W-40 / 5W-30 / 80W-90, solución AdBlue (AUS 32, urea 32.5%), refrigerante etilenglicol, líquido de frenos DOT 4, alcohol isopropílico al 99.8% (CAS 67-63-0), limpiador dieléctrico, lubricante polimérico biodegradable y pintura galvanizada en frío.</li>
            </ul>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>2.5 Política Integrada de Gestión (RD-PL-01 Versión 08 - 15/10/2025)</h3>
            <p>Suscrita por Filiberto Jesús Revilla Delgado (CEO Director) y Sergio David Gonzales Mendívil (Gerente General). Sus 6 compromisos son: (1) Calidad de servicio y satisfacción del cliente, (2) Eliminación de peligros y reducción de riesgos ocupacionales, (3) <b>Protección del ambiente y prevención de la contaminación</b>, (4) Cumplimiento normativo legal, (5) Capacitación, sensibilización y participación, y (6) Mejora continua del SIG.</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>2.6 Caracterización del Medio Afectado (Línea Base)</h3>
            <ul>
                <li><b>Medio Físico:</b> Valles fluvioglaciares y morrenas (pendientes 15%–60%, Grupo Pucará y secuencias volcánicas); clima Frío de Puna con oscilación térmica &gt;20 °C (heladas de -5 °C a -15 °C); temporada húmeda dic–mar (650–900 mm) y estiaje may–sep. Subcuenca alta del río Yauli (cuenca del Mantaro) y suelos Entisoles/Inceptisoles (Tierras de Protección X y Pastoreo Limitado P).</li>
                <li><b>Medio Biológico:</b> Pajonales de puna (<i>Stipa ichu</i>, <i>Festuca dolichophylla</i>), plantas en almohadilla (<i>Pycnophyllum molle</i>) y <b>Bofedales altoandinos</b> (<i>Distichia muscoides</i>, <i>Plantago rigida</i>). Fauna sensible: vizcacha (<i>Lagidium viscacia</i>), zorro andino (<i>Lycalopex culpaeus</i>), huallata (<i>Chloephaga melanoptera</i>), pato sutro y perdiz serrana.</li>
                <li><b>Medio Socioeconómico:</b> Enclave minero con turnos atípicos (14&times;7 / 21&times;10) y articulación indirecta con las Comunidades Campesinas de Yauli, Huancachupa y Pachachaca (ganadería de camélidos y ovinos).</li>
            </ul>
        </div>
        """

    def obtener_contenido_cap3(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>3.1 Metodología de Evaluación Semicuantitativa (S &times; P)</h3>
            <p>En coherencia con la cláusula 6.1.2 de ISO 14001:2015, la importancia ambiental se calcula mediante: <b>Significancia = Severidad (S) &times; Probabilidad (P)</b> (escala 1 a 5 en cada eje, producto de 1 a 25):</p>
            <table border='1' cellpadding='5' cellspacing='0' style='border-collapse:collapse; width:100%; border-color:{GRIS_BORDE};'>
                <tr style='background-color:{VERDE_SUAVE}; font-weight:bold; color:{VERDE_OSCURO};'>
                    <td>Rango (S &times; P)</td><td>Nivel de Significancia</td><td>Aspectos Comprendidos</td><td>Acción de Gestión Requerida</td>
                </tr>
                <tr><td><b>1 – 4</b></td><td><b>BAJO</b></td><td>Consumo de papel bond y cartón limpio en oficina.</td><td>Control operacional rutinario y digitalización.</td></tr>
                <tr><td><b>5 – 9</b></td><td><b>MODERADO</b></td><td>Residuos orgánicos, consumo de agua, energía y metales/plásticos.</td><td>Reforzar controles existentes y capacitación.</td></tr>
                <tr><td><b>10 – 16</b></td><td><b>ALTO</b></td><td>Emisiones vehiculares, derrames de hidrocarburos, RESPEL, RAEE, ruido, incendios y no aprovechables.</td><td>Mitigación específica de ingeniería, presupuesto y KPIs.</td></tr>
                <tr><td><b>17 – 25</b></td><td><b>CRÍTICO</b></td><td>Escenarios catastróficos no controlados.</td><td>Acción inmediata, paralización y rediseño del proceso.</td></tr>
            </table>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>3.2 – 3.16 Los 12 Aspectos e Impactos Ambientales Evaluados</h3>
            <ol>
                <li><b>Consumo de papel y generación de residuos de embalaje (cartón):</b> Reportes técnicos y desembalaje de equipos &rarr; Huella indirecta y saturación de acopios.</li>
                <li><b>Emisión de gases de combustión de vehículos livianos:</b> Motores turbodiésel en hipoxia barométrica (4,000–4,700 m.s.n.m.) &rarr; Deterioro del aire en socavón (CO, NOx, PM<sub>2.5</sub>) y gases GEI.</li>
                <li><b>Generación de Residuos de Aparatos Eléctricos y Electrónicos (RAEE):</b> Descarte de switches, routers, módulos SFP, UPS y cableado &rarr; Contaminación por metales pesados y pérdida de valorización.</li>
                <li><b>Generación de residuos sólidos peligrosos (RESPEL):</b> Trapos con aceite/grasa, guantes contaminados, envases de limpiadores dieléctricos y aerosoles &rarr; Contaminación de suelos y drenajes.</li>
                <li><b>Consumo de productos químicos auxiliares y riesgo de liberación:</b> Uso de alcohol isopropílico (99.8%), solventes y pintura galvanizada &rarr; Riesgo de inflamabilidad y contaminación puntual.</li>
                <li><b>Potencial derrame de lubricantes, combustibles e hidrocarburos:</b> Fugas mecánicas de camionetas 4&times;4 en rampas o taller &rarr; Alteración de suelos Entisoles/Inceptisoles y afectación de bofedales y río Yauli.</li>
                <li><b>Generación de residuos sólidos industriales (aprovechables):</b> Recortes de fibra óptica, cables de cobre, bandejas galvanizadas y canaletas PVC &rarr; Ocupación de espacio / ahorro por reciclaje (+).</li>
                <li><b>Generación de ruido ambiental y vibraciones mecánicas:</b> Rotomartillos y tránsito vehicular &rarr; Ahuyentamiento de fauna (vizcachas, aves) y exposición sonora.</li>
                <li><b>Consumo de energía eléctrica:</b> Servidores, fusionadoras ópticas, equipos OTDR y recarga de baterías &rarr; Demanda energética y huella de carbono.</li>
                <li><b>Consumo de agua para uso industrial y doméstico:</b> Limpieza de áreas y herramientas &rarr; Reducción de disponibilidad hídrica en cabecera de cuenca.</li>
                <li><b>Almacenamiento y descarte de baterías de respaldo (VRLA / Ion-Litio):</b> Sistemas UPS y equipos portátiles &rarr; Riesgo de fuga electrolítica o evento térmico.</li>
                <li><b>Escenarios de emergencia ambiental (incendios / derrames súbitos):</b> Cortocircuitos en gabinetes o sustancias inflamables &rarr; Humos tóxicos y residuos de extinción.</li>
            </ol>
        </div>
        """

    def obtener_contenido_cap4_5_6(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>4.1 Programa de Prevención y Mitigación Ambiental</h3>
            <ul>
                <li><b>Control de Emisiones y Ruido:</b> Mantenimiento preventivo vehicular, uso obligatorio de solución <b>AdBlue (AUS 32)</b> en catalizadores SCR, prohibición de ralentí innecesario y mantenimiento de rotomartillos.</li>
                <li><b>Conservación de Suelos y Cuerpos de Agua:</b> Inspección vehicular preuso diaria, bandejas de contención secundaria en talleres/almacenes y kits antiderrame portátiles en las 2 camionetas 4&times;4.</li>
            </ul>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>4.2 Programa de Manejo Integral de Residuos (PMIR) y Subprograma RAEE</h3>
            <p>Segregación obligatoria en origen bajo la <b>NTP 900.058:2019</b> (Amarillo: metales, Verde: vidrio, Azul: papel/cartón, Blanco: plásticos, Marrón: orgánicos, Negro: no aprovechables, Rojo: residuos peligrosos) y declaración anual en <b>SIGERSOL No Municipal</b>.</p>
            <p><b>Subprograma Especial de RAEE (D.S. 009-2019-MINAM):</b> (1) Identificación y desconexión sin desarme destructivo, (2) Rotulación e inventario técnico (serie, marca, peso), (3) Almacenamiento temporal protegido de humedad e impactos separando baterías plomo-ácido e ion-litio, y (4) Entrega formal con manifiestos a una <b>EO-RS autorizada por el MINAM</b>.</p>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>5 y 6. Indicadores de Desempeño (8 KPIs) y Auditorías Ambientales</h3>
            <ul>
                <li><b>IFIAS (Índice de Frecuencia de Incidentes Ambientales Significativos):</b> Meta = <b>0.00</b> (IAS / HHT &times; 10<sup>6</sup>).</li>
                <li><b>Segregación y Entrega RAEE a EO-RS:</b> Meta = <b>100%</b>.</li>
                <li><b>Operatividad de Kits Antiderrame (Estaciones móviles y fijas):</b> Meta = <b>100%</b> (cumplimiento observado 92% en PRAM).</li>
                <li><b>Cumplimiento de Inspecciones Ambientales (Internas y Cruzadas):</b> Meta &ge; <b>90% – 100%</b> (24 inspecciones anuales).</li>
                <li><b>Cobertura de Capacitación y Campañas Ambientales:</b> Meta &ge; <b>85% – 90%</b> (12 capacitaciones + 12 campañas ambientales).</li>
                <li><b>Auditorías Ambientales:</b> Ejecución semestral e interna bajo ISO 14001:2015, con cierre de hallazgos en &lt;24 h (críticos), &lt;72 h (altos) y 2 semanas (moderados).</li>
            </ul>
        </div>
        """

    def obtener_contenido_cap7_8(self):
        return f"""
        <div style='font-family: Segoe UI, sans-serif;'>
            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>7.1 – 7.2 Cronograma Maestro (12 Meses) y Presupuesto Ambiental ($10,800.00 USD)</h3>
            <p>La Alta Dirección de COMM garantiza la viabilidad técnico-económica del Plan mediante una inversión anual consolidada de <b>$10,800.00 USD</b> distribuida en 12 meses continuos:</p>
            <ul>
                <li><b>Implementación de Kits Antiderrame, bandejas de contención y absorbentes:</b> $1,800.00 USD.</li>
                <li><b>Estaciones de segregación y contenedores cromáticos NTP 900.058:2019:</b> $1,500.00 USD.</li>
                <li><b>Acondicionamiento, embalaje y transporte de RAEE y RESPEL con EO-RS:</b> $2,500.00 USD.</li>
                <li><b>Monitoreos instrumentales acreditados por INACAL (fuentes móviles y ruido):</b> $1,800.00 USD.</li>
                <li><b>Programa de capacitación, campañas ambientales y simulacros semestrales:</b> $1,200.00 USD.</li>
                <li><b>Auditorías internas ISO 14001:2015 y programa de cierre/restitución ambiental:</b> $2,000.00 USD.</li>
            </ul>
            <hr style='border: 1px solid {GRIS_BORDE};'>

            <h3 style='color: {VERDE_OSCURO}; margin-bottom: 4px;'>7.3 – 8. Formatos de Control y Anexos del Plan</h3>
            <ul>
                <li><b>Anexo 1:</b> Matriz Consolidada de Identificación y Valoración de Aspectos e Impactos Ambientales (12 aspectos evaluados).</li>
                <li><b>Anexo 2:</b> Inventario de Sustancias Químicas y Hojas de Datos de Seguridad (SDS/MSDS) de Diésel B5-S50, AdBlue, Alcohol Isopropílico 99.8% y Dieléctricos.</li>
                <li><b>Anexo 3:</b> Procedimiento Operativo Específico para la Gestión Integral de RAEE (D.S. 009-2019-MINAM).</li>
                <li><b>Anexo 4:</b> Check-List de Inspección Preoperacional Vehicular y Kits Antiderrame en Interior Mina y Superficie.</li>
                <li><b>Anexo 5:</b> Formato de Reporte e Investigación de Incidentes Ambientales, Registro de Residuos y Trazabilidad SIGERSOL.</li>
            </ul>
        </div>
        """


# ==========================================================
# 12. EJECUCIÓN DEL APLICATIVO
# ==========================================================

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    ventana = VentanaPlanAmbiental()
    ventana.show()
    sys.exit(app.exec())
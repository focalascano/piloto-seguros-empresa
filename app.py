import streamlit as st
from fpdf import FPDF
import datetime
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Determinador de Seguros", layout="centered")

# --- ESTILOS CSS ---
st.markdown("""
    <style>
    .stApp { background-color: #f0f2f6; }
    .main-header {
        background-color: #002366;
        padding: 2.5rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 { color: white !important; margin-bottom: 0.5rem; }
    div.stDownloadButton:nth-of-type(1) button { background-color: #002366 !important; color: white !important; }
    div.stDownloadButton:nth-of-type(2) button { background-color: #f0f2f6 !important; color: black !important; border: 1px solid #cccccc; }
    </style>
    """, unsafe_allow_html=True)

# --- CLASE PDF ---
class PDF(FPDF):
    def __init__(self):
        super().__init__(orientation='P', unit='mm', format='A4')
        self.set_margins(15, 15, 15)
        self.set_auto_page_break(auto=True, margin=15)

    def header(self):
        if os.path.exists("logotrenes.png"):
            try: self.image("logotrenes.png", 10, 8, 33)
            except: pass
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title, size=12):
        self.set_font('Helvetica', 'B', size)
        txt_safe = title.upper().encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 10, txt=txt_safe)
        self.ln(2)

    def chapter_body(self, body, size=10, style=''):
        self.set_font('Helvetica', style, size)
        txt_safe = str(body).encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, txt=txt_safe, align='J')
        self.ln(2)

# --- INTERFAZ ---
st.markdown("""
    <div class="main-header">
        <h1>MODELO DE DETERMINACIÓN DE SEGUROS A PROVEEDORES</h1>
        <p>Piloto institucional – Uso interno | Versión 1.0</p>
    </div>
    """, unsafe_allow_html=True)

opciones = ["No", "Sí"]
r1 = st.radio("Pregunta 1: ¿Para realizar la actividad personal del proveedor ingresará a predios o instalaciones de SOFSA?", opciones)
r2 = st.radio("Pregunta 2: ¿La actividad consiste exclusivamente en tareas administrativas...?", opciones)
r3 = st.radio("Pregunta 3: ¿La actividad requiere el ingreso de vehículos...?", opciones)
r4 = st.radio("Pregunta 4: ¿El proveedor tendrá bajo su guarda bienes de SOFSA...?", opciones)
r5 = st.radio("Pregunta 5: ¿El trabajo se realizará en andenes, vías...?", opciones)
r6 = st.radio("Pregunta 6: ¿La actividad corresponde a un trabajo menor...?", opciones)
r7 = st.radio("Pregunta 7: ¿La actividad requiere uso de equipos complejos...?", opciones)
r8 = st.radio("Pregunta 8: ¿La actividad incluye tareas críticas (altura, soldadura, etc)?", opciones)
r9 = st.radio("Pregunta 9: ¿La actividad implica obra o montaje (>USD 30.000)?", opciones)

p1, p3, p4, p5, p7, p8, p9 = [r == "Sí" for r in [r1, r3, r4, r5, r7, r8, r9]]

# Lógica de Seguros Requeridos
seguros_activos = []
if p1: seguros_activos.append("Seguro de Personas (ART / VO / AP)")
if (p5 or p7 or p8 or p9) and not p9: seguros_activos.append("Responsabilidad Civil Comprensiva")
if p9: seguros_activos.append("Todo Riesgo Construcción y Montaje")
if p4: seguros_activos.append("Caución por Tenencia de Bienes")
if p3: seguros_activos.append("Responsabilidad Civil Automotor")

# Lógica de Riesgo
if p9 or p8 or p5: nivel = "Alto"
elif p1 and (p7 or p4): nivel = "Medio"
elif p1: nivel = "Bajo"
else: nivel = "Nulo"

if nivel != "Nulo":
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn2:
        if len(seguros_activos) > 0:
            chk = PDF()
            chk.add_page()
            
            # 1. Encabezado [cite: 5, 6, 7]
            chk.chapter_title("CHECKLIST DE CONTROL DE PÓLIZAS", 14)
            chk.chapter_body("Seguros requeridos según Anexo generado por el Modelo de Determinación de Seguros a Proveedores", 11, 'B')
            
            # 2. Resultado del modelo [cite: 8, 9, 10]
            chk.ln(4)
            chk.chapter_body("Resultado del modelo", 10, 'B')
            chk.chapter_body(f"Nivel de riesgo determinado: {nivel}")
            chk.chapter_body(f"Seguros requeridos: {', '.join(seguros_activos)}")
            
            # 3. Regla operativa [cite: 11, 12]
            chk.ln(4)
            chk.chapter_body("Regla operativa", 10, 'B')
            chk.chapter_body("Ante duda razonable sobre la aplicabilidad del seguro, SOFSA determinará su exigencia en función del riesgo identificado.")
            
            # 4. Control documental general [cite: 13, 14, 86]
            chk.ln(4)
            chk.chapter_body("Control documental general (aplica a todos los seguros)", 10, 'B')
            chk.chapter_body("[] Aseguradora habilitada SSN  [] Calificación de la aseguradora  [] Vigencia durante toda la actividad  [] Actividad asegurada compatible  [] Certificado de cobertura vigente  [] Libre deuda (si aplica)")
            
            # 5. Bloques específicos [cite: 21]
            
            # Seguro de Personas [cite: 22, 87]
            if p1:
                chk.ln(4)
                chk.chapter_body("1. Seguro de Personas", 10, 'B')
                chk.chapter_body("ART: [] Nómina de personal afectado [] Cláusula de no repetición a favor de SOFSA")
                chk.chapter_body("Seguro Colectivo de Vida Obligatorio: [] Nómina de personal afectado")
                chk.chapter_body("Seguro de Accidentes Personales: [] Nómina de personal afectado [] Cláusula de no repetición a favor de SOFSA [] Cláusula SOFSA beneficiaria en primer término [] Cláusula de notificación previa")

            # Responsabilidad Civil Comprensiva (Solo si no hay TRCyM) [cite: 33, 59]
            if (p5 or p7 or p8 or p9) and not p9:
                chk.ln(4)
                chk.chapter_body("2. Responsabilidad Civil Comprensiva", 10, 'B')
                chk.chapter_body("[] Suma asegurada correcta [] Cláusula de no repetición [] Asegurados adicionales [] Cláusula RC cruzada [] Cláusula de notificación previa")
                chk.chapter_body("Adicionales según actividad: [] Trabajos en altura [] Soldadura / oxicorte [] Izaje de carga [] Intervención eléctrica [] Maquinaria pesada [] Uso de armas [] Suministro de alimentos")

            # Todo Riesgo Construcción y Montaje [cite: 47, 95]
            if p9:
                chk.ln(4)
                chk.chapter_body("3. Todo Riesgo Construcción y Montaje", 10, 'B')
                chk.chapter_body("[] Suma asegurada correcta [] Vigencia total de obra [] Incluye daños materiales [] Cláusula de no repetición [] Asegurados adicionales [] Cláusula RC cruzada [] Cláusula de notificación previa")
                # RC dentro de TRCyM [cite: 55, 96, 97]
                chk.chapter_body("Cobertura de Responsabilidad Civil dentro de Todo Riesgo Construcción", 10, 'B')
                chk.chapter_body("[] Responsabilidad Civil incluida dentro de la póliza TRCyM [] Suma asegurada de RC acorde al nivel de riesgo [] Incluye adicionales según actividad (si corresponden)")

            # Caución [cite: 60, 98]
            if p4:
                chk.ln(4)
                chk.chapter_body("4. Caución por Tenencia de Bienes", 10, 'B')
                chk.chapter_body("[] Monto acorde al valor indicado en el pliego [] Vigencia total del contrato")

            # Automotor [cite: 63, 99]
            if p3:
                chk.ln(4)
                chk.chapter_body("5. Responsabilidad Civil Automotor", 10, 'B')
                chk.chapter_body("[] Vehículos declarados [] Cláusula de notificación previa [] Cláusula de no repetición")

            st.download_button(
                label="Generar Checklist de control",
                data=bytes(chk.output()),
                file_name=f"Checklist_Control_{nivel}.pdf",
                mime="application/pdf"
            )

    # Cartel de nivel final
    if nivel == "Alto": st.error(f"**NIVEL DE RIESGO: {nivel}**")
    elif nivel == "Medio": st.warning(f"**NIVEL DE RIESGO: {nivel}**")
    elif nivel == "Bajo": st.info(f"**NIVEL DE RIESGO: {nivel}**")

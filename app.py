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

# --- TEXTOS LEGALES (Mantenidos del original) ---
TEXTOS_LEGALES = {
    "GENERAL_ENCABEZADO": "La Contratista deberá acreditar ante La SOFSA...", # (Truncado por brevedad, usar el original)
    "RC": "Seguro de Responsabilidad Civil Comprensiva...", 
    "ART": "Seguro de Riesgos del Trabajo...",
    "VO": "Seguro Colectivo de Vida Obligatorio...",
    "AP": "Seguro de Accidentes Personales...",
    "CAUCION": "Caución de Tenencia de Bienes...",
    "TRCYM": "Seguros Todo riesgo Construcción y/o Montaje...",
    "AUTO": "Seguro Automotor Obligatorio...",
    "REQUISITOS_FINALES": "Otros Seguros..."
}

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

# Lógica de Riesgo
if p9 or p8 or p5: nivel = "Alto"
elif p1 and (p7 or p4): nivel = "Medio"
elif p1: nivel = "Bajo"
else: nivel = "Nulo"

if nivel != "Nulo":
    st.write("---")
    col_btn1, col_btn2 = st.columns(2)

    # --- BOTÓN 1: ANEXO DE SEGUROS ---
    with col_btn1:
        pdf_anexo = PDF()
        pdf_anexo.add_page()
        pdf_anexo.chapter_title("ANEXO DE SEGUROS")
        pdf_anexo.chapter_body(TEXTOS_LEGALES["GENERAL_ENCABEZADO"])
        if p1:
            pdf_anexo.chapter_body(TEXTOS_LEGALES["ART"])
            pdf_anexo.chapter_body(TEXTOS_LEGALES["VO"])
            pdf_anexo.chapter_body(TEXTOS_LEGALES["AP"])
        if (p5 or p7 or p8 or p9) and not p9:
            suma_rc = "USD 100.000" if nivel == "Alto" else "USD 50.000"
            pdf_anexo.chapter_body(TEXTOS_LEGALES["RC"] + f"\n\nSUMA ASEGURADA MINIMA REQUERIDA: {suma_rc}")
        if p4: pdf_anexo.chapter_body(TEXTOS_LEGALES["CAUCION"])
        if p9: pdf_anexo.chapter_body(TEXTOS_LEGALES["TRCYM"])
        if p3: pdf_anexo.chapter_body(TEXTOS_LEGALES["AUTO"])
        
        pdf_anexo.add_page()
        pdf_anexo.chapter_title("REQUISITOS GENERALES")
        pdf_anexo.chapter_body(TEXTOS_LEGALES["REQUISITOS_FINALES"])
        
        st.download_button(
            label="Generar Anexo de Seguros",
            data=bytes(pdf_anexo.output()),
            file_name=f"Anexo_Seguros_{nivel}.pdf",
            mime="application/pdf"
        )

    # --- BOTÓN 2: CHECKLIST DE CONTROL ---
    with col_btn2:
        seguros_activos = []
        if p1: seguros_activos.append("Seguro de Personas (ART / VO / AP)")
        if (p5 or p7 or p8 or p9) and not p9: seguros_activos.append("Responsabilidad Civil Comprensiva")
        if p9: seguros_activos.append("Todo Riesgo Construcción y Montaje")
        if p4: seguros_activos.append("Caución por Tenencia de Bienes")
        if p3: seguros_activos.append("Responsabilidad Civil Automotor")

        chk = PDF()
        chk.add_page()
        chk.chapter_title("CHECKLIST DE CONTROL DE PÓLIZAS", 14)
        chk.chapter_body("Seguros requeridos según Anexo generado por el Modelo de Determinación de Seguros a Proveedores", 11, 'B')
        
        chk.ln(4)
        chk.chapter_body("Resultado del modelo", 10, 'B')
        chk.chapter_body(f"Nivel de riesgo determinado: {nivel}")
        chk.chapter_body(f"Seguros requeridos: {', '.join(seguros_activos)}")
        
        chk.ln(4)
        chk.chapter_body("Regla operativa", 10, 'B')
        chk.chapter_body("Ante duda razonable sobre la aplicabilidad del seguro, SOFSA determinará su exigencia en función del riesgo identificado.")
        
        chk.ln(4)
        chk.chapter_body("Control documental general (aplica a todos los seguros)", 10, 'B')
        chk.chapter_body("[] Aseguradora habilitada SSN  [] Calificación de la aseguradora  [] Vigencia durante toda la actividad  [] Actividad asegurada compatible  [] Certificado de cobertura vigente  [] Libre deuda (si aplica)")

        if p1:
            chk.ln(4)
            chk.chapter_body("1. Seguro de Personas", 10, 'B')
            chk.chapter_body("ART: [] Nómina de personal afectado [] Cláusula de no repetición a favor de SOFSA")
            chk.chapter_body("Seguro Colectivo de Vida Obligatorio: [] Nómina de personal afectado")
            chk.chapter_body("Seguro de Accidentes Personales: [] Nómina de personal afectado [] Cláusula de no repetición a favor de SOFSA [] Cláusula SOFSA beneficiaria en primer término [] Cláusula de notificación previa")

        if (p5 or p7 or p8 or p9) and not p9:
            chk.ln(4)
            chk.chapter_body("2. Responsabilidad Civil Comprensiva", 10, 'B')
            chk.chapter_body("[] Suma asegurada correcta [] Cláusula de no repetición [] Asegurados adicionales [] Cláusula RC cruzada [] Cláusula de notificación previa")
            chk.chapter_body("Adicionales según actividad: [] Trabajos en altura [] Soldadura / oxicorte [] Izaje de carga [] Intervención eléctrica [] Maquinaria pesada [] Uso de armas [] Suministro de alimentos")

        if p9:
            chk.ln(4)
            chk.chapter_body("3. Todo Riesgo Construcción y Montaje", 10, 'B')
            chk.chapter_body("[] Suma asegurada correcta [] Vigencia total de obra [] Incluye daños materiales [] Cláusula de no repetición [] Asegurados adicionales [] Cláusula RC cruzada [] Cláusula de notificación previa")
            chk.chapter_body("Cobertura de Responsabilidad Civil dentro de Todo Riesgo Construcción", 10, 'B')
            chk.chapter_body("[] Responsabilidad Civil incluida dentro de la póliza TRCyM [] Suma asegurada de RC acorde al nivel de riesgo [] Incluye adicionales según actividad (si corresponden)")

        if p4:
            chk.ln(4)
            chk.chapter_body("4. Caución por Tenencia de Bienes", 10, 'B')
            chk.chapter_body("[] Monto acorde al valor indicado en el pliego [] Vigencia total del contrato")

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

    # Cartel final de nivel
    if nivel == "Alto": st.error(f"**NIVEL DE RIESGO: {nivel}**")
    elif nivel == "Medio": st.warning(f"**NIVEL DE RIESGO: {nivel}**")
    elif nivel == "Bajo": st.info(f"**NIVEL DE RIESGO: {nivel}**")

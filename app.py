import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SDS - Cuestionario de Riesgo", page_icon="🛡️")

st.title("🛡️ Determinación de Seguros a Proveedores")
st.markdown("---")

# --- 1. CUESTIONARIO (Sección 12.2) ---
st.subheader("Cuestionario de Caracterización de la Actividad")
col1, col2 = st.columns(2)

with col1:
    p1 = st.checkbox("P1: Presencia de personal en instalaciones", value=False)
    p2 = st.checkbox("P2: Actividad administrativa/profesional pura", value=False)
    p3 = st.checkbox("P3: Ingreso de vehículos a instalaciones", value=False)
    p4 = st.checkbox("P4: Traslado o custodia de bienes de La Empresa", value=False)
    p5 = st.checkbox("P5: Trabajo en zona ferroviaria u operativa", value=False)

with col2:
    p6 = st.checkbox("P6: Trabajo menor (herramientas manuales, <1 mes)", value=False)
    p7 = st.checkbox("P7: Uso de equipos o maquinaria", value=False)
    p8 = st.checkbox("P8: Tareas riesgosas (Altura, fuego, izaje, etc.)", value=False)
    p9 = st.checkbox("P9: Obra, instalación o montaje", value=False)

# --- 2. MOTOR DE VALIDACIÓN (Sección 15.3) ---
errores = []
if not p1 and (p3 or p4 or p5 or p6 or p7 or p8 or p9):
    errores.append("⚠️ Bloqueo: Toda condición operativa implica presencia de personal (P1 debe ser SÍ).")
if p2 and (p4 or p5 or p6 or p7 or p8 or p9):
    errores.append("⚠️ Bloqueo: Actividad administrativa (P2) no es compatible con tareas operativas/riesgosas.")
if p6 and (p4 or p5 or p7 or p8 or p9):
    errores.append("⚠️ Bloqueo: El trabajo menor (P6) es incompatible con riesgos altos o maquinaria compleja.")

# --- 3. PROCESAMIENTO ---
if st.button("Calcular Riesgo y Seguros"):
    if errores:
        for err in errores:
            st.error(err)
    else:
        # Jerarquía de Riesgo (Sección 13.1)
        # Se evalúa en orden: Alto -> Medio -> Bajo -> Nulo
        nivel = "Nulo"
        if p9 or p8 or p5 or p4:
            nivel = "Alto"
        elif p1 and p7:
            nivel = "Medio"
        elif p1:
            nivel = "Bajo"
        
        # Mapeo de Seguros (Sección 16)
        seguros = []
        if p1:
            seguros.append("Seguro de Personas (ART y Vida Obligatorio o AP)")
        if p1 and (p5 or p7 or p8 or p9):
            suma = "USD 100.000" if nivel == "Alto" else "USD 50.000"
            seguros.append(f"Responsabilidad Civil General (Suma Asegurada: {suma})")
        if p8:
            seguros.append("Adicionales de RC (Altura, Soldadura, Izaje, etc. según corresponda)")
        if p4:
            seguros.append("Caución de Tenencia de Bienes")
        if p9:
            seguros.append("Todo Riesgo Construcción y Montaje (TRCyM)")
        if p3:
            seguros.append("Responsabilidad Civil Automotor")

        # --- MOSTRAR RESULTADOS ---
        st.markdown("---")
        color = "red" if nivel == "Alto" else "orange" if nivel == "Medio" else "green"
        st.markdown(f"### NIVEL DE RIESGO: :{color}[{nivel.upper()}]")
        
        st.write("**Seguros Requeridos:**")
        for s in seguros:
            st.write(f"- {s}")

        # Generación de Word para descarga
        doc = Document()
        doc.add_heading('ANEXO DE SEGUROS', 0)
        doc.add_paragraph(f"Nivel de Riesgo: {nivel}")
        doc.add_paragraph(f"Fecha: {datetime.now().strftime('%d/%m/%Y')}")
        for s in seguros:
            doc.add_paragraph(s, style='List Bullet')
        
        bio = BytesIO()
        doc.save(bio)
        
        st.download_button(
            label="📄 Descargar Anexo en Word",
            data=bio.getvalue(),
            file_name=f"Anexo_Seguros_{nivel}.docx",
            mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
        )

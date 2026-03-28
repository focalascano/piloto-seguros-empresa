import streamlit as st
from docx import Document
from io import BytesIO
from datetime import datetime

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="SDS - Cuestionario de Riesgo", page_icon="🛡️")

st.title("🛡️ Determinación de Seguros a Proveedores")
st.markdown("---")

# --- 1. CUESTIONARIO (Sección 12.2) ---
st.subheader("Cuestionario de Caracterización de riesgo: Marque las casillas que correspondan en caso de que la respuesta a la pregunta sea afirmativa")
col1, col2 = st.columns(2)

with col1:
    p1 = st.checkbox("¿Para realizar la actividad personal del proveedor ingresará a predios o instalaciones de la empresa?", value=False)
    p2 = st.checkbox("¿La actividad consiste exclusivamente en tareas administrativas o profesionales de oficina, sin intervención técnica ni operativa? Ejemplos: consultoría, auditoría, capacitaciones teóricas, asesoramiento profesional", value=False)
    p3 = st.checkbox("¿La actividad requiere uso o ingreso de vehículos del proveedor a predios o instalaciones de la empresa?", value=False)
    p4 = st.checkbox("¿El proveedor transportará o tendrá en sus instalaciones mercadería, bienes o equipos de la empresa?", value=False)
    p5 = st.checkbox("¿El trabajo se realizará en estaciones, andenes, vías, talleres ferroviarios o sectores con circulación de trenes o pasajeros?", value=False)

with col2:
    p6 = st.checkbox("¿La actividad corresponde a un trabajo menor de mantenimiento simple en la empresa?  Debe cumplir todas estas condiciones: duración corta (menor a 1 mes de trabajo) - uso herramientas manuales simples - sin trabajo en altura, ni andamios
 - sin maquinaria - sin intervención en infraestructura - sin afectar circulación ferroviaria o de pasajeros Ejemplos: (pintura interior de oficina, reparación menor de mobiliario, cerrajería, etc)", value=False)
    p7 = st.checkbox("¿La actividad requiere uso de equipos, maquinaria o de herramientas complejas en la empresa? Ejemplos: herramientas de corte y/o herramienta de calor y/o herramienta a explosión, equipos técnicos, maquinarias", value=False)
    p8 = st.checkbox("¿La actividad incluye alguna de las siguientes tareas? trabajos en altura - soldadura u oxicorte - izaje de cargas - intervención eléctrica - uso de maquinaria pesada - uso de armas de fuego - suministro de alimentos", value=False)
    p9 = st.checkbox("¿La actividad implica construir, instalar o montar una obra, sistema o equipos nuevo? Incluye: obras civiles, refacciones estructurales, instalación de equipos (montaje o desmontaje), montaje de sistema electrico o mecánico - No incluye:
mantenimiento simple, refacciones menores, tareas de servicio", value=False)

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

import streamlit as st
import pandas as pd
from docx import Document
from io import BytesIO

# Carga de base de cláusulas (asumiendo que subiste el CSV)
@st.cache_data
def cargar_clausulas():
    try:
        return pd.read_csv("clausulas.csv")
    except:
        return pd.DataFrame(columns=["Seguro", "Texto"])

df_clausulas = cargar_clausulas()

def generar_word(datos_seguros, nivel):
    doc = Document()
    doc.add_heading('Anexo de Seguros - Determinación Automática', 0)
    doc.add_paragraph(f"Nivel de Riesgo Determinado: {nivel}")
    doc.add_heading('Cláusulas Exigibles:', level=1)
    
    for s in datos_seguros:
        doc.add_paragraph(s, style='List Bullet')
    
    bio = BytesIO()
    doc.save(bio)
    return bio.getvalue()

# --- INTERFAZ STREAMLIT ---
st.title("🛡️ SDS: Prueba Piloto")
# ... (Aquí va el código del cuestionario P1 a P9 que ya tienes) ...

if st.button("Procesar y Generar Documento"):
    # (Lógica de validación e identificación de seguros que ya tienes [cite: 13])
    # Suponiendo que 'seguros_finales' es la lista de textos detectados:
    
    nivel_detectado = "Alto" # Resultado del motor lógico
    lista_seguros = ["ART Cláusula 1", "RC Suma USD 100k"] # Ejemplo
    
    st.success(f"Análisis Completado: Riesgo {nivel_detectado}")
    
    # Botón de descarga
    docx_file = generar_word(lista_seguros, nivel_detectado)
    st.download_button(
        label="📄 Descargar Anexo de Seguros (Word)",
        data=docx_file,
        file_name="Anexo_Seguros_Proveedor.docx",
        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    )
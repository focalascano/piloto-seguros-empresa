import streamlit as st
from fpdf import FPDF
import datetime
import os

# --- CONFIGURACIÓN DE PÁGINA ---
st.set_page_config(page_title="Determinador de Seguros", layout="centered")

# --- ESTILOS CSS PARA FORMATO ESTÉTICO ---
st.markdown("""
    <style>
    /* Fondo de la página en gris clarito */
    .stApp {
        background-color: #f0f2f6;
    }
    
    /* Contenedor del título en azul oscuro */
    .main-header {
        background-color: #002366;
        padding: 2.5rem;
        border-radius: 0.5rem;
        color: white;
        text-align: center;
        margin-bottom: 2rem;
    }
    .main-header h1 {
        color: white !important;
        margin-bottom: 0.5rem;
    }
    .main-header p {
        margin: 0;
        opacity: 0.9;
    }

    /* Estilo para el Botón de Anexo (Azul Oscuro) */
    div.stDownloadButton:nth-of-type(1) button {
        background-color: #002366 !important;
        color: white !important;
        border: none;
    }

    /* Estilo para el Botón de Checklist (Gris Claro) */
    div.stDownloadButton:nth-of-type(2) button {
        background-color: #e0e0e0 !important;
        color: black !important;
        border: 1px solid #cccccc;
    }
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
        self.set_font('Helvetica', 'B', 15)
        self.ln(10)

    def footer(self):
        self.set_y(-15)
        self.set_font('Helvetica', 'I', 8)
        self.cell(0, 10, f'Página {self.page_no()}', 0, 0, 'C')

    def chapter_title(self, title):
        self.set_font('Helvetica', 'B', 12)
        txt_safe = title.upper().encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 10, txt=txt_safe)
        self.ln(2)

    def chapter_body(self, body):
        self.set_font('Helvetica', '', 10)
        txt_safe = str(body).encode('latin-1', 'replace').decode('latin-1')
        self.multi_cell(0, 6, txt=txt_safe, align='J')
        self.ln(4)

# --- TEXTOS LEGALES ---
TEXTOS_LEGALES = {
    "GENERAL_ENCABEZADO": "La Contratista deberá acreditar ante La SOFSA, con una antelación mínima de CINCO (5) días corridos al inicio de los trabajos y/o servicios, la contratación y vigencia de los seguros que resulten aplicables en función de la naturaleza y riesgos de la prestación, debiendo exigir el cumplimiento de esta obligación a los Subcontratistas que eventualmente participen en la ejecución de sus obligaciones contractuales, cuando la contratación así lo permita:  ",
    "RC": """Seguros a presentar por la Contratista cuando, por la naturaleza de la actividad a desarrollar, exista riesgo de ocasionar daños a personas y/o a bienes de terceros: Seguro de Responsabilidad Civil Comprensiva: La Contratista deberá contratar y mantener vigente, por su exclusiva cuenta y cargo, un seguro de Responsabilidad Civil Comprensiva que deberá cubrir los daños a personas y/o bienes de terceros derivados directa o indirectamente de la ejecución de los trabajos y/o servicios contratados. En caso de insuficiencia o falta de cobertura, los daños deberán ser asumidos íntegramente por la Contratista. Ante el pago de un siniestro, la suma asegurada deberá ser repuesta dentro de los DIEZ (10) días de producido el mismo. Coberturas adicionales (condicionales): La póliza deberá incluir, cuando el riesgo asociado a la actividad lo requiera, los adicionales correspondientes a uso de grúas, izaje, andamios, trabajos de soldadura u oxicorte, carga y descarga, maquinaria, transporte de bienes, contaminación súbita y accidental, suministro de alimentos, uso de armas de fuego, uso de vehículos propios o no propios en exceso de su póliza específica y personas físicas bajo contrato. Previo al inicio de las tareas, la Contratista deberá presentar certificado de cobertura y libre deuda emitido por la aseguradora. Clausulas obligatorias: Asegurado Adicional: Serán considerados asegurados y/o asegurados adicionales el titular de la póliza y/o la empresa CUIT 30-71068177-1 y/o ADMINISTRACION DE INFRAESTRUCTURAS FERROVIARIAS SOCIEDAD ANONIMA (ADIFSA) CUIT 30- 71069599-3, y/o FERROCARRILES ARGENTINOS SOCIEDAD DEL ESTADO (FASE) - en proceso de transformación a Sociedad Anónima Unipersonal (SAU) - CUIT 30-71525570-3, y/o a SECRETARIA DE TRANSPORTE DE LA NACIÓN CUIT 30-71512720-9, y/o MINISTERIO DE ECONOMÍA CUIT 30-54667611-7, y/o al ESTADO NACIONAL, quienes serán coasegurados y/o asegurados adicionales a los efectos de la cobertura de la póliza, así como sus accionistas, directores, empleados y funcionarios. Responsabilidad Civil Cruzada: Todos los sujetos mencionados precedentemente serán considerados terceros entre sí. Cláusula de No Repetición: La Aseguradora renunciará expresamente a todo derecho de subrogación o repetición contra los sujetos mencionados precedentemente, manteniendo indemne a la empresa frente a reclamos de terceros cubiertos por la póliza. Notificación previa: La póliza no será anulada sin previo aviso por escrito a la OPERADORA FERROVIARIA SOCIEDAD ANONIMA, con domicilio en la Avda. Ramos Mejía Nº 1302, piso 4to. de la Ciudad Autónoma de Buenos Aires, con un plazo mínimo de 15 días corridos de anticipación.""",
    "ART": """Seguros a presentar por la Contratista para el personal que se encuentre en relación de dependencia, y que deba ingresar a predio de SOFSA en virtud de la presente contratación: Seguro de Riesgos del Trabajo: La Contratista deberá contratar y mantener vigente, por su exclusiva cuenta y cargo, un seguro que cubra los riesgos del trabajo de acuerdo con la Ley Nº 24.557 de Riesgos del Trabajo, sus reformas y decretos reglamentarios. Previo al inicio de las tareas, la Contratista deberá presentar certificado de cobertura emitido por la ART, incluyendo la nómina del personal afectado. La póliza deberá incluir la siguiente cláusula: Cláusula de No Repetición: La Aseguradora de Riesgos del Trabajo debe renunciar en forma expresa a sus derechos de subrogación y/o a reclamar o iniciar toda acción de repetición o de regreso contra SOFSA, y/o FASE - en proceso de transformación a Sociedad Anónima Unipersonal (SAU) - y/o ADIFSA y/o SECRETARIA DE TRANSPORTE DE LA NACIÓN, y/o MINISTERIO DE ECONOMÍA, y/o ESTADO NACIONAL así como sus accionistas, directors, empleados y funcionarios, con motivo de las prestaciones a las que se vea obligada a otorgar o abonar al personal dependiente o ex dependiente de la Contratista, amparados por la cobertura del contrato de afiliación, por accidente de trabajo o enfermedades profesionales ocurridos o contraídos por el hecho o en ocasión del trabajo o en el trayecto entre el domicilio del trabajador y el lugar de trabajo.""",
    "VO": """Seguro Colectivo de Vida Obligatorio: La Contratista deberá contratar y mantener vigente, por su exclusiva cuenta y cargo, un seguro colectivo de vida obligatorio para cubrir la totalidad del personal afectado al trabajo y/o servicio contratado, según lo previsto en el Decreto Nº 1567/74. Previo al inicio de las tareas, deberá presentarse certificado de cobertura emitido por la aseguradora, con indicación de la nómina del personal cubierto.""",
    "AP": """Seguros a presentar por la Contratista para el personal contratado que NO se encuentre en relación de dependencia, y que deba ingresar a predio de SOFSA en virtud de la presente contratación: Seguro de Accidentes Personales: La contratista deberá contratar y mantener vigente, por su exclusiva cuenta y cargo, un seguro que cubra los accidentes que pudiera sufrir el personal de la Contratista, afectado a los trabajos y/o servicios y que no se encuentre en relación de dependencia con ésta, cuando la modalidad contractual así lo permita. La cobertura mínima por persona deberá contemplar: Muerte e incapacidad permanente (total o parcial): USD 20.000 o su equivalente en moneda local. Gastos médicos asistenciales: USD 2.000 o su equivalente en moneda local. La póliza deberá designar a SOFSA como beneficiaria en primer término, exclusivamente a los efectos de garantizar su indemnidad frente a eventuales obligaciones legales derivadas del siniestro. Previo al inicio de las tareas, la Contratista deberá presentar certificado de cobertura y libre deuda emitido por la aseguradora. La póliza deberá incluir las siguientes cláusulas: Notificación previa: La póliza no será anulada sin previo aviso por escrito a la OPERADORA FERROVIARIA SOCIEDAD ANONIMA, con un plazo mínimo de 15 días corridos de anticipación.""",
    "CAUCION": """Caución de Tenencia de Bienes: La Contratista deberá contratar una Póliza de Caución de Tenencia de Bienes, destinada a garantizar el retiro, transporte, traslado, tenencia, guarda, custodia, correcta conservación y posterior devolución de los Bienes y/o Equipos propiedad de SOFSA y/o bajo su responsabilidad. La cobertura deberá mantenerse vigente desde el momento del retiro de los bienes de las instalaciones de SOFSA o del lugar que ésta determine, durante todo el período de traslado, permanencia, manipulación, intervención técnica y custodia en instalaciones de la Contratista o de terceros, hasta su efectiva devolución y recepción conforme por parte de SOFSA. La suma asegurada deberá ser equivalente a la suma establecida en el Pliego de Especificaciones Técnicas. La póliza deberá incluir la siguiente cláusula: Los actos, declaraciones, acciones u omisiones de la Contratista (Tomador), incluida la falta de pago del premio, no afectarán de modo alguno los derechos de SOFSA (Asegurada) frente al Asegurador, quien mantendrá íntegramente su obligación de responder en los términos de la póliza.""",
    "TRCYM": """Seguro a presentar por la Contratista para aquellos trabajos y/o servicios que requieran la realización de una obra y/o montaje: Seguros Todo riesgo Construcción y/o Montaje: Cuando la contratación implique la ejecución de obras y/o trabajos de montaje, la Contratista deberá contratar y mantener vigente, por su exclusiva cuenta y cargo, un Seguro Todo Riesgo Construcción y/o Montaje que ampare la totalidad de la obra y/o montaje, incluyendo trabajos temporarios, materiales, equipos, instalaciones, obradores, maquinarias y bienes existentes y/o adyacentes afectados a la prestación. La cobertura deberá mantenerse vigente durante todo el período de ejecución, incluyendo los períodos de almacenaje, construcción y/o montaje, pruebas y mantenimiento, y hasta la recepción definitiva de la obra, debiendo actualizarse progresivamente la suma asegurada de modo tal que refleje en todo momento el valor total certificado. La póliza deberá ser contratada a nombre conjunto de la Contratista y de SOFSA, y extenderse, cuando corresponda, a subcontratistas y/o proveedores que intervengan en la ejecución. La Contratista deberá presentar a SOFSA certificado de cobertura y libre deuda emitido por la aseguradora. Clausulas obligatorias: Asegurado Adicional: Serán considerados asegurados y/o asegurados adicionales el titular de la póliza y/o la La OPERADORA FERROVIARIA SOCIEDAD ANONIMA (SOFSA) CUIT 30-71068177-1 y/o ADMINISTRACION DE INFRAESTRUCTURAS FERROVIARIAS SOCIEDAD ANONIMA (ADIFSA) CUIT 30- 71069599-3, y/o FERROCARRILES ARGENTINOS SOCIEDAD DEL ESTADO (FASE) - en proceso de transformación a Sociedad Anónima Unipersonal (SAU) - CUIT 30-71525570-3, y/o a SECRETARIA DE TRANSPORTE DE LA NACIÓN CUIT 30-71512720-9, y/o MINISTERIO DE ECONOMÍA CUIT 30-54667611-7, y/o al ESTADO NACIONAL, quienes serán coasegurados y/o asegurados adicionales a los efectos de la cobertura de la póliza, así como sus accionistas, directores, empleados y funcionarios. Responsabilidad Civil Cruzada: Todos los sujetos mencionados precedentemente serán considerados terceros entre sí. Cláusula de No Repetición: La Aseguradora renunciará expresamente a todo derecho de subrogación o repetición contra los sujetos mencionados precedentemente, manteniendo indemne a SOFSA frente a reclamos de terceros cubiertos por la póliza. Notificación previa: La póliza no será anulada sin previo aviso por escrito a la OPERADORA FERROVIARIA SOCIEDAD ANONIMA, con un plazo mínimo de 15 días corridos de anticipación.""",
    "AUTO": """Seguro Automotor Obligatorio: La Contratista deberá contratar y mantener vigente, por su exclusiva cuenta y cargo, un seguro Automotor para los vehículos a ser utilizados en virtud de la presente contratación, los cuales deberán contar, como mínimo, con la cobertura de Responsabilidad Civil - Seguro Voluntario, por la suma establecida por la Superintendencia de Seguros de la Nación. La Contratista deberá presentar a SOFSA un certificado de cobertura y libre deuda emitido por la Aseguradora. La póliza deberá incluir las siguientes cláusulas: Cláusula de No Repetición: La Aseguradora renunciará expresamente a todo derecho de subrogación o repetición contra SOFSA, y/o FASE - en proceso de transformación a Sociedad Anónima Unipersonal (SAU) - y/o ADIFSA y/o SECRETARIA DE TRANSPORTE DE LA NACIÓN, y/o MINISTERIO DE ECONOMÍA, y/o ESTADO NACIONAL, así como sus accionistas, directores, empleados y funcionarios, con motivo de las sumas que se vea obligada a abonar por los riesgos amparados en la cobertura de la póliza. Notificación previa: La póliza no será anulada sin previo aviso por escrito a la OPERADORA FERROVIARIA SOCIEDAD ANONIMA, con domicilio en la Avda. Ramos Mejía Nº 1302, piso 4to. de la Ciudad Autónoma de Buenos Aires, con un plazo mínimo de 15 días corridos de anticipación.""",
    "REQUISITOS_FINALES": """Otros Seguros: SOFSA se reserva el derecho de exigir otros seguros que, en virtud de la contratación pudiesen ser requeridos. Requisitos de los Seguros: Las aseguradoras contratadas deberán cumplir con las siguientes condiciones: • Ser una aseguradora habilitada por la Superintendencia de Seguros de la Nación. • Estar calificada por alguna de las Calificadoras de Riesgo autorizadas por la Comisión Nacional de Valores (CNV). Se tomará como válida la calificación del año en que se adjudique la contratación y/o la calificación del año inmediato anterior a la adjudicación. La Contratista deberá presentar a la Licitante la calificación de riesgos de la Aseguradora. La Contratista deberá mantener y pagar el premio correspondiente a las pólizas. Los comprobantes de pago de las mismas deberán ser presentados a la Licitante de manera mensual y consecutiva. Vigencia de los Seguros: Los seguros deberán mantenerse vigentes desde el inicio de cualquier actividad vinculada a la contratación, incluyendo tareas previas, y hasta la extinción total de las obligaciones contractuales de la Contratista, comprendiendo la recepción provisoria, el período de garantía y toda intervención posterior vinculada al contrato. Incumplimientos en la Presentación de los Seguros: Si la Contratista no presentase los seguros que correspondan de acuerdo con la naturaleza de la actividad, los trabajos y/o los servicios a ejecutar, o no cumpliera con alguno de los requisitos establecidos en el presente Anexo, no podrá iniciar ni continuar las tareas hasta tanto regularice dicha situación, siendo de su exclusiva responsabilidad las consecuencias que ello genere, sin que ello otorgue derecho a reclamo alguno contra la SOFSA. Criterio de interpretación y aplicación: Ante cualquier duda razonable respecto de la aplicabilidad, alcance o suficiencia de los seguros exigidos en el presente Anexo, SOFSA tendrá la facultad de definir el seguro que resulte exigible, en función de la naturaleza de la prestación y de los riesgos involucrados. Responsabilidad: La contratación de seguros por parte de la Contratista no limita ni reduce en modo alguno su responsabilidad contractual ni legal, siendo ésta responsable directa por todos los daños y obligaciones derivados de la ejecución del contrato. En consecuencia, la Contratista asumirá a su exclusivo cargo las franquicias, descubiertos, diferencias de suma asegurada y todo daño o reclamo que no resulte cubierto por las pólizas contratadas. La Contratista mantendrá indemne a SOFSA, ADIFSA, FASE - en proceso de transformación a Sociedad Anónima Unipersonal (SAU)-, Secretaria de Transporte de la Nación, y/o al Estado Nacional, así como a sus accionistas, directores, empleados y funcionarios, frente a cualquier reclamo, suma, daño o gasto que deban afrontar con motivo de la ejecución contractual y/o del incumplimiento del régimen de seguros."""
}

# --- INTERFAZ ---
# Título con fondo azul oscuro y letra blanca
st.markdown("""
    <div class="main-header">
        <h1>MODELO DE DETERMINACIÓN DE SEGUROS A PROVEEDORES</h1>
        <p>Piloto institucional – Uso interno | Versión 1.0</p>
    </div>
    """, unsafe_allow_html=True)

st.info("""Herramienta de apoyo para la determinación estandarizada de seguros exigibles a proveedores y contratistas, basada en un modelo de evaluación de riesgo y reglas de decisión. 

Complete el siguiente cuestionario para describir el servicio o contratación. En caso de duda, responder **“Sí”**.""")

opciones = ["No", "Sí"]

r1 = st.radio("Pregunta 1: ¿Para realizar la actividad personal del proveedor ingresará a predios o instalaciones de SOFSA?", opciones, index=0)
r2 = st.radio("""Pregunta 2: ¿La actividad consiste exclusivamente en tareas administrativas o profesionales de oficina, realizadas sin ingreso a áreas operativas ni intervención técnica?  
Ejemplos: consultoría, auditoría, capacitaciones teóricas, asesoramiento profesional""", opciones, index=0)
r3 = st.radio("Pregunta 3: ¿La actividad requiere el ingreso de vehículos del proveedor a predios o instalaciones de SOFSA?", opciones, index=0)
r4 = st.radio("Pregunta 4: ¿El proveedor tendrá bajo su guarda, custodia o control bienes de SOFSA, sin supervisión directa, cuyo valor individual o total supere los USD 5.000?", opciones, index=0)
r5 = st.radio("Pregunta 5: ¿El trabajo se realizará en andenes, vías, talleres ferroviarios o sectores con circulación de trenes?", opciones, index=0)
r6 = st.radio("""Pregunta 6: ¿La actividad corresponde a un trabajo menor de mantenimiento simple en SOFSA? Para ser considerado trabajo menor, debe cumplir todas estas condiciones: 
• duración corta (menor a 1 mes de trabajo)  
• uso herramientas manuales simples  
• sin trabajo en altura, ni andamios  
• sin maquinaria pesada o equipos  
• sin intervención en infraestructura  
• sin afectar circulación ferroviaria o de pasajeros  
Ejemplos: (pintura interior de oficina, reparación menor de mobiliario, cerrajería, etc)""", opciones, index=0)
r7 = st.radio("""Pregunta 7: ¿La actividad requiere uso de equipos, maquinaria o de herramientas complejas en la empresa?  
Ejemplos: herramientas de corte y/o de calor y/o a explosión, equipos técnicos, maquinarias pesada""", opciones, index=0)
r8 = st.radio("""Pregunta 8: ¿La actividad incluye alguna de las siguientes tareas?  
• trabajos en altura  
• soldadura u oxicorte  
• izaje de cargas  
• intervención eléctrica  
• uso de maquinaria pesada  
• uso de armas de fuego  
• suministro de alimentos""", opciones, index=0)
r9 = st.radio("""Pregunta 9: ¿La actividad implica la ejecución de una obra o el montaje/instalación de un sistema o equipo nuevo, cuyo valor total supere los USD 30.000?  
Incluye:  
• obras civiles  
• refacciones estructurales  
• instalación de equipos (montaje o desmontaje)  
• montaje de sistema eléctrico o mecánico  
 
No incluye:  
• mantenimiento simple  
• refacciones menores  
• tareas de servicio""", opciones, index=0)

p1, p2, p3, p4, p5, p6, p7, p8, p9 = [(r == "Sí") for r in [r1, r2, r3, r4, r5, r6, r7, r8, r9]]

# --- VALIDACIONES DE BLOQUEO ---
bloqueo = False
if not p1 and (p3 or p4 or p5 or p6 or p7 or p8 or p9):
    st.error("""Bloqueo detectado: La pregunta 1 debe  responderse "Sí" para las tareas seleccionadas.""")
    bloqueo = True
if p2 and (p4 or p5 or p6 or p7 or p8 or p9):
    st.error("Bloqueo detectado: Tareas seleccionadas incompatibles con actividad administrativa (Pregunta 2).")
    bloqueo = True

st.markdown("---")
st.caption("""**Uso sugerido del resultado:** • Incorporar el Anexo de Seguros como referencia en el pliego  
• Utilizar el checklist de verificación documental previo al inicio de actividades  
Si el servicio o contratación no se puede describir mediante el cuestionario, contactar a la Subgerencia de Administración de Riesgos (SAR).  
""")

# --- LÓGICA DE RIESGO ---
if p9 or p8 or p5: nivel = "Alto"
elif p1 and (p7 or p4): nivel = "Medio"
elif p1: nivel = "Bajo"
else: nivel = "Nulo"

# --- GENERACIÓN DE DOCUMENTOS ---
if not bloqueo:
    if nivel == "Nulo":
        st.warning("El riesgo es nulo, no se requiere anexo de seguros.")
    else:
        st.write("---")
        col_btn1, col_btn2 = st.columns(2)

        with col_btn1:
            pdf_anexo = PDF()
            pdf_anexo.add_page()
            pdf_anexo.chapter_title("ANEXO DE SEGUROS")
            pdf_anexo.chapter_body(TEXTOS_LEGALES["GENERAL_ENCABEZADO"])
            pdf_anexo.chapter_body(TEXTOS_LEGALES["ART"])
            pdf_anexo.chapter_body(TEXTOS_LEGALES["VO"])
            pdf_anexo.chapter_body(TEXTOS_LEGALES["AP"])
            if p5 or p7 or p8 or p9:
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

        with col_btn2:
            chk = PDF()
            chk.add_page()
            chk.chapter_title("CHECKLIST DE CONTROL DOCUMENTAL")
            chk.chapter_body(f"Nivel de Riesgo Determinado: {nivel}")
            chk.chapter_body(f"Fecha de proceso: {datetime.datetime.now().strftime('%d/%m/%Y')}")
            chk.chapter_body("---")
            chk.chapter_body("Seguros requeridos para verificar:")
            chk.chapter_body("[ ] Seguro de Riesgos del Trabajo (ART)")
            chk.chapter_body("[ ] Seguro de Vida Obligatorio")
            chk.chapter_body("[ ] Seguro de Accidentes Personales (si corresponde)")
            if p5 or p7 or p8 or p9: chk.chapter_body("[ ] Seguro de Responsabilidad Civil Comprensiva")
            if p4: chk.chapter_body("[ ] Seguro de Caución por Tenencia de Bienes")
            if p9: chk.chapter_body("[ ] Seguro Todo Riesgo Construcción y Montaje")
            if p3: chk.chapter_body("[ ] Seguro Automotor")

            st.download_button(
                label="Generar Checklist de control",
                data=bytes(chk.output()),
                file_name=f"Checklist_Control_{nivel}.pdf",
                mime="application/pdf"
            )

# --- CARTEL DE RIESGO FINAL (Pequeño y al final) ---
if not bloqueo:
    st.write("") # Espacio
    if nivel == "Alto":
        st.error(f"**NIVEL DE RIESGO: {nivel}**")
    elif nivel == "Medio":
        st.warning(f"**NIVEL DE RIESGO: {nivel}**")
    elif nivel == "Bajo":
        st.info(f"**NIVEL DE RIESGO: {nivel}**")
    else:
        st.success(f"**NIVEL DE RIESGO: {nivel}**")

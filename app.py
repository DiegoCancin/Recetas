import streamlit as st
from reportlab.lib.colors import gray
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from PIL import Image
from datetime import datetime

# Función para agregar la imagen como marca de agua
def agregar_marca_agua_imagen(c):
    marca_agua = ImageReader('marca_agua.png')  # Ruta fija de la marca de agua
    c.saveState()
    c.setFillColor(gray, alpha=0.1)
    # Colocar la imagen de la marca de agua más pequeña y arriba
    c.drawImage('marca_agua.png', 208, 450, width=200, height=200, mask='auto')

# Función para generar el PDF
def generar_receta(datos):
    archivo_pdf = "receta_medica.pdf"
    c = canvas.Canvas(archivo_pdf, pagesize=letter)

    c.setFont("Helvetica", 12)

    # Logo de la institución educativa (ruta fija)
    c.drawImage('logo_institucion.png', 50, 685, width=80, height=65)  # Ruta fija del logo

    # Datos del doctor (fijos)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(200, 730, f"DR. CAMILO CANCÍN VICTORIANO")
    c.drawString(250, 715, f"MÉDICO CIRUJANO")
    c.drawString(245, 700, f"CÉD. PROF. 2047688")
    c.drawString(280, 685, f"UAEM")

    # Línea debajo de los datos del doctor
    c.line(30, 680, 580, 680)

    c.setFont("Helvetica", 12)
    # Datos del paciente y fecha
    c.drawString(30, 660, f"Nombre del paciente: {datos['paciente']['nombre']}")
    fecha_actual = datetime.now().strftime("%d/%m/%Y")
    c.drawString(480, 660, f"Fecha: {fecha_actual}")

    # "RP-" y signos vitales
    c.drawString(300, 630, "RP-")

    # Información de los signos vitales
    c.drawString(30, 620, f"Edad: {datos['signos_vitales']['edad']} años")
    c.drawString(30, 600, f"T.A.: {datos['signos_vitales']['ta']}")
    c.drawString(30, 580, f"F.C.: {datos['signos_vitales']['fc']}'")
    c.drawString(30, 560, f"F.R.: {datos['signos_vitales']['fr']}'")
    c.drawString(30, 540, f"TEMP.: {datos['signos_vitales']['temp']} °C")
    c.drawString(30, 520, f"PESO: {datos['signos_vitales']['peso']} Kgs")
    c.drawString(30, 500, f"TALLA: {datos['signos_vitales']['talla']} m.")
    c.drawString(30, 480, f"I.M.C.: {datos['signos_vitales']['imc']}")

    # Alergias e ID
    c.drawString(30, 460, f"Alergias: {datos['alergias']}")
    c.drawString(30, 440, f"I.D.: {datos['id']}")

    # Medicamentos
    y_pos = 615
    c.setFont("Helvetica-Bold", 12)
    c.drawString(150, y_pos, "Medicamentos:")
    y_pos -= 20
    for medicamento in datos['medicamentos']:
        c.setFont("Helvetica", 12)
        c.drawString(150, y_pos, f"{medicamento['nombre']} ({medicamento['tipo']}) {medicamento['dosis']} - Cada: {medicamento['cada_cuanto']} horas - Días: {medicamento['dias']} días")
        y_pos -= 20

    # Firma del médico
    c.drawString(400, 420, "Firma: _____________________")

    # Domicilio y teléfono debajo de la firma (datos estáticos)
    c.setFont("Helvetica", 8)
    c.drawString(40, 400,
                 f"DOMICILIO: ACEQUIA MZ 9 LT1 EDIF E DPTO 2 U.H. ANDRÉS MOLINA ENRIQUEZ, METEPEC, MÉXICO. 52149            TEL: 722 930 9430")

    # Agregar la imagen como marca de agua
    agregar_marca_agua_imagen(c)

    # Guardar el archivo PDF
    c.save()

# Crear la interfaz de Streamlit
def app():
    st.set_page_config(page_title="Generador de Receta Médica", page_icon="📑", layout="wide")

    # Título principal con estilo
    st.markdown("<h1 style='text-align: center; color: #0073e6;'>Generador de Receta Médica</h1>",
                unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    st.write("Completa los campos a continuación para generar la receta médica:")

    # Inicializar session_state para los medicamentos
    if 'medicamentos' not in st.session_state:
        st.session_state.medicamentos = []

    # Campos de entrada organizados en un formulario
    with st.form(key='receta_form'):
        col1, col2 = st.columns([1, 1])

        with col1:
            nombre_paciente = st.text_input('Nombre del paciente', max_chars=50)
            edad = st.text_input('Edad', max_chars=3)
            ta = st.text_input('T.A. (ej. 120/80)', max_chars=7)
            fc = st.text_input('F.C.', max_chars=5)
            fr = st.text_input('F.R.', max_chars=5)
            temp = st.text_input('Temperatura', max_chars=5)

        with col2:
            peso = st.text_input('Peso (kg)', max_chars=5)
            talla = st.text_input('Talla (m)', max_chars=5)
            imc = st.text_input('I.M.C.', max_chars=5)
            alergias = st.text_input('Alergias', max_chars=100)
            id_paciente = st.text_input('I.D. del paciente', max_chars=100)

        # Medicamentos dinámicos
        st.write("Medicamentos:")
        medicamento_nombre = st.text_input('Nombre del medicamento', key="med_nombre")
        medicamento_tipo = st.selectbox('Tipo de medicamento', ['Tableta', 'Suspensión', 'Cápsula', 'Inyección', 'Otro'], key="med_tipo")
        medicamento_dosis = st.text_input('Dosis del medicamento (ej. 500 mg)', max_chars=20, key="med_dosis")  # Cambiado a st.text_input
        medicamento_cada_cuanto = st.number_input('Cada cuánto (solo número, en horas)', min_value=0, key="med_cada_cuanto")
        medicamento_dias = st.number_input('Por cuantos días (solo número)', min_value=0, key="med_dias")

        if st.form_submit_button('Agregar medicamento'):
            if medicamento_nombre and medicamento_dosis and medicamento_cada_cuanto and medicamento_dias:
                st.session_state.medicamentos.append({
                    'nombre': medicamento_nombre,
                    'tipo': medicamento_tipo,
                    'dosis': medicamento_dosis,
                    'cada_cuanto': medicamento_cada_cuanto,
                    'dias': medicamento_dias
                })

    # Mostrar los medicamentos agregados con botón de eliminar (fuera del formulario)
    if st.session_state.medicamentos:
        st.write("Medicamentos agregados:")
        for i, medicamento in enumerate(st.session_state.medicamentos):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{medicamento['nombre']} ({medicamento['tipo']}) - {medicamento['dosis']} - Cada: {medicamento['cada_cuanto']} horas - Días: {medicamento['dias']} días")
            with col2:
                if st.button(f"Eliminar {i}"):
                    del st.session_state.medicamentos[i]
                    st.rerun()  # Usar st.rerun() en lugar de st.experimental_rerun()

    # Botón para generar el PDF
    if st.button("Generar PDF"):
        if not st.session_state.medicamentos:
            st.error("Debes agregar al menos un medicamento para generar la receta.")
        else:
            # Recopilar los datos en un diccionario
            datos_receta = {
                'paciente': {
                    'nombre': nombre_paciente,
                },
                'signos_vitales': {
                    'edad': edad,
                    'ta': ta,
                    'fc': fc,
                    'fr': fr,
                    'temp': temp,
                    'peso': peso,
                    'talla': talla,
                    'imc': imc
                },
                'alergias': alergias,
                'id': id_paciente,
                'medicamentos': st.session_state.medicamentos  # Agregar medicamentos
            }

            # Llamar a la función para generar el PDF
            generar_receta(datos_receta)

            # Mostrar un mensaje de confirmación
            st.success('Receta médica generada exitosamente!')

            # Mostrar el enlace para descargar el PDF
            with open("receta_medica.pdf", "rb") as file:
                st.download_button(
                    label="Descargar PDF",
                    data=file,
                    file_name="receta_medica.pdf",
                    mime="application/pdf"
                )

# Ejecutar la aplicación de Streamlit
if __name__ == "__main__":
    app()
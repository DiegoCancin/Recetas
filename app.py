import streamlit as st
import  pytz
from reportlab.lib.colors import gray
from reportlab.lib.pagesizes import letter
from reportlab.lib.utils import ImageReader
from reportlab.pdfgen import canvas
from datetime import datetime

# Función para agregar la imagen como marca de agua
def agregar_marca_agua_imagen(c):
    marca_agua = ImageReader('marca_agua.png')  # Ruta fija de la marca de agua
    c.saveState()
    c.setFillColor(gray, alpha=0.1)
    # Colocar la imagen de la marca de agua más pequeña y arriba
    c.drawImage('marca_agua.png', 208, 460, width=200, height=200, mask='auto')

# Función para manejar texto largo
def draw_wrapped_text(c, text, x, y, max_width, font_size):
    c.setFont("Helvetica", font_size)
    lines = []
    words = text.split()
    current_line = words[0]
    for word in words[1:]:
        test_line = current_line + " " + word
        if c.stringWidth(test_line, "Helvetica", font_size) < max_width:
            current_line = test_line
        else:
            lines.append(current_line)
            current_line = word
    lines.append(current_line)
    for line in lines:
        c.drawString(x, y, line)
        y -= font_size + 2  # Ajustar el espacio entre líneas

# Función para generar el PDF
def generar_receta(datos):
    archivo_pdf = "receta_medica.pdf"
    c = canvas.Canvas(archivo_pdf, pagesize=letter)

    c.setFont("Helvetica", 12)

    # Logo de la institución educativa (ruta fija)
    c.drawImage('logo_institucion.png', 50, 695, width=80, height=60)  # Ruta fija del logo

    # Datos del doctor (fijos)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(200, 740, f"DR. CAMILO CANCÍN VICTORIANO")
    c.drawString(250, 725, f"MÉDICO CIRUJANO")
    c.drawString(245, 710, f"CÉD. PROF. 2047688")
    c.drawString(280, 695, f"UAEM")

    # Línea debajo de los datos del doctor
    c.line(30, 690, 580, 690)

    c.setFont("Helvetica", 12)
    # Datos del paciente y fecha
    c.drawString(30, 670, f"Nombre del paciente: {datos['paciente']['nombre']}")
    # Definir la zona horaria de México
    zona_horaria_mexico = pytz.timezone('America/Mexico_City')
    fecha_actual = datetime.now(zona_horaria_mexico).strftime("%d/%m/%Y")
    c.drawString(480, 670, f"Fecha: {fecha_actual}")

    # "RP-" y signos vitales
    c.drawString(300, 640, "RP-")

    # Información de los signos vitales
    c.drawString(30, 630, f"Edad: {datos['signos_vitales']['edad']} años")
    c.drawString(30, 610, f"T.A.: {datos['signos_vitales']['ta']}")
    c.drawString(30, 590, f"F.C.: {datos['signos_vitales']['fc']}'")
    c.drawString(30, 570, f"F.R.: {datos['signos_vitales']['fr']}'")
    c.drawString(30, 550, f"TEMP.: {datos['signos_vitales']['temp']} °C")
    c.drawString(30, 530, f"PESO: {datos['signos_vitales']['peso']} Kgs")
    c.drawString(30, 510, f"TALLA: {datos['signos_vitales']['talla']} m.")
    c.drawString(30, 490, f"I.M.C.: {datos['signos_vitales']['imc']}")

    # Alergias e ID
    c.drawString(30, 470, f"Alergias: {datos['alergias']}")
    c.drawString(30, 450, f"I.D.: {datos['id']}")

    # Medicamentos
    y_pos = 625
    c.setFont("Helvetica-Bold", 14)
    c.drawString(150, y_pos, "Medicamentos:")
    y_pos -= 20
    for medicamento in datos['medicamentos']:
        c.setFont("Helvetica", 12)
        texto_medicamento = f"{medicamento['nombre']} {medicamento['gramos_medicamento']} ({medicamento['tipo']}) {medicamento['dosis']} - Cada: {medicamento['cada_cuanto']} horas - Días: {medicamento['dias']} días"
        draw_wrapped_text(c, texto_medicamento, 150, y_pos, 400, 12)
        y_pos -= 40  # Ajustar el espacio entre medicamentos

    # Firma del médico
    c.drawString(400, 430, "Firma: _____________________")

    # Domicilio y teléfono debajo de la firma (datos estáticos)
    c.setFont("Helvetica", 8)
    c.drawString(40, 410,
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

    # Inicializar session_state para los medicamentos y datos de la receta
    if 'medicamentos' not in st.session_state:
        st.session_state.medicamentos = []

    # Campos de entrada para los datos principales de la receta (sin formulario)
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

    # Formulario independiente para agregar medicamentos
    with st.form(key='medicamento_form', clear_on_submit=True):  # clear_on_submit solo limpia este formulario
        st.write("Agregar medicamento:")
        medicamento_nombre = st.text_input('Nombre del medicamento', key="med_nombre")
        gramos_medicamento = st.text_input('Gramos del medicamento (ej. 500 mg)', key="gram_nombre")
        medicamento_tipo = st.selectbox('Tipo de medicamento', ['Tableta', 'Suspensión', 'Cápsula', 'Inyección', 'Otro'], key="med_tipo")
        medicamento_dosis = st.text_input('Dosis del medicamento (ej. 2 tabletas o 2 ml)', max_chars=20, key="med_dosis")
        medicamento_cada_cuanto = st.number_input('Cada cuánto (solo número, en horas)', min_value=0, key="med_cada_cuanto")
        medicamento_dias = st.number_input('Por cuantos días (solo número)', min_value=0, key="med_dias")

        if st.form_submit_button('Agregar medicamento'):
            if medicamento_nombre and medicamento_dosis and medicamento_cada_cuanto and medicamento_dias:
                st.session_state.medicamentos.append({
                    'nombre': medicamento_nombre,
                    'gramos_medicamento': gramos_medicamento,
                    'tipo': medicamento_tipo,
                    'dosis': medicamento_dosis,
                    'cada_cuanto': medicamento_cada_cuanto,
                    'dias': medicamento_dias
                })

    # Mostrar los medicamentos agregados con botón de eliminar
    if st.session_state.medicamentos:
        st.write("Medicamentos agregados:")
        for i, medicamento in enumerate(st.session_state.medicamentos):
            col1, col2 = st.columns([4, 1])
            with col1:
                st.write(f"{medicamento['nombre']} {medicamento['gramos_medicamento']} ({medicamento['tipo']}) - {medicamento['dosis']} - Cada: {medicamento['cada_cuanto']} horas - Días: {medicamento['dias']} días")
            with col2:
                if st.button(f"Eliminar {i}"):
                    del st.session_state.medicamentos[i]
                    st.rerun()

    # Botón para generar el PDF
    if st.button("Generar receta"):
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

            # Guardar los datos en session_state para usarlos en la descarga
            st.session_state.datos_receta_generada = datos_receta

    # Botón para descargar el PDF (solo se muestra si la receta ha sido generada)
    if 'datos_receta_generada' in st.session_state:
        with open("receta_medica.pdf", "rb") as file:
            if st.download_button(
                label="Descargar PDF",
                data=file,
                file_name="receta_medica.pdf",
                mime="application/pdf"
            ):
                st.session_state.medicamentos = []
                del st.session_state.datos_receta_generada  # Eliminar los datos generados
                st.rerun()  # Recargar la página para reflejar los cambios

# Ejecutar la aplicación de Streamlit
if __name__ == "__main__":
    app()
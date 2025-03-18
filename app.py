import streamlit as st
from pdf_generator import generar_receta
from firebase_utils import obtener_medicamentos, obtener_forma_farmaceutica_por_id  # Funciones para obtener datos desde Firestore

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

    # Obtener los medicamentos desde Firestore
    medicamentos_firestore = obtener_medicamentos()

    # Ordenar los nombres de los medicamentos alfabéticamente (sin gramaje)
    nombres_medicamentos = sorted([med['nombre'] for med in medicamentos_firestore])

    # Campos de entrada para los datos principales de la receta
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

    # Selección de medicamento y campos relacionados
    st.write("Agregar medicamento:")
    medicamento_nombre = st.selectbox('Selecciona un medicamento', nombres_medicamentos, key="med_nombre")

    # Obtener el medicamento seleccionado desde Firestore
    try:
        medicamento_info = next(med for med in medicamentos_firestore if med['nombre'] == medicamento_nombre)
    except StopIteration:
        st.error("Medicamento no encontrado en la base de datos.")
        medicamento_info = None

    # Mostrar el gramaje y tipo del medicamento dinámicamente
    if medicamento_info:
        # Obtener el tipo de medicamento desde la referencia
        forma_id = medicamento_info['forma_id'].id
        forma = obtener_forma_farmaceutica_por_id(forma_id)

        # Mostrar el gramaje y tipo del medicamento
        st.text_input('Gramos del medicamento', value=f"{medicamento_info['gramaje']} {medicamento_info['unidad']}", key="gram_nombre", disabled=True)
        st.text_input('Tipo de medicamento', value=forma['nombre'], key="med_tipo", disabled=True)

        # Mostrar los ingredientes si es un medicamento compuesto
        if 'ingredientes' in medicamento_info:
            st.write("**Ingredientes:**")
            for ingrediente in medicamento_info['ingredientes']:
                st.write(f"- {ingrediente['nombre']}: {ingrediente['dosis']}")

        # Formulario para agregar medicamentos
    with st.form(key='medicamento_form', clear_on_submit=True):
        st.write("Detalles del medicamento:")

        # Campos para la dosis, frecuencia y días
        medicamento_dosis = st.text_input('Dosis del medicamento (ej. 2 tabletas o 2 ml)', max_chars=100,
                                          key="med_dosis")
        medicamento_cada_cuanto = st.number_input('Cada cuánto (solo número, en horas)', min_value=0,
                                                  key="med_cada_cuanto")
        medicamento_dias = st.number_input('Por cuantos días (solo número)', min_value=0, key="med_dias")

        # Botón para agregar medicamento
        if st.form_submit_button('Agregar medicamento'):
            if medicamento_info and medicamento_dosis and medicamento_cada_cuanto and medicamento_dias:
                st.session_state.medicamentos.append({
                    'nombre': medicamento_info['nombre'].upper(),
                    'gramos_medicamento': f"{medicamento_info['gramaje']} {medicamento_info['unidad']}",
                    'tipo': forma['nombre'].upper(),
                    'dosis': medicamento_dosis,
                    'cada_cuanto': medicamento_cada_cuanto,
                    'dias': medicamento_dias,
                    'ingredientes': medicamento_info.get('ingredientes', [])  # Agregar ingredientes si existen
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
import streamlit as st
from firebase_utils import (
    obtener_firestore,
    obtener_formas_farmaceuticas,
    agregar_medicamento
)

# Interfaz de Streamlit para agregar medicamentos
def add_medication():
    st.set_page_config(page_title="Agregar Medicamento", page_icon="💊", layout="wide")

    # Título principal
    st.markdown("<h1 style='text-align: center; color: #0073e6;'>Agregar Medicamento</h1>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Obtener la instancia de Firestore
    db = obtener_firestore()

    # Preguntar si es un medicamento compuesto
    es_compuesto = st.checkbox("¿Es un medicamento compuesto?")

    # Campos comunes para todos los medicamentos
    unidad = st.selectbox("Unidad", ["g", "mg", "mg/mL", "%", "ml", "UI"])  # Lista desplegable para seleccionar la unidad

    # Obtener la lista de formas farmacéuticas desde Firestore
    try:
        formas_farmaceuticas = obtener_formas_farmaceuticas()
        if formas_farmaceuticas:
            # Seleccionar la forma farmacéutica de una lista desplegable
            forma_seleccionada = st.selectbox(
                "Forma farmacéutica",
                options=formas_farmaceuticas,
                format_func=lambda x: x["nombre"],  # Mostrar el nombre de la forma farmacéutica
            )
            forma_id = forma_seleccionada["id"]  # Obtener el ID de la forma seleccionada
            forma_nombre = forma_seleccionada["nombre"]  # Obtener el nombre de la forma seleccionada
        else:
            st.error("No se encontraron formas farmacéuticas en la base de datos.")
            forma_id = None
            forma_nombre = None
    except Exception as e:
        st.error(f"Error al obtener formas farmacéuticas: {e}")
        forma_id = None
        forma_nombre = None

    # Campos específicos para medicamentos compuestos
    ingredientes = []
    gramaje = ""
    nombre = ""

    if es_compuesto:
        st.write("Ingresa los ingredientes:")
        num_ingredientes = st.number_input("Número de ingredientes", min_value=1, max_value=10, value=1)
        for i in range(num_ingredientes):
            st.write(f"Ingrediente {i + 1}:")
            nombre_ingrediente = st.text_input(f"Nombre del ingrediente {i + 1}", key=f"nombre_ingrediente_{i}")
            dosis_ingrediente = st.text_input(f"Dosis del ingrediente {i + 1} (solo número, ej. 0.500)",
                                              key=f"dosis_ingrediente_{i}")

            # Validar que la dosis sea un número
            try:
                float(dosis_ingrediente)  # Intenta convertir a número
                dosis_con_unidad = f"{dosis_ingrediente} {unidad}"  # Agregar la unidad a la dosis
                ingredientes.append({"nombre": nombre_ingrediente, "dosis": dosis_con_unidad})
            except ValueError:
                st.error(f"La dosis del ingrediente {i + 1} debe ser un número válido.")

        # Generar el nombre automáticamente concatenando los nombres de los ingredientes
        nombre = "-".join([ing["nombre"] for ing in ingredientes])  # Formato: "Amantadina-Clorfenamina-Paracetamol"

        # Generar el gramaje automáticamente a partir de las dosis de los ingredientes
        gramaje = ", ".join([ing["dosis"] for ing in ingredientes])  # Formato: "250 mg, 10 mg"
    else:
        # Campos para medicamentos no compuestos
        nombre = st.text_input("Nombre del medicamento", max_chars=100)
        gramaje = st.text_input("Gramaje (solo número, ej. 0.500)", max_chars=50)

        # Validar que el gramaje sea un número
        try:
            float(gramaje)  # Intenta convertir a número
        except ValueError:
            st.error("El gramaje debe ser un número válido.")

        # Agregar la forma farmacéutica al nombre entre paréntesis
        if forma_nombre:
            nombre = f"{nombre} ({forma_nombre})"

    # Botón para agregar el medicamento
    if st.button("Agregar Medicamento"):
        if nombre and unidad and forma_id:
            if es_compuesto and not ingredientes:
                st.error("Por favor, ingresa al menos un ingrediente para medicamentos compuestos.")
            else:
                # Si no es compuesto, agregar la unidad al gramaje
                if not es_compuesto:
                    gramaje = f"{gramaje}"

                # Intentar agregar el medicamento a Firestore
                try:
                    success, message = agregar_medicamento(nombre, gramaje, unidad, forma_id,
                                                           ingredientes if es_compuesto else None)
                    if success:
                        st.success(message)
                    else:
                        st.error(message)
                except Exception as e:
                    st.error(f"Error al agregar el medicamento: {e}")
        else:
            st.error("Por favor, completa todos los campos obligatorios.")


# Ejecutar la aplicación de Streamlit
if __name__ == "__main__":
    add_medication()
import os
import json
import firebase_admin
from firebase_admin import credentials, firestore

'''
# Cargar las credenciales desde una variable de entorno
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_credentials:
    raise ValueError("La variable de entorno FIREBASE_CREDENTIALS no está configurada.")

# Convertir la cadena JSON en un diccionario
cred_dict = json.loads(firebase_credentials)

# Inicializa la app de Firebase (solo una vez)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

# Función para obtener los medicamentos desde Firestore
def obtener_medicamentos():
    db = firestore.client()
    medicamentos_ref = db.collection('medicamentos')
    docs = medicamentos_ref.stream()

    medicamentos = []
    for doc in docs:
        medicamento = doc.to_dict()
        medicamento['id'] = doc.id  # Guarda el ID del documento
        medicamentos.append(medicamento)

    return medicamentos

# Función para obtener la forma farmacéutica por ID
def obtener_forma_farmaceutica_por_id(forma_id):
    db = firestore.client()
    forma_ref = db.collection('formas_farmaceuticas').document(forma_id)
    forma_doc = forma_ref.get()

    if forma_doc.exists:
        return forma_doc.to_dict()
    else:
        return None
'''
import os
import firebase_admin
from firebase_admin import credentials, firestore

# Cargar las credenciales desde una variable de entorno
firebase_credentials = os.getenv("FIREBASE_CREDENTIALS")

if not firebase_credentials:
    raise ValueError("La variable de entorno FIREBASE_CREDENTIALS no está configurada.")

# Convertir la cadena JSON en un diccionario
cred_dict = json.loads(firebase_credentials)

# Inicializa la app de Firebase (solo una vez)
cred = credentials.Certificate(cred_dict)
firebase_admin.initialize_app(cred)

# Obtener la instancia de Firestore
def obtener_firestore():
    return firestore.client()

# Función para obtener los medicamentos desde Firestore
def obtener_medicamentos():
    db = obtener_firestore()
    medicamentos_ref = db.collection('medicamentos')
    docs = medicamentos_ref.stream()

    medicamentos = []
    for doc in docs:
        medicamento = doc.to_dict()
        medicamento['id'] = doc.id  # Guarda el ID del documento
        medicamentos.append(medicamento)

    return medicamentos

# Función para obtener la forma farmacéutica por ID
def obtener_forma_farmaceutica_por_id(forma_id):
    db = obtener_firestore()
    forma_ref = db.collection('formas_farmaceuticas').document(forma_id)
    forma_doc = forma_ref.get()

    if forma_doc.exists:
        return forma_doc.to_dict()
    else:
        return None

# Función para obtener la lista de formas farmacéuticas desde Firestore
def obtener_formas_farmaceuticas():
    db = obtener_firestore()
    try:
        formas_ref = db.collection("formas_farmaceuticas").stream()
        formas = []
        for doc in formas_ref:
            forma = doc.to_dict()
            forma["id"] = doc.id  # Guardar el ID del documento
            formas.append(forma)
        return formas
    except Exception as e:
        raise Exception(f"Error al obtener las formas farmacéuticas: {e}")

# Función para agregar un medicamento a Firestore
def agregar_medicamento(nombre, gramaje, unidad, forma_id, ingredientes=None):
    db = obtener_firestore()
    try:
        # Crear el documento del medicamento
        medicamento_data = {
            "nombre": nombre,
            "gramaje": gramaje,
            "unidad": unidad,
            "forma_id": db.document(f"formas_farmaceuticas/{forma_id}")  # Referencia a la forma farmacéutica
        }

        # Agregar ingredientes si es un medicamento compuesto
        if ingredientes:
            # Asegurarse de que la dosis de cada ingrediente incluya la unidad
            for ingrediente in ingredientes:
                if unidad not in ingrediente["dosis"]:
                    ingrediente["dosis"] = f"{ingrediente['dosis']} {unidad}"
            medicamento_data["ingredientes"] = ingredientes

        # Agregar el medicamento a Firestore
        db.collection("medicamentos").add(medicamento_data)
        return True, f"Medicamento agregado: {nombre}"
    except Exception as e:
        return False, f"Error al agregar medicamento {nombre}: {e}"
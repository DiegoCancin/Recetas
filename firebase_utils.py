# firebase_utils.py
import firebase_admin
from firebase_admin import credentials, firestore

# Inicializa la app de Firebase (solo una vez)
cred = credentials.Certificate("recetas-cavic-firebase-adminsdk-fbsvc-723990aafd.json")
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

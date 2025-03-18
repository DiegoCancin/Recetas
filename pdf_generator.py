import pytz
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime
from utils import draw_wrapped_text, agregar_marca_agua_imagen

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

        # Extraer el nombre del medicamento sin paréntesis
        nombre_medicamento = medicamento['nombre'].split(' (')[0]

        # Verificar si es un medicamento compuesto (tiene ingredientes)
        if 'ingredientes' in medicamento and medicamento['ingredientes']:
            # Si es un medicamento compuesto, listar los ingredientes en una sola línea
            ingredientes_texto = ", ".join(
                [f"{ingrediente['nombre']} {ingrediente['dosis']}" for ingrediente in medicamento['ingredientes']])

            # Validar el tipo de medicamento compuesto y construir el texto personalizado
            if medicamento['tipo'] == 'TABLETA':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'SUSPENSIÓN':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Tomar {medicamento['dosis']} ml cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'JARABE':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Tomar {medicamento['dosis']} ml cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'INYECTABLE':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días Intramuscular"
            elif medicamento['tipo'] == 'SUERO':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Polvo/Solución Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días (Tomar a libre demanda)"
            elif medicamento['tipo'] == 'SUPOSITORIOS':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía rectal"
            elif medicamento['tipo'] == 'PERLAS':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'NASAL':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía nasal"
            elif medicamento['tipo'] == 'LOCAL CUTÁNEA':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} {medicamento['dosis']} aplicaciones cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días en la zona afectada"
            elif medicamento['tipo'] == 'VAGINAL':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía vaginal"
            elif medicamento['tipo'] == 'SUBCUTÁNEA':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía subcutánea"
            elif medicamento['tipo'] == 'CÁPSULA':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'RECTAL':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía rectal"
            elif medicamento['tipo'] == 'AEROSOL':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} {medicamento['dosis']} inhalaciones cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía inhalación"
            elif medicamento['tipo'] == 'ÓTICA':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía ótica"
            elif medicamento['tipo'] == 'OFTÁLMICA':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía oftálmica"
            elif medicamento['tipo'] == 'INHALACIÓN':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} {medicamento['dosis']} inhalaciones cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía inhalación"
            elif medicamento['tipo'] == 'INTRAVENOSA':
                texto_medicamento = f"{ingredientes_texto} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía intravenosa"
        else:
            # Si no es un medicamento compuesto, mostrar el gramaje general
            if medicamento['tipo'] == 'INYECTABLE':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días Intramuscular"
            elif medicamento['tipo'] == 'SUERO':
                texto_medicamento = f"{nombre_medicamento} Polvo/Solución Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días (Tomar a libre demanda)"
            elif medicamento['tipo'] == 'SUPOSITORIOS':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía rectal"
            elif medicamento['tipo'] == 'PERLAS':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'NASAL':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía nasal"
            elif medicamento['tipo'] == 'LOCAL CUTÁNEA':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} {medicamento['dosis']} aplicaciones cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días en la zona afectada"
            elif medicamento['tipo'] == 'SUSPENSIÓN':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Tomar {medicamento['dosis']} ml cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'VAGINAL':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía vaginal"
            elif medicamento['tipo'] == 'SUBCUTÁNEA':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía subcutánea"
            elif medicamento['tipo'] == 'CÁPSULA':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'TABLETA':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            elif medicamento['tipo'] == 'RECTAL':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía rectal"
            elif medicamento['tipo'] == 'AEROSOL':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} {medicamento['dosis']} inhalaciones cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía inhalación"
            elif medicamento['tipo'] == 'ÓTICA':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía ótica"
            elif medicamento['tipo'] == 'OFTÁLMICA':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía oftálmica"
            elif medicamento['tipo'] == 'INHALACIÓN':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} {medicamento['dosis']} inhalaciones cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía inhalación"
            elif medicamento['tipo'] == 'INTRAVENOSA':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Aplicar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas por {medicamento['dias']} días vía intravenosa"
            elif medicamento['tipo'] == 'JARABE':
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Tomar {medicamento['dosis']} ml cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"
            else:
                texto_medicamento = f"{nombre_medicamento} {medicamento['gramos_medicamento']} {medicamento['tipo']} Tomar {medicamento['dosis']} cada {medicamento['cada_cuanto']} horas vía oral por {medicamento['dias']} días"

        # Dibujar el texto del medicamento en el PDF
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
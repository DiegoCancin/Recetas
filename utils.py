from reportlab.lib.utils import ImageReader
from reportlab.lib.colors import gray

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
# app.py
from flask import Flask, render_template, request, redirect, url_for, flash
import datetime
from datetime import datetime, time, timedelta, date
import json
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_restaurante_porto_belo_2025'

# Arquivo para armazenar reservas
RESERVAS_FILE = 'reservas.json'

def cargar_reservas():
    if os.path.exists(RESERVAS_FILE):
        with open(RESERVAS_FILE, 'r') as f:
            return json.load(f)
    return []

def guardar_reserva(reserva):
    reservas = cargar_reservas()
    reservas.append(reserva)
    with open(RESERVAS_FILE, 'w') as f:
        json.dump(reservas, f, indent=2)

def verificar_disponibilidad(fecha, hora):
    reservas = cargar_reservas()
    hora_reserva = datetime.strptime(hora, '%H:%M').time()
    
    for reserva in reservas:
        if reserva['fecha'] == fecha:
            hora_existente = datetime.strptime(reserva['hora'], '%H:%M').time()
            # Verificar intervalo de 30 minutos
            diferencia = abs(
                datetime.combine(date.today(), hora_reserva) - 
                datetime.combine(date.today(), hora_existente)
            )
            if diferencia <= timedelta(minutes=30):
                return False
    return True

@app.route('/')
def index():
    return render_template('index.html', hoy=date.today().isoformat(), año_actual=datetime.now().year)

@app.route('/reservar', methods=['POST'])
def reservar():
    if request.method == 'POST':
        # Recoger datos del formulario
        nombre = request.form['nombre']
        telefono = request.form['telefono']
        fecha = request.form['fecha']
        hora = request.form['hora']
        personas = request.form['personas']
        comentarios = request.form.get('comentarios', '')
        
        # Validar campos obligatorios
        if not all([nombre, telefono, fecha, hora, personas]):
            flash('Por favor, complete todos los campos obligatorios.', 'error')
            return redirect(url_for('index'))
        
        # Validar fecha (no permitir fechas pasadas)
        try:
            fecha_reserva = datetime.strptime(fecha, '%Y-%m-%d').date()
            if fecha_reserva < datetime.today().date():
                flash('No se pueden hacer reservas para fechas pasadas.', 'error')
                return redirect(url_for('index'))
        except ValueError:
            flash('Formato de fecha incorrecto.', 'error')
            return redirect(url_for('index'))
        
        # Verificar disponibilidad
        if not verificar_disponibilidad(fecha, hora):
            flash('Lo sentimos, ese horario no está disponible. Por favor, elija otro horario con al menos 30 minutos de diferencia.', 'error')
            return redirect(url_for('index'))
        
        # Crear objeto reserva
        reserva = {
            'nombre': nombre,
            'telefono': telefono,
            'fecha': fecha,
            'hora': hora,
            'personas': personas,
            'comentarios': comentarios,
            'timestamp': datetime.now().isoformat()
        }
        
        # Guardar reserva
        guardar_reserva(reserva)
        
        # Crear mensaje para WhatsApp
        mensaje = f"Hola, me gustaría hacer una reserva:%0A%0A"
        mensaje += f"*Nombre:* {nombre}%0A"
        mensaje += f"*Teléfono:* {telefono}%0A"
        mensaje += f"*Fecha:* {fecha}%0A"
        mensaje += f"*Hora:* {hora}%0A"
        mensaje += f"*Personas:* {personas}%0A"
        if comentarios:
            mensaje += f"*Comentarios:* {comentarios}%0A"
        
        # Número de WhatsApp del restaurante
        numero_whatsapp = "34647525324"
        
        # Crear URL de WhatsApp
        url_whatsapp = f"https://wa.me/{numero_whatsapp}?text={mensaje}"
        
        # Mensaje de confirmación para el cliente
        mensaje_cliente = f"Gracias {nombre} por su reserva. Le confirmamos que hemos recibido su solicitud para el {fecha} a las {hora} para {personas} personas. Nos pondremos en contacto con usted pronto para confirmar. ¡Gracias!"
        
        flash('¡Reserva enviada con éxito! Será redirigido a WhatsApp para confirmar.', 'success')
        
        return render_template('reserva_confirmacion.html', 
                              url_whatsapp=url_whatsapp, 
                              mensaje_cliente=mensaje_cliente,
                              nombre=nombre,
                              telefono=telefono)
    
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
from flask import Flask, jsonify
import time


app = Flask(__name__)

# Estado global para simular caídas
is_healthy = True

@app.route('/health')
def health():
    if is_healthy:
        return jsonify(status="UP"), 200
    else:
        return jsonify(status="DOWN"), 500

@app.route('/off')
def set_off():
    global is_healthy
    is_healthy = False
    return "Servicio simulado como CAÍDO.\n"

@app.route('/on')
def set_on():
    global is_healthy
    is_healthy = True
    return "Servicio RESTABLECIDO.\n"

if __name__ == '__main__':
    print("⏳ Iniciando proceso de carga del sistema (espera forzada de 10s)...")
    time.sleep(10)  # El proceso de Python se bloquea aquí antes de levantar el servidor. Simulamos un proceso de inicializacion.
    print("🚀 Aplicación lista para recibir tráfico en el puerto 8000")
    app.run(host='0.0.0.0', port=8000)
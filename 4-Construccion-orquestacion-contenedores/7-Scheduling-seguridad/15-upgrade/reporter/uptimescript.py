import requests
import time
import sys

# --- Configuración ---
URL = "http://diplodevops.example:8080/uptime-app/health"
INTERVALO = 0.5  # 2 veces por segundo

def generar_reporte(inicio, fin, fallos, total_intentos):
    tiempo_total = fin - inicio
    # Calculamos el downtime basado en la proporción de fallos sobre el total de intentos
    proporcion_fallo = (fallos / total_intentos) if total_intentos > 0 else 0
    tiempo_down = tiempo_total * proporcion_fallo
    tiempo_up = tiempo_total - tiempo_down
    
    porcentaje_up = (1 - proporcion_fallo) * 100 if total_intentos > 0 else 0
    porcentaje_down = 100 - porcentaje_up

    print("\n\n" + "═"*45)
    print(" 📊 REPORTE FINAL DE DISPONIBILIDAD")
    print("═"*45)
    print(f" ⏱️  Duración total    : {tiempo_total:.2f} segundos")
    print(f" 🔍 Total de chequeos  : {total_intentos}")
    print("─"*45)
    print(f" ✅ Tiempo ONLINE      : {tiempo_up:.2f}s ({porcentaje_up:.2f}%)")
    print(f" ❌ Tiempo DOWNTIME    : {tiempo_down:.2f}s ({porcentaje_down:.2f}%)")
    print("═"*45)

def monitorear():
    fallos = 0
    intentos = 0
    
    print(f"🚀 Monitoreando: {URL}")
    print("Presiona [Ctrl+C] para detener y ver el reporte...")
    
    t_inicio = time.time()
    
    try:
        while True:
            intentos += 1
            try:
                # Timeout corto para no retrasar el siguiente ciclo
                response = requests.get(URL, timeout=0.4)
                if not response.ok:
                    fallos += 1
            except (requests.exceptions.RequestException):
                fallos += 1
            
            # Feedback visual simple en una sola línea
            sys.stdout.write(f"\rIntentos: {intentos} | Fallos: {fallos}")
            sys.stdout.flush()
            
            time.sleep(INTERVALO)
            
    except KeyboardInterrupt:
        # Aquí es donde ocurre la magia: al presionar Ctrl+C se ejecuta esto
        t_fin = time.time()
        generar_reporte(t_inicio, t_fin, fallos, intentos)
        print("\nMonitoreo finalizado por el usuario.")

if __name__ == "__main__":
    monitorear()
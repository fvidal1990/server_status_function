from flask import Flask, request, jsonify
import psutil, requests

app = Flask(__name__)

@app.route('/')
def home():
    return "Servidor Flask activo ✅"

@app.route('/server_status')
def server_status():
    cpu = psutil.cpu_percent(1)
    mem = psutil.virtual_memory().percent
    estado = "OK" if cpu < 80 and mem < 80 else "ALERTA"
    data = {"cpu": cpu, "memoria": mem, "estado": estado}

    # Simula notificación a webhook (puedes usar https://webhook.site)
    webhook_url = "https://webhook.site/1475dc15-e429-49f3-ab73-6057297fe772"
    try:
        requests.post(webhook_url, json=data)
    except Exception as e:
        print("Error al notificar:", e)

    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)

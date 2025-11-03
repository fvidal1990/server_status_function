from flask import Flask, jsonify
import psutil, platform, datetime, requests

app = Flask(__name__)

@app.route('/')
def home():
    return """
    <h2>Panel de Servidor activo clase MTT612</h2>
    <p>Ver detalle <a href='/server_status'>aquí</a>.</p>
    """

@app.route('/server_status')
def server_status():
    cpu = psutil.cpu_percent(1)
    mem = psutil.virtual_memory().percent
    disco = psutil.disk_usage('/').percent
    so = platform.system() + " " + platform.release()
    hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    estado = "OK" if cpu < 80 and mem < 80 and disco < 90 else "ALERTA"

    data = {
        "hora": hora,
        "sistema_operativo": so,
        "cpu": cpu,
        "memoria": mem,
        "disco": disco,
        "estado": estado
    }

    # enviar a webhook opcional
    try:
        requests.post("https://webhook.site/tu-url", json=data)
    except:
        pass

    # render HTML legible también
    html = f"""
    <h3>📊 Estado del Servidor</h3>
    <ul>
      <li><b>Estado:</b> {estado}</li>
      <li><b>Hora:</b> {hora}</li>
      <li><b>Sistema:</b> {so}</li>
      <li><b>CPU:</b> {cpu}%</li>
      <li><b>Memoria:</b> {mem}%</li>
      <li><b>Disco:</b> {disco}%</li>
      
    </ul>
    <p>JSON: <a href="/server_status_json">/server_status_json</a></p>
    """
    return html

@app.route('/server_status_json')
def server_status_json():
    cpu = psutil.cpu_percent(1)
    mem = psutil.virtual_memory().percent
    disco = psutil.disk_usage('/').percent
    so = platform.system() + " " + platform.release()
    hora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    estado = "OK" if cpu < 80 and mem < 80 and disco < 90 else "ALERTA"
    return jsonify({
        "hora": hora,
        "sistema_operativo": so,
        "cpu": cpu,
        "memoria": mem,
        "disco": disco,
        "estado": estado
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


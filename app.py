from flask import Flask, render_template_string, request, redirect, url_for, jsonify
import folium
import os
import requests

app = Flask(__name__)

# Verifique se a pasta "static" existe
if not os.path.exists("static"):
    os.makedirs("static")

# Coordenadas iniciais para centralizar o mapa em Salvador, Bahia
latitude_inicial = -12.9714
longitude_inicial = -38.5014

# Função para criar o mapa com coordenadas iniciais e marcadores
def criar_mapa(lat, lng, marcadores=[]):
    mapa = folium.Map(
        location=[lat, lng],
        zoom_start=12,
        tiles="OpenStreetMap"
    )
    
    # Adiciona marcadores ao mapa
    for idx, marcador in enumerate(marcadores):
        folium.Marker(
            [marcador['lat'], marcador['lng']],
            popup=f'<button onclick="parent.postMessage({{lat: {marcador["lat"]}, lng: {marcador["lng"]}, index: {idx}}}, \'*\')">Mostrar Endereço</button>'
        ).add_to(mapa)
    
    return mapa

# Rota principal
@app.route("/", methods=["GET", "POST"])
def index():
    marcadores = []
    if os.path.exists("marcadores.txt"):
        with open("marcadores.txt", "r") as f:
            for line in f:
                lat, lng = map(float, line.strip().split(","))
                marcadores.append({"lat": lat, "lng": lng})

    if request.method == "POST":
        lat = request.form.get("latitude")
        lng = request.form.get("longitude")

        try:
            lat = float(lat)
            lng = float(lng)
            marcadores.append({"lat": lat, "lng": lng})
            
            with open("marcadores.txt", "a") as f:
                f.write(f"{lat},{lng}\n")

            mapa = criar_mapa(latitude_inicial, longitude_inicial, marcadores)
            mapa.save("static/mapa_interativo.html")

        except ValueError:
            return "Coordenadas inválidas. Por favor, insira valores numéricos.", 400

        return redirect(url_for("index"))

    mapa = criar_mapa(latitude_inicial, longitude_inicial, marcadores)
    mapa.save("static/mapa_interativo.html")

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mapa Interativo com Marcação</title>
            <style>
                * {
                    box-sizing: border-box;
                    font-family: Arial, sans-serif;
                }
                body {
                    margin: 0;
                    display: flex;
                    height: 100vh;
                    flex-direction: column;
                    background-color: #f8f9fa;
                }
                .navbar {
                    background-color: #f0f0f0;
                    padding: 1rem;
                    color: #333;
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                    position: fixed;
                    width: 100%;
                    top: 0;
                    z-index: 1000;
                }
                .navbar a {
                    color: #333;
                    margin: 0 15px;
                    text-decoration: none;
                    font-weight: bold;
                }
                .content {
                    margin-top: 60px; /* Altura da navbar para evitar sobreposição */
                }
                h1 {
                    color: #333;
                }
                .form-container {
                    padding: 1rem;
                    max-width: 400px;
                    margin: auto;
                    text-align: center;
                    background-color: #fff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                label {
                    display: block;
                    font-size: 14px;
                    color: #555;
                    margin-bottom: 5px;
                }
                input[type="text"] {
                    width: calc(100% - 20px);
                    padding: 10px;
                    border-radius: 5px;
                    border: 1px solid #ddd;
                    font-size: 14px;
                    margin-bottom: 10px;
                }
                button {
                    padding: 10px 20px;
                    background-color: #007bff;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                    font-size: 16px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                button:hover {
                    background-color: #0056b3;
                }
                .map-container {
                    flex: 1;
                    overflow: hidden;
                    display: flex;
                    justify-content: center;
                    padding: 10px;
                }
                .map-container iframe {
                    width: 100%;
                    max-width: 800px;
                    height: 500px;
                    border: none;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                }
                aside {
                    position: fixed;
                    top: 20px;
                    right: 20px;
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    padding: 15px;
                    width: 300px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                    display: none;
                }
                aside h2 {
                    font-size: 18px;
                    margin-bottom: 10px;
                }
                aside p {
                    font-size: 14px;
                    color: #555;
                }
                aside img {
                    width: 100%;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="navbar">
                <a href="{{ url_for('index') }}">Página Inicial</a>
                <a href="{{ url_for('incidentes') }}">Incidentes</a>
            </div>
            <div class="content">
                <div class="form-container">
                    <h1>Adicionar Marcação no Mapa</h1>
                    <form action="/" method="POST">
                        <label for="latitude">Latitude:</label>
                        <input type="text" id="latitude" name="latitude" required>
                        <label for="longitude">Longitude:</label>
                        <input type="text" id="longitude" name="longitude" required>
                        <button type="submit">Adicionar Marcação</button>
                    </form>
                </div>
                <div class="map-container">
                    <iframe src="{{ url_for('static', filename='mapa_interativo.html') }}" id="mapFrame"></iframe>
                </div>
            </div>
            <aside id="infoBox">
                <h2>Endereço do Marcador</h2>
                <p id="endereco"></p>
                <img id="imagem" src="" alt="Imagem do Local">
                <button onclick="fecharInfoBox()">Fechar</button>
            </aside>

            <script>
                window.addEventListener("message", async function(event) {
                    if (event.data.lat && event.data.lng) {
                        const lat = event.data.lat;
                        const lng = event.data.lng;

                        const response = await fetch(`/get_address?lat=${lat}&lng=${lng}`);
                        const data = await response.json();
                        document.getElementById('endereco').innerText = data.address;
                        
                        const imageResponse = await fetch(`https://source.unsplash.com/400x300/?${data.city}`);
                        document.getElementById('imagem').src = imageResponse.url;

                        document.getElementById('infoBox').style.display = 'block';
                    }
                });

                function fecharInfoBox() {
                    document.getElementById('infoBox').style.display = 'none';
                }
            </script>
        </body>
        </html>
    ''', markers=marcadores)

# Página de incidentes
@app.route("/incidentes")
def incidentes():
    marcadores = []
    if os.path.exists("marcadores.txt"):
        with open("marcadores.txt", "r") as f:
            for line in f:
                lat, lng = map(float, line.strip().split(","))
                marcadores.append({"lat": lat, "lng": lng})

    return render_template_string('''
        <!DOCTYPE html>
        <html lang="pt-br">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Mapa de Incidentes</title>
            <style>
                * {
                    box-sizing: border-box;
                    font-family: Arial, sans-serif;
                }
                body, html {
                    margin: 0;
                    overflow: hidden;
                    height: 100%;
                }
                .navbar {
                    background-color: #f0f0f0;
                    padding: 1rem;
                    color: #333;
                    text-align: center;
                    border-bottom: 1px solid #ddd;
                    position: fixed;
                    width: 100%;
                    top: 0;
                    z-index: 1000;
                }
                .navbar a {
                    color: #333;
                    margin: 0 15px;
                    text-decoration: none;
                    font-weight: bold;
                }
                .map-container {
                    display: flex;
                    height: calc(100vh - 60px);
                    position: relative;
                    margin-top: 60px; /* Altura da navbar */
                }
                .map-container iframe {
                    flex: 1;
                    border: none;
                }
                .incident-sidebar {
                    position: absolute;
                    left: 0;
                    top: 0;
                    bottom: 0;
                    width: 300px;
                    background-color: #f9f9f9;
                    padding: 20px;
                    overflow-y: auto;
                    border-right: 1px solid #ddd;
                }
                .incident-sidebar h2 {
                    margin-top: 0;
                }
                .incident-card {
                    background-color: #fff;
                    border: 1px solid #ddd;
                    border-radius: 5px;
                    padding: 15px;
                    margin-bottom: 10px;
                    cursor: pointer;
                    transition: background-color 0.3s;
                }
                .incident-card:hover {
                    background-color: #e0e0e0;
                }
                .clear-btn {
                    display: block;
                    width: 100%;
                    padding: 10px;
                    margin-top: 20px;
                    background-color: #dc3545;
                    color: #fff;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                    font-size: 16px;
                    transition: background-color 0.3s;
                }
                .clear-btn:hover {
                    background-color: #c82333;
                }
                /* Popup com fundo embaçado */
                .popup-overlay {
                    position: fixed;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background-color: rgba(0, 0, 0, 0.5);
                    display: none;
                    justify-content: center;
                    align-items: center;
                }
                .popup-card {
                    background-color: #fff;
                    padding: 20px;
                    border-radius: 8px;
                    max-width: 400px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
                }
                .popup-card p {
                    margin-top: 0;
                }
                .popup-card img {
                    width: 100%;
                    border-radius: 5px;
                    margin-top: 10px;
                }
            </style>
        </head>
        <body>
            <div class="navbar">
                <a href="{{ url_for('index') }}">Página Inicial</a>
                <a href="{{ url_for('incidentes') }}">Incidentes</a>
            </div>
            <div class="map-container">
                <div class="incident-sidebar">
                    <h2>Incidentes</h2>
                    <div id="incidentList">
                        {% for marker in markers %}
                        <div class="incident-card" onclick="mostrarInfo({{ marker.lat }}, {{ marker.lng }})">
                            <p>{{ marker.lat }}, {{ marker.lng }}</p>
                        </div>
                        {% endfor %}
                    </div>
                    <button class="clear-btn" onclick="deletarMarcadores()">Deletar Todas as Marcações</button>
                </div>
                <iframe src="{{ url_for('static', filename='mapa_interativo.html') }}" id="mapFrame"></iframe>
            </div>
            <div class="popup-overlay" id="popupOverlay">
                <div class="popup-card">
                    <p id="popupEndereco"></p>
                    <img id="popupImagem" src="" alt="Imagem do Local">
                    <button onclick="fecharPopup()">Fechar</button>
                </div>
            </div>

            <script>
                async function mostrarInfo(lat, lng) {
                    const response = await fetch(`/get_address?lat=${lat}&lng=${lng}`);
                    const data = await response.json();
                    document.getElementById('popupEndereco').innerText = data.address;

                    const imageResponse = await fetch(`https://source.unsplash.com/400x300/?${data.city}`);
                    document.getElementById('popupImagem').src = imageResponse.url;

                    document.getElementById('popupOverlay').style.display = 'flex';
                }

                function fecharPopup() {
                    document.getElementById('popupOverlay').style.display = 'none';
                }

                async function deletarMarcadores() {
                    const response = await fetch("/delete_markers", { method: "POST" });
                    if (response.ok) {
                        window.location.reload();
                    }
                }
            </script>
        </body>
        </html>
    ''', markers=marcadores)

# Endpoint para deletar todas as marcações
@app.route("/delete_markers", methods=["POST"])
def delete_markers():
    if os.path.exists("marcadores.txt"):
        os.remove("marcadores.txt")
    return jsonify({"success": True})

@app.route("/get_address")
def get_address():
    lat = request.args.get("lat")
    lng = request.args.get("lng")
    response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={lat}&lon={lng}&addressdetails=1")
    data = response.json()
    address = data.get("address", {})
    endereco_simplificado = f"{address.get('road', 'N/A')}, {address.get('suburb', 'N/A')}, {address.get('city', 'N/A')}, {address.get('state', 'N/A')}, {address.get('postcode', 'N/A')}"
    return jsonify({"address": endereco_simplificado, "city": address.get('city', 'N/A')})

if __name__ == "__main__":
    app.run(debug=True)

import sys
import os
import folium
import requests
from PyQt5.QtWidgets import QApplication, QMainWindow, QVBoxLayout, QWidget, QLineEdit, QPushButton, QMessageBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl

class MapaApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Mapa Interativo com Marcação")
        self.setGeometry(100, 100, 800, 600)

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.layout = QVBoxLayout(self.central_widget)

        # Input para Localização
        self.location_input = QLineEdit(self)
        self.location_input.setPlaceholderText("Digite uma localização")

        self.add_button = QPushButton("Adicionar Marcação", self)
        self.add_button.clicked.connect(self.adicionar_marcacao)

        self.layout.addWidget(self.location_input)
        self.layout.addWidget(self.add_button)

        # Mapa
        self.map_view = QWebEngineView(self)
        self.layout.addWidget(self.map_view)

        # Carregar o mapa inicial
        self.marcadores = []
        self.carregar_mapa()

    def carregar_mapa(self):
        latitude_inicial = -12.9714
        longitude_inicial = -38.5014
        mapa = folium.Map(location=[latitude_inicial, longitude_inicial], zoom_start=12)

        for marcador in self.marcadores:
            folium.Marker(
                [marcador['lat'], marcador['lng']],
                popup=f'Lat: {marcador["lat"]}, Lng: {marcador["lng"]}'
            ).add_to(mapa)

        mapa.save("mapa_interativo.html")
        self.map_view.setUrl(QUrl.fromLocalFile(os.path.abspath("mapa_interativo.html")))

    def adicionar_marcacao(self):
        location = self.location_input.text()

        if not location:
            QMessageBox.warning(self, "Erro", "Por favor, insira uma localização.")
            return

        # Usar a API do Nominatim para obter coordenadas
        headers = {'User-Agent': 'MapaApp'}
        response = requests.get(
            f"https://nominatim.openstreetmap.org/search?q={location}&format=json&addressdetails=1",
            headers=headers
        )

        if response.status_code == 200:
            data = response.json()
            if data:
                lat = float(data[0]["lat"])
                lng = float(data[0]["lon"])
                self.marcadores.append({"lat": lat, "lng": lng})
                self.carregar_mapa()
                self.location_input.clear()
            else:
                QMessageBox.warning(self, "Erro", "Localização não encontrada.")
        else:
            QMessageBox.warning(self, "Erro", "Erro ao acessar o serviço de geocodificação.")

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MapaApp()
    window.show()
    sys.exit(app.exec_())
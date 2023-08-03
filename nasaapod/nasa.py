import sys
import requests
import os
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QScrollArea, QPushButton
from PyQt5.QtGui import QPixmap, QFont, QIcon
from PyQt5.QtCore import Qt

API_KEY = "DEMO_KEY"
API_URL = f"https://api.nasa.gov/planetary/apod?api_key={API_KEY}"

class APODApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Astronomy Picture of the Day - GumusSpace")
        self.setGeometry(100, 100, 800, 600)

        self.init_ui()

    def init_ui(self):
        self.setStyleSheet("background-color: #222; color: white;")

        main_layout = QVBoxLayout(self)
        main_layout.setAlignment(Qt.AlignCenter)

        scroll_area = QScrollArea(self)

        apod_data = self.get_apod_data()

        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.image_label.setScaledContents(True)
        main_layout.addWidget(self.image_label)

        self.title_label = QLabel(apod_data["title"], self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 24, QFont.Bold))
        main_layout.addWidget(self.title_label)

        self.date_label = QLabel(apod_data["date"], self)
        self.date_label.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.date_label)

        self.explanation_label = QLabel(self)
        self.explanation_label.setWordWrap(True)
        self.explanation_label.setStyleSheet("QLabel { background-color: #333; padding: 10px; }")
        self.explanation_label.setFont(QFont("Arial", 16))
        main_layout.addWidget(self.explanation_label)

        self.download_button = QPushButton("Download Image", self)
        self.download_button.setStyleSheet("QPushButton { background-color: #3498db; color: white; }")
        self.download_button.clicked.connect(self.download_image)
        main_layout.addWidget(self.download_button)

        scroll_widget = QWidget(self)
        scroll_widget.setLayout(main_layout)
        scroll_area.setWidget(scroll_widget)
        scroll_area.setWidgetResizable(True)

        main_layout_outer = QVBoxLayout(self)
        main_layout_outer.addWidget(scroll_area)
        self.setLayout(main_layout_outer)

        self.update_data(apod_data)

    def get_apod_data(self):
        response = requests.get(API_URL)
        data = response.json()
        return data

    def update_data(self, apod_data):
        image_url = apod_data["url"]
        image_data = requests.get(image_url).content
        pixmap = QPixmap()
        pixmap.loadFromData(image_data)
        self.image_label.setPixmap(pixmap)
        self.image_label.setFixedSize(pixmap.size())

        explanation = apod_data["explanation"]
        html_explanation = f"<div style='font-size: 14px;'>{explanation}</div>"
        self.explanation_label.setText(html_explanation)

    def download_image(self):
        apod_data = self.get_apod_data()
        image_url = apod_data["url"]
        image_data = requests.get(image_url).content

        file_name = os.path.join(os.path.dirname(__file__), os.path.basename(image_url))
        with open(file_name, "wb") as f:
            f.write(image_data)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = APODApp()

#Kendi uzantınızı girin.
    icon_path = "nasa.ico"
    app_icon = QIcon(icon_path)
    window.setWindowIcon(app_icon)

    window.show()
    sys.exit(app.exec_())
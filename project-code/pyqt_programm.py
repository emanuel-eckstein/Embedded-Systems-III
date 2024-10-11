from opcua import Client, ua
from PyQt5 import QtWidgets, QtGui, QtCore
import sys
import os

def receive_Datas(status):
    match status:
        case 0:
            return ".../Bilder/Grundkonzept.png"
        case 1:
            return ".../Bilder/PRESS_OUT.png"
        case 2:
            return ".../Bilder/STAMP.png"
        case 3:
            return ".../Bilder/CHECK.png"
        case 4:
            return ".../Bilder/STOP.png"
        case 5:
            return ".../Bilder/OUTSOURCE.png"
        case 6:
            return ".../Bilder/FREE.png"

def start():
    start_node.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))

# Hauptklasse für das PyQt-Interface
class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        # OPC UA Client
        self.url = "opc.tcp://192.168.0.100:4840"
        self.client = Client(self.url)
        self.client.connect()

        # Nodes für SPS anlegen
        self.start_node = self.client.get_node("ns=7;s=::AsGlobalPV:di_start_opc")
        self.status_node = self.client.get_node("ns=6;s=::Program:SM_PRODUCING_MACHINE")

        # UI-Elemente erstellen
        self.initUI()

        # Timer für die Bildaktualisierung
        self.timer = QtCore.QTimer(self)
        self.timer.timeout.connect(self.update_image)
        self.timer.start(500)  # Alle 500 ms aktualisieren

    def initUI(self):
        # Fenstergröße und Titel setzen
        self.setWindowTitle("Visualisierung Automatisierungsanlage")
        self.setGeometry(100, 100, 480, 272)

        # Layout erstellen
        self.layout = QtWidgets.QVBoxLayout(self)

        # Label zur Bilderanzeige
        self.image_label = QtWidgets.QLabel(self)
        self.layout.addWidget(self.image_label)

        # Button für den Start
        self.start_button = QtWidgets.QPushButton("Start", self)
        self.start_button.clicked.connect(start)
        self.layout.addWidget(self.start_button)

        # self.stop_button = QtWidgets.QPushButton("Stop", self)
        # self.layout.addWidget(self.stop_button)

    def update_image(self):
        status = self.status_node.get_value()
        datapath = receive_Datas(status)

        # Bild laden und anzeigen
        if os.path.exists(datapath):
            pixmap = QtGui.QPixmap(datapath)
            self.image_label.setPixmap(pixmap.scaled(480, 272, QtCore.Qt.KeepAspectRatio))
        else:
            print(f"Bildpfad existiert nicht: {datapath}")

    def closeEvent(self, event):
        # Trenne die Verbindung zum OPC UA Server beim Schließen des Fensters
        self.client.disconnect()
        event.accept()


# Hauptprogramm
if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
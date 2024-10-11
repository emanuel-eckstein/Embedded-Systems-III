from opcua import Client, ua
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from kivy.uix.label import Label
from kivy.clock import Clock
import os


def receive_Datas(status):
    match status:
        case 0:
            return "Grundkonzept"
        case 1:
            return "PRESS_OUT"
        case 2:
            return "STAMP"
        case 3:
            return "CHECK"
        case 4:
            return "STOP"
        case 5:
            return "OUTSOURCE"
        case 6:
            return "FREE"
        case _:
            return "Unbekannter Status"


class OPCUAGUI(BoxLayout):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        # Layout erstellen
        self.orientation = 'vertical'
        
        # Label zur Anzeige des Status
        self.status_label = Label(text='Status: Wartet auf Start...', font_size=24)
        self.add_widget(self.status_label)

        # Start-Button
        self.start_button = Button(text='Start', size_hint=(1, 0.1))
        self.start_button.bind(on_press=self.start)
        self.add_widget(self.start_button)

        # OPC-UA Client verbinden
        self.client = Client("opc.tcp://192.168.0.100:4840")
        self.start_node = None
        self.status_node = None

        try:
            self.client.connect()
            print("Verbindung zum OPC-UA Server hergestellt.")

            # Nodes für SPS anlegen
            self.start_node = self.client.get_node("ns=7;s=::AsGlobalPV:di_start_opc")
            self.status_node = self.client.get_node("ns=6;s=::Program:SM_PRODUCING_MACHINE")

        except Exception as e:
            print(f"Fehler beim Verbinden: {e}")

    def start(self, instance):
        # Starte die OPC UA Kommunikation
        self.start_node.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
        print("Start-Kommando gesendet.")

        # Statusaktualisierung starten
        Clock.schedule_interval(self.update_status, 1)

    def update_status(self, dt):
        # Aktuellen Status abrufen und anzeigen
        status = self.status_node.get_value()
        status_description = receive_Datas(status)
        self.status_label.text = f'Status: {status_description}'


class MyApp(App):
    def build(self):
        return OPCUAGUI()

    def on_stop(self):
        # Verbindung trennen, wenn die App geschlossen wird
        if hasattr(self.root, 'client'):
            self.root.client.disconnect()
            print("Verbindung zum OPC-UA Server getrennt.")


if __name__ == '__main__':
    MyApp().run()
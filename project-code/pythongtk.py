import gi
gi.require_version("Gtk", "3.0")
from gi.repository import GLib, Gtk, GdkPixbuf, Gdk
from opcua import Client, ua

class ImageSwitcherGTK(Gtk.Window):
    def __init__(self):
        super().__init__(title="Visualisierung Automatisierungsanlage")

        # Standardgröße des Fensters auf 480x272 setzen
        self.set_default_size(480, 272)

        # Variable, um den Vollbildstatus zu verfolgen
        self.is_fullscreen = False

        # Layout erstellen
        vbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=10)
        self.add(vbox)

        # Image-Widget
        self.image = Gtk.Image()
        vbox.pack_start(self.image, True, True, 0)

        # Umschalt-Button hinzufügen
        self.start_button = Gtk.Button(label="Start")
        self.start_button.connect("clicked", self.on_start_button_clicked)
        vbox.pack_start(self.start_button, False, False, 0)

        # OPC UA Client initialisieren
        self.client = Client("opc.tcp://192.168.0.100:4840")
        self.connect_to_opcua()

        # Bildpfade basierend auf dem Status
        self.image_paths = [self.receive_datas(i) for i in range(7)]
        self.current_image_index = 0  # Aktueller Index des Bildes

        # Bild sofort beim Start laden
        self.load_image()

        # Bild alle 500 ms aktualisieren
        Gdk.threads_add_idle(GLib.PRIORITY_DEFAULT_IDLE, self.update_image)

        # Tastatur-Ereignis hinzufügen, um F11 zu überwachen
        self.connect("key-press-event", self.on_key_press)

    def connect_to_opcua(self):
        try:
            self.client.connect()
            self.start_node = self.client.get_node("ns=7;s=::AsGlobalPV:di_start_opc")
            self.status_node = self.client.get_node("ns=6;s=::Program:SM_PRODUCING_MACHINE")
        except Exception as e:
            print(f"Fehler bei der Verbindung zum OPC UA Server: {e}")

    def receive_datas(self, status):
        match status:
            case 0:
                return "../Bilder/INIT.png"
            case 1:
                return "../Bilder/PRESS_OUT.png"
            case 2:
                return "../Bilder/STAMP.png"
            case 3:
                return "../Bilder/CHECK.png"
            case 4:
                return "../Bilder/STOP.png"
            case 5:
                return "../Bilder/OUTSOURCE.png"
            case 6:
                return "../Bilder/FREE.png"

    def load_image(self):
        # Bild laden
        image_path = self.image_paths[self.current_image_index]  # Aktuelles Bild verwenden
        try:
            # Ursprüngliches Bild laden
            pixbuf = GdkPixbuf.Pixbuf.new_from_file(image_path)

            # Skalierung auf eine Breite von 330 Pixeln
            new_width = 300
            new_height = int((new_width / pixbuf.get_width()) * pixbuf.get_height())

            # Bild skalieren
            scaled_pixbuf = pixbuf.scale_simple(new_width, new_height, GdkPixbuf.InterpType.BILINEAR)
            self.image.set_from_pixbuf(scaled_pixbuf)
        except Exception as e:
            print(f"Fehler beim Laden des Bildes: {e}")

    def on_start_button_clicked(self, widget):
        # Start-Logik ausführen (z.B. OPC UA Node setzen)
        self.start_node.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))

    def update_image(self):
        # Status abrufen und Bild aktualisieren
        status = self.status_node.get_value()
        self.current_image_index = status
        self.load_image()  # Bild neu laden

        return True  # True zurückgeben, um die Idle-Funktion aufrechtzuerhalten

    def on_key_press(self, widget, event):
        # Umschalten des Vollbildmodus bei Drücken von F11
        if event.keyval == Gdk.KEY_F11:
            if self.is_fullscreen:
                self.unfullscreen()  # Vollbildmodus verlassen
            else:
                self.fullscreen()  # In den Vollbildmodus wechseln
            self.is_fullscreen = not self.is_fullscreen

    def on_destroy(self, widget):
        # Verbindung trennen und Anwendung beenden
        self.client.disconnect()
        Gtk.main_quit()

# GTK-Anwendung starten
if __name__ == "__main__":
    win = ImageSwitcherGTK()
    win.connect("destroy", win.on_destroy)
    win.show_all()
    Gtk.main()


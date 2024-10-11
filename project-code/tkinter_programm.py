from opcua import Client, ua
import customtkinter as ctk
from tkinter import filedialog
from PIL import Image, ImageTk


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

# def stop():
#     print(start_node.get_value())

def update_image():
    status = status_node.get_value()
    datapath = receive_Datas(status)

    image = Image.open(datapath)
    photo = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor=ctk.NW, image=photo)
    canvas.image = photo  # Referenz speichern, um das Bild anzuzeigen

    root.after(500, update_image)  # Bild alle 1 Sekunde aktualisieren



if __name__ == "__main__":
     # OPCUA Server erstellen
    url = "opc.tcp://192.168.0.100:4840" 
    client = Client(url)

    try: 
        #GUI Einstelleungen vornehmen
        ctk.set_appearance_mode("System")  # Modes: "System" (standard), "Dark", "Light"
        ctk.set_default_color_theme("blue")  # Themes: "blue" (standard), "green", "dark-blue"

        # Ein Fenster erzeugen
        root = ctk.CTk()
        root.title("Visualisierung Automatisierungsanlage")
        root.geometry("480x272")

        datapath = None

        # Mit SPS verbinden
        client.connect()

        # Nodes für SPS anlegen
        start_node = client.get_node("ns=7;s=::AsGlobalPV:di_start_opc")
        #var_type_start = start_node.get_data_type_as_variant_type()

        status_node = client.get_node("ns=6;s=::Program:SM_PRODUCING_MACHINE")
        status = status_node.get_value()

        # Objekt für ein Bild erzeugen auf die gegebene Groesse
        canvas = ctk.CTkCanvas(root, width=480, height=272)
        canvas.pack()

        # Buttons erzeuegen für die Start und Stop Logik
        start_button = ctk.CTkButton(root, text="Start", command=start, width=50, height=20)
        canvas.create_window(250, 280, window = start_button)

        # stop_button = ctk.CTkButton(root, text="Stopp",command=stop, width=50, height=20)
        # canvas.create_window(320, 280, window = stop_button)

        update_image()
        root.mainloop()


    finally:
       # Verbindung trennen
       client.disconnect()
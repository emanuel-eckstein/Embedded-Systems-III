from opcua import Client, ua
import time

# Funktion, die den aktuellen Status beschreibt
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

def start():
    start_node.set_value(ua.DataValue(ua.Variant(True, ua.VariantType.Boolean)))
    print("Start-Kommando gesendet.")

def print_status():
    while True:
        status = status_node.get_value()
        status_description = receive_Datas(status)
        print(f"Aktueller Status: {status_description}")
        
        time.sleep(1)  # Warte 1 Sekunde, bevor der Status erneut abgerufen wird


if __name__ == "__main__":
    # OPC UA Client verbinden
    url = "opc.tcp://192.168.0.100:4840"  # URL des OPC-UA Servers
    client = Client(url)

    try:
        # Verbindung herstellen
        client.connect()
        print("Verbindung zum OPC-UA Server hergestellt.")

        # Nodes für SPS anlegen
        start_node = client.get_node("ns=7;s=::AsGlobalPV:di_start_opc")
        status_node = client.get_node("ns=6;s=::Program:SM_PRODUCING_MACHINE")

        # Status regelmäßig ausgeben
        print_status()

    finally:
        # Verbindung trennen
        client.disconnect()
        print("Verbindung zum OPC-UA Server getrennt.")

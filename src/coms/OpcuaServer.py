from opcua import Server
import random
from time import sleep

if __name__ == "__main__":
        
    server = Server()
    server.set_endpoint("opc.tcp://127.0.0.1:12345")
    server.register_namespace("Room1")
    objects = server.get_objects_node()
    tempsense = objects.add_object('ns=2;s="TS1"',"Temperature Sensor 1")
    tempsense.add_variable('ns=2;s="TS1_VendorName"', "TS1 Vendor Name", "SensorKing")
    tempsense.add_variable('ns=2;s="TS1_SerialNumber"', "TS1 Serial Number", 12345678)
    temp = tempsense.add_variable('ns=2;s="TS1_Temperature"',"TS1 Temperature", 20)
    bulb = objects.add_object(2,"Light Bulb")
    state = bulb.add_variable(2,"State of Light Bulb",False)
    state.set_writable()
    server.export_xml_by_ns('MANF455-555_nodes.xml')

    try:
        print("starting server")
        server.start()
        print("server online")
        while True:
            temp.set_value(temp.get_value() + random.uniform(-1,1))
            print("New Temperature: " + str(temp.get_value()))
            print("State of Light Bulb: " + str(state.get_value()))
            sleep(2)
    finally:
        server.stop()
        print("server offline")

from opcua import Client

class SubHandler(object):
    def datachange_notification(self, node, val, data):
        print("New data change event at NodeID", node, ". New value = ", val)

if __name__ == "__main__":
    
    client = Client("opc.tcp://127.0.0.1:12345")

    try:
        client.connect()
        temp = client.get_node('ns=2;s="TS1_Temperature"')
        handler = SubHandler()
        sub = client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(temp)
        while True:
            pass

    finally:
        client.disconnect()

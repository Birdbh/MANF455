from opcua import Client

URL = "opc.tcp://127.0.0.1:12345"
NODE_ADDRESS_LIST = ['ns=2;s="TS1_Temperature"']

class SubHandler(object):
    def datachange_notification(self, node, val, data):
        print("New data change event at NodeID", node, ". New value = ", val)

class Client():

    def __init__(self):
        self.client = Client(URL)

        try:
            self.client.connect()
            self.get_nodes()
            while True:
                pass

        finally:
            self.client.disconnect()

    def get_nodes(self):
        self.node_array = []
        for node in NODE_ADDRESS_LIST:
            self.node_array.append(self.client.get_node(node))
            self.subscribe_node(node)

    def subscribe_node(self, node):
        handler = SubHandler()
        sub = self.client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(node)


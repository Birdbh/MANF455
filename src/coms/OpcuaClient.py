from opcua import Client
from ComsManager import ComsManager

URL = "opc.tcp://127.0.0.1:12345"
NODE_ADDRESS_DICT = {'ns=2;s="TS1_Temperature"':'Downtime'}

class SubHandler(object):
    def datachange_notification(self, node, val, data):
        com_type = NODE_ADDRESS_DICT[node]
        nodeId = node
        new_value = val
        ComsManager().direct_communication(com_type, nodeId, new_value)

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
        for node in NODE_ADDRESS_DICT.keys():
            self.node_array.append(self.client.get_node(node))
            self.subscribe_node(node)

    def subscribe_node(self, node):
        handler = SubHandler()
        sub = self.client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(node)


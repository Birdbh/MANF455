import time
import code

from opcua import Client
from ComsManager import ComsManager
#example
IP_ADDRESS ="opc.tcp://172.21.3.1:4840"
NS_NUMBER = 3

def embed():
    vars = globals()
    vars.update(locals())
    shell = code.InteractiveConsole(vars)
    shell.interact()

class NodeList:
    _instance = None
    _nodes = [] 
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    @classmethod
    def add_node(cls, node):
        cls._nodes.append(node)
    
    @classmethod
    def get_nodes(cls):
        return cls._nodes

class Node():
    def __init__(self, datablock, tag_name):
        self.ns_number = NS_NUMBER
        self.datablock = datablock
        self.tag_name = tag_name
        self.address = "ns=" + str(self.ns_number) + ";s=" + self.datablock + "." + self.tag_name + '"'
        self.past_value = None
        self.current_value = None
        self.rising_edge = False
        NodeList.add_node(self)

    def update_rising_edge(self):
        if self.past_value is True and self.current_value is False:
            self.rising_edge = True
        elif self.past_value is False and self.current_value is True:
            self.rising_edge = False
        else:
            self.rising_edge = False

class SubHandler(object):
    def datachange_notification(self, node, val, data):

        for potential_node in NodeList.get_nodes():
            if node == potential_node.address:
                potential_node.past_value = potential_node.current_value
                potential_node.current_value = val
                potential_node.update_rising_edge()

class Client():

    def __init__(self):
        self.client = Client(IP_ADDRESS)

        try:
            self.client.connect()
            for node in NodeList.get_nodes():
                self.subscribe_node(node)

            time.sleep(0.1)
            embed()

        finally:
            self.client.disconnect()

    def subscribe_nodes(self, node):
        node_address = node.address
        handler = SubHandler()
        sub = self.client.create_subscription(500, handler)
        handle = sub.subscribe_data_change(node_address)

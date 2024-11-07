from coms.OpcuaClient import PLC_COM
from coms.OpcuaClient import NodeList
from coms.OpcuaClient import Node
from data.Order import OrderTable
import threading

import time
class ComsManager():
    def __init__(self):
        self.presenceNode = Node("abstractMachine", "pres_blk")
        self.TaskCode = Node("abstractMachine", "task_code")
        self.orderId = Node("identData", "writeData")
        self.order_table = OrderTable()

        self.nodes = NodeList()
        self.plc = PLC_COM()

        self.thread = threading.Thread(target=self.loop, daemon=True)
        self.thread.start()

    def loop(self):
        while True:
            if self.presenceNode.rising_edge and not self.queueEmpty():
                self.presenceNode.rising_edge = False
                print("got here")
                task_code, orderId = self.firstItemInQueueTaskCode()
                self.TaskCode.write(task_code)
                data_to_write = self.RFIDArrayToWrite(task_code, orderId)
                self.orderId.write(data_to_write)
            
            elif self.presenceNode.rising_edge and self.queueEmpty():
                self.presenceNode.rising_edge = False
                self.TaskCode.write(-1)

            time.sleep(0.2)

    def queueEmpty(self):
        #select all items from the order database where the status is Pending and the start time is less tahn the current time but in this day
        results = self.order_table.get_all_proccesing_orders_from_today_before_the_current_time()
        if results:
            return False
        return True
    
    def firstItemInQueueTaskCode(self):
        #select all items from the order database where the status is Pending and the start time is less tahn the current time but in this day
        results = self.order_table.get_all_proccesing_orders_from_today_before_the_current_time()
        if results:
            orderId = results[0].orderId
            task_code = results[0].drilling_operation
            #set the order as completed
            self.order_table.set_status_completed(orderId)
            return task_code, orderId
        return None
    
    def RFIDArrayToWrite(self, task_code, orderID):
        #the first number in data_to_write shoudl be the task_code, the remaining ones should be the orderID, one digit of the number in each entry of the array
        #the length of the array should be 32 with the unused spots filled with 0
        data_to_write = []
        data_to_write.append(int(task_code))
        for digit in str(orderID):
            data_to_write.append(int(digit))
        while len(data_to_write) < 32:
            data_to_write.append(0)
        return data_to_write

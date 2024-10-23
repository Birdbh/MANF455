#TODO: Create a class that will handle the queue of the orders being sent to the drilling machine.
# This class should have the following methods:
# - add_order: This method should add a new order to the queue.
# - get_next_order: This method should return the next order in the queue.
# - remove_order: This method should remove the next order in the queue.
# - get_queue: This method should return the entire queue.
# - clear_queue: This method should remove all the orders in the queue.
# The class should have the following attributes:
# - queue: This attribute should be a list that will store the orders in the queue.
# The class should have the following constructor:
# - __init__: This method should initialize the queue attribute as an empty list.
# The class should have the following properties:
# - next_order: This property should return the next order in the queue.
# - queue_length: This property should return the length of the queue.
# The class should have the following methods:

import datetime

class Queue():
    def __init__(self):
        self.queue = []
        self.queue_length = 0

    def add_order(self, order):
        self.queue.append(order)
        self.queue_length += 1

    def get_next_order(self):
        return self.queue[0] if self.queue else None
    
    def remove_order(self):
        if self.queue:
            self.queue.pop(0)
            self.queue_length -= 1

    def get_queue(self):
        return self.queue
    
    def scan_orders_database_for_orders_to_begin_now(self, order_table):
        pass
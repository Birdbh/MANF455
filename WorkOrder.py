class WorkOrder:
    def __init__(self, order_id, customer_id, drilling_location, start_time):
        self.order_id = order_id
        self.customer_id = customer_id
        self.drilling_location = drilling_location
        self.start_time = start_time
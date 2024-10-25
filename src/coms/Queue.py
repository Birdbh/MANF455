import threading
import time
import datetime
from typing import Optional
from sqlalchemy import and_

class OrderQueue(threading.Thread):
    def __init__(self, order_table, node_list):
        """
        Initialize the OrderQueue thread
        
        Args:
            order_table: Instance of OrderTable for database operations
            node_list: Instance of NodeList for checking processing status
        """
        super().__init__()
        self.order_table = order_table
        self.node_list = node_list
        self.daemon = True  # Thread will exit when main program exits
        self._stop_event = threading.Event()
        self.processing_node = next(
            (node for node in node_list.get_nodes() if node.tag_name == "CurrentProcessing"),
            None
        )

    def stop(self):
        """Signal the thread to stop"""
        self._stop_event.set()

    def process_order(self, order) -> None:
        """
        Process an order when its start time is reached
        
        Args:
            order: Order object to be processed
        """
        # Mark the order as in progress
        session = self.order_table.Session()
        try:
            order.status = "In Progress"
            session.commit()
            
            # Call your processing function here
            self.start_manufacturing_process(order)
            
        finally:
            session.close()

    def start_manufacturing_process(self, order) -> None:
        """
        Start the manufacturing process for an order
        
        Args:
            order: Order object to be manufactured
        """
        # Implement your manufacturing process logic here
        # This could involve sending signals to your OPC UA client
        # or triggering other manufacturing systems
        pass

    def run(self):
        """Main thread loop for monitoring and processing orders"""
        while not self._stop_event.is_set():
            current_time = datetime.datetime.now()
            
            # Get all unprocessed orders
            session = self.order_table.Session()
            try:
                unprocessed_orders = session.query(Order).filter(
                    and_(
                        Order.status != "Completed",
                        Order.order_date <= current_time
                    )
                ).all()

                for order in unprocessed_orders:
                    if order.status == "Pending":
                        if order.order_date <= current_time:
                            # Check if system is currently processing
                            if self.processing_node and self.processing_node.current_value:
                                # System is busy, push start time forward
                                order.order_date = current_time + datetime.timedelta(minutes=1)
                                session.commit()
                            else:
                                # System is available, process the order
                                self.process_order(order)
                
                session.commit()
            
            except Exception as e:
                print(f"Error in OrderQueue: {e}")
                session.rollback()
            finally:
                session.close()

            # Sleep for a short interval before next check
            time.sleep(1)

def create_order_queue(order_table, node_list) -> OrderQueue:
    """
    Create and start an OrderQueue instance
    
    Args:
        order_table: Instance of OrderTable
        node_list: Instance of NodeList
    
    Returns:
        OrderQueue: Running OrderQueue thread instance
    """
    queue = OrderQueue(order_table, node_list)
    queue.start()
    return queue
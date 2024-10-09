
class Customer:
    def __init__(self, customer_id, name, address, email):
        self.customer_id = customer_id
        self.name = name
        self.address = address
        self.email = email

    def __str__(self):
        return f"{self.customer_id}: {self.name}, {self.address}, {self.email}"
    
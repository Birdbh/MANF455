from data import MESDatabase

    db = MESDatabase("mes.db")

    # Adding an operator
    db.operators.insert({
        'name': 'John Doe',
        'role': 'Technician',
        'username': 'john.doe',
        'password': 'hashed_password_here'
    })

#     # Adding a customer
#     db.customers.insert({
#         'name': 'Acme Corp',
#         'email': 'contact@acmecorp.com',
#         'address': '123 Main St, City, Country'
#     })

#     # Adding an order
#     db.orders.insert({
#         'customer_id': 1,
#         'operator_id': 1,
#         'order_date': '2024-10-08',
#         'status': 'Pending'
#     })

#     # Querying data
#     operators = db.operators.select({'role': 'Technician'})
#     print("Technicians:", operators)

#     customers = db.customers.select({'name': 'Acme Corp'})
#     print("Acme Corp customer:", customers)

#     orders = db.orders.select({'status': 'Pending'})
#     print("Pending orders:", orders)

#     # Updating data
#     db.orders.update({'status': 'In Progress'}, {'id': 1})

#     # Deleting data
#     db.customers.delete({'id': 1})
from flask import Flask, jsonify, request
from flask_cors import CORS
try:
    from database_java import db
    print("Using Java Oracle connector for database access")
except ImportError:
    try:
        from database import db
        print("Using real Oracle database connection")
    except ImportError:
        from database_mock import db
        print("Using mock database (Oracle client not available)")
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
CORS(app)

# Customer endpoints
@app.route('/api/customers', methods=['GET'])
def get_customers():
    try:
        rows = db.execute_select('SELECT * FROM Customer ORDER BY customer_id')
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['POST'])
def create_customer():
    try:
        data = request.get_json()
        # Get the last customer_id
        result = db.execute_select('SELECT MAX(customer_id) AS max_id FROM Customer')
        last_id = result[0]['MAX_ID'] if result and result[0]['MAX_ID'] is not None else 0
        new_id = last_id + 1
        db.execute_query(
            'INSERT INTO Customer (customer_id, first_name, last_name, phone_number, email, address) VALUES (:1, :2, :3, :4, :5, :6)',
            [new_id, data['first_name'], data['last_name'], data['phone_number'], data['email'], data['address']]
        )
        return jsonify({'message': 'Customer created successfully', 'customer_id': new_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    try:
        data = request.get_json()
        db.execute_query(
            'UPDATE Customer SET first_name = :1, last_name = :2, phone_number = :3, email = :4, address = :5 WHERE customer_id = :6',
            [data['first_name'], data['last_name'], data['phone_number'], data['email'], data['address'], customer_id]
        )
        return jsonify({'message': 'Customer updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['DELETE'])
def delete_customer(customer_id):
    try:
        db.execute_query('DELETE FROM Customer WHERE customer_id = :1', [customer_id])
        return jsonify({'message': 'Customer deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Laundry Service endpoints
@app.route('/api/laundry-services', methods=['GET'])
def get_laundry_services():
    try:
        rows = db.execute_select('SELECT * FROM Laundry_Service ORDER BY service_id')
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/laundry-services', methods=['POST'])
def create_laundry_service():
    try:
        data = request.get_json()
        result = db.execute_select('SELECT MAX(service_id) AS max_id FROM Laundry_Service')
        last_id = result[0]['MAX_ID'] if result and result[0]['MAX_ID'] is not None else 0
        new_id = last_id + 1
        db.execute_query(
            'INSERT INTO Laundry_Service (service_id, service_name, description, price) VALUES (:1, :2, :3, :4)',
            [new_id, data['service_name'], data['description'], data['price']]
        )
        return jsonify({'message': 'Laundry service created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/laundry-services/<int:service_id>', methods=['PUT'])
def update_laundry_service(service_id):
    try:
        data = request.get_json()
        db.execute_query(
            'UPDATE Laundry_Service SET service_name = :1, description = :2, price = :3 WHERE service_id = :4',
            [data['service_name'], data['description'], data['price'], service_id]
        )
        return jsonify({'message': 'Laundry service updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/laundry-services/<int:service_id>', methods=['DELETE'])
def delete_laundry_service(service_id):
    try:
        db.execute_query('DELETE FROM Laundry_Service WHERE service_id = :1', [service_id])
        return jsonify({'message': 'Laundry service deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Employee endpoints
@app.route('/api/employees', methods=['GET'])
def get_employees():
    try:
        rows = db.execute_select('SELECT * FROM Employee ORDER BY employee_id')
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees', methods=['POST'])
def create_employee():
    try:
        data = request.get_json()
        result = db.execute_select('SELECT MAX(employee_id) AS max_id FROM Employee')
        last_id = result[0]['MAX_ID'] if result and result[0]['MAX_ID'] is not None else 0
        new_id = last_id + 1
        db.execute_query(
            'INSERT INTO Employee (employee_id, first_name, last_name, job_title, hire_date, salary) VALUES (:1, :2, :3, :4, :5, :6)',
            [new_id, data['first_name'], data['last_name'], data['job_title'], data['hire_date'], data['salary']]
        )
        return jsonify({'message': 'Employee created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['PUT'])
def update_employee(employee_id):
    try:
        data = request.get_json()
        db.execute_query(
            'UPDATE Employee SET first_name = :1, last_name = :2, job_title = :3, hire_date = :4, salary = :5 WHERE employee_id = :6',
            [data['first_name'], data['last_name'], data['job_title'], data['hire_date'], data['salary'], employee_id]
        )
        return jsonify({'message': 'Employee updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees/<int:employee_id>', methods=['DELETE'])
def delete_employee(employee_id):
    try:
        db.execute_query('DELETE FROM Employee WHERE employee_id = :1', [employee_id])
        return jsonify({'message': 'Employee deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Membership Card endpoints
@app.route('/api/membership-cards', methods=['GET'])
def get_membership_cards():
    try:
        rows = db.execute_select('SELECT * FROM Membership_Card ORDER BY card_id')
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/membership-cards', methods=['POST'])
def create_membership_card():
    try:
        data = request.get_json()
        result = db.execute_select('SELECT MAX(card_id) AS max_id FROM Membership_Card')
        last_id = result[0]['MAX_ID'] if result and result[0]['MAX_ID'] is not None else 0
        new_id = last_id + 1
        db.execute_query(
            'INSERT INTO Membership_Card (card_id, card_type, discount_percentage, valid_until) VALUES (:1, :2, :3, :4)',
            [new_id, data['card_type'], data['discount_percentage'], data['valid_until']]
        )
        return jsonify({'message': 'Membership card created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/membership-cards/<int:card_id>', methods=['PUT'])
def update_membership_card(card_id):
    try:
        data = request.get_json()
        db.execute_query(
            'UPDATE Membership_Card SET card_type = :1, discount_percentage = :2, valid_until = :3 WHERE card_id = :4',
            [data['card_type'], data['discount_percentage'], data['valid_until'], card_id]
        )
        return jsonify({'message': 'Membership card updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/membership-cards/<int:card_id>', methods=['DELETE'])
def delete_membership_card(card_id):
    try:
        db.execute_query('DELETE FROM Membership_Card WHERE card_id = :1', [card_id])
        return jsonify({'message': 'Membership card deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer Membership endpoints
@app.route('/api/customer-memberships', methods=['GET'])
def get_customer_memberships():
    try:
        query = "SELECT cm.customer_id, cm.card_id, cm.join_date, c.first_name, c.last_name, mc.card_type, mc.discount_percentage FROM Customer_Membership cm JOIN Customer c ON cm.customer_id = c.customer_id JOIN Membership_Card mc ON cm.card_id = mc.card_id ORDER BY cm.join_date DESC"
        rows = db.execute_select(query)
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customer-memberships', methods=['POST'])
def create_customer_membership():
    try:
        data = request.get_json()
        db.execute_query(
            'INSERT INTO Customer_Membership (customer_id, card_id, join_date) VALUES (:1, :2, :3)',
            [data['customer_id'], data['card_id'], data['join_date']]
        )
        return jsonify({'message': 'Customer membership created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customer-memberships/<int:customer_id>/<int:card_id>', methods=['DELETE'])
def delete_customer_membership(customer_id, card_id):
    try:
        db.execute_query('DELETE FROM Customer_Membership WHERE customer_id = :1 AND card_id = :2', [customer_id, card_id])
        return jsonify({'message': 'Customer membership deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Utilities Bill endpoints
@app.route('/api/utility-bills', methods=['GET'])
def get_utility_bills():
    try:
        rows = db.execute_select('SELECT * FROM Utilities_Bill ORDER BY due_date DESC')
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/utility-bills', methods=['POST'])
def create_utility_bill():
    try:
        data = request.get_json()
        result = db.execute_select('SELECT MAX(bill_id) AS max_id FROM Utilities_Bill')
        last_id = result[0]['MAX_ID'] if result and result[0]['MAX_ID'] is not None else 0
        new_id = last_id + 1
        db.execute_query(
            'INSERT INTO Utilities_Bill (bill_id, bill_type, amount, due_date, payment_status) VALUES (:1, :2, :3, :4, :5)',
            [new_id, data['bill_type'], data['amount'], data['due_date'], data.get('payment_status', 'Unpaid')]
        )
        return jsonify({'message': 'Utility bill created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/utility-bills/<int:bill_id>', methods=['PUT'])
def update_utility_bill(bill_id):
    try:
        data = request.get_json()
        db.execute_query(
            'UPDATE Utilities_Bill SET bill_type = :1, amount = :2, due_date = :3, payment_status = :4 WHERE bill_id = :5',
            [data['bill_type'], data['amount'], data['due_date'], data['payment_status'], bill_id]
        )
        return jsonify({'message': 'Utility bill updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/utility-bills/<int:bill_id>', methods=['DELETE'])
def delete_utility_bill(bill_id):
    try:
        db.execute_query('DELETE FROM Utilities_Bill WHERE bill_id = :1', [bill_id])
        return jsonify({'message': 'Utility bill deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Customer Utilities endpoints
@app.route('/api/customer-utilities', methods=['GET'])
def get_customer_utilities():
    try:
        query = "SELECT cu.customer_id, cu.bill_id, c.first_name, c.last_name, ub.bill_type, ub.amount, ub.due_date, ub.payment_status FROM Customer_Utilities cu JOIN Customer c ON cu.customer_id = c.customer_id JOIN Utilities_Bill ub ON cu.bill_id = ub.bill_id ORDER BY ub.due_date DESC"
        rows = db.execute_select(query)
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customer-utilities', methods=['POST'])
def create_customer_utility():
    try:
        data = request.get_json()
        db.execute_query(
            'INSERT INTO Customer_Utilities (customer_id, bill_id) VALUES (:1, :2)',
            [data['customer_id'], data['bill_id']]
        )
        return jsonify({'message': 'Customer utility assignment created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customer-utilities/<int:customer_id>/<int:bill_id>', methods=['DELETE'])
def delete_customer_utility(customer_id, bill_id):
    try:
        db.execute_query('DELETE FROM Customer_Utilities WHERE customer_id = :1 AND bill_id = :2', [customer_id, bill_id])
        return jsonify({'message': 'Customer utility assignment deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Owner endpoints
@app.route('/api/owners', methods=['GET'])
def get_owners():
    try:
        rows = db.execute_select('SELECT * FROM Owner ORDER BY owner_id')
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/owners', methods=['POST'])
def create_owner():
    try:
        data = request.get_json()
        result = db.execute_select('SELECT MAX(owner_id) AS max_id FROM Owner')
        last_id = result[0]['MAX_ID'] if result and result[0]['MAX_ID'] is not None else 0
        new_id = last_id + 1
        db.execute_query(
            'INSERT INTO Owner (owner_id, first_name, last_name, phone_number, email) VALUES (:1, :2, :3, :4, :5)',
            [new_id, data['first_name'], data['last_name'], data['phone_number'], data['email']]
        )
        return jsonify({'message': 'Owner created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/owners/<int:owner_id>', methods=['PUT'])
def update_owner(owner_id):
    try:
        data = request.get_json()
        db.execute_query(
            'UPDATE Owner SET first_name = :1, last_name = :2, phone_number = :3, email = :4 WHERE owner_id = :5',
            [data['first_name'], data['last_name'], data['phone_number'], data['email'], owner_id]
        )
        return jsonify({'message': 'Owner updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/owners/<int:owner_id>', methods=['DELETE'])
def delete_owner(owner_id):
    try:
        db.execute_query('DELETE FROM Owner WHERE owner_id = :1', [owner_id])
        return jsonify({'message': 'Owner deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Owner Laundry Service endpoints
@app.route('/api/owner-laundry-services', methods=['GET'])
def get_owner_laundry_services():
    try:
        query = "SELECT ols.owner_id, ols.service_id, o.first_name, o.last_name, ls.service_name, ls.description, ls.price FROM Owner_Laundry_Service ols JOIN Owner o ON ols.owner_id = o.owner_id JOIN Laundry_Service ls ON ols.service_id = ls.service_id ORDER BY o.last_name, o.first_name"
        rows = db.execute_select(query)
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/owner-laundry-services', methods=['POST'])
def create_owner_laundry_service():
    try:
        data = request.get_json()
        db.execute_query(
            'INSERT INTO Owner_Laundry_Service (owner_id, service_id) VALUES (:1, :2)',
            [data['owner_id'], data['service_id']]
        )
        return jsonify({'message': 'Owner laundry service assignment created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/owner-laundry-services/<int:owner_id>/<int:service_id>', methods=['DELETE'])
def delete_owner_laundry_service(owner_id, service_id):
    try:
        db.execute_query('DELETE FROM Owner_Laundry_Service WHERE owner_id = :1 AND service_id = :2', [owner_id, service_id])
        return jsonify({'message': 'Owner laundry service assignment deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Home Service endpoints
@app.route('/api/home-services', methods=['GET'])
def get_home_services():
    try:
        query = "SELECT hs.home_service_id, hs.customer_id, hs.service_date, hs.service_type, hs.cost, c.first_name, c.last_name FROM Home_Service hs JOIN Customer c ON hs.customer_id = c.customer_id ORDER BY hs.service_date DESC"
        rows = db.execute_select(query)
        return jsonify(rows)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/home-services', methods=['POST'])
def create_home_service():
    try:
        data = request.get_json()
        result = db.execute_select('SELECT MAX(home_service_id) AS max_id FROM Home_Service')
        last_id = result[0]['MAX_ID'] if result and result[0]['MAX_ID'] is not None else 0
        new_id = last_id + 1
        db.execute_query(
            'INSERT INTO Home_Service (home_service_id, customer_id, service_date, service_type, cost) VALUES (:1, :2, :3, :4, :5)',
            [new_id, data['customer_id'], data['service_date'], data['service_type'], data['cost']]
        )
        return jsonify({'message': 'Home service created successfully'}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/home-services/<int:home_service_id>', methods=['PUT'])
def update_home_service(home_service_id):
    try:
        data = request.get_json()
        db.execute_query(
            'UPDATE Home_Service SET customer_id = :1, service_date = :2, service_type = :3, cost = :4 WHERE home_service_id = :5',
            [data['customer_id'], data['service_date'], data['service_type'], data['cost'], home_service_id]
        )
        return jsonify({'message': 'Home service updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/home-services/<int:home_service_id>', methods=['DELETE'])
def delete_home_service(home_service_id):
    try:
        db.execute_query('DELETE FROM Home_Service WHERE home_service_id = :1', [home_service_id])
        return jsonify({'message': 'Home service deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

# Dashboard stats endpoint
@app.route('/api/dashboard/stats', methods=['GET'])
def get_dashboard_stats():
    try:
        queries = {
            'totalCustomers': 'SELECT COUNT(*) as count FROM Customer',
            'totalServices': 'SELECT COUNT(*) as count FROM Laundry_Service',
            'totalEmployees': 'SELECT COUNT(*) as count FROM Employee',
            'totalOwners': 'SELECT COUNT(*) as count FROM Owner',
            'pendingBills': "SELECT COUNT(*) as count FROM Utilities_Bill WHERE payment_status = 'Unpaid'",
            'totalBillAmount': "SELECT NVL(SUM(amount), 0) as total FROM Utilities_Bill WHERE payment_status = 'Unpaid'",
            'totalHomeServices': 'SELECT COUNT(*) as count FROM Home_Service',
            'activeMemberships': 'SELECT COUNT(*) as count FROM Customer_Membership cm JOIN Membership_Card mc ON cm.card_id = mc.card_id WHERE mc.valid_until > SYSDATE'
        }

        stats = {}
        for key, query in queries.items():
            try:
                result = db.execute_select(query)
                if result and len(result) > 0:
                    stats[key] = result[0].get('TOTAL', result[0].get('COUNT', 0))
                else:
                    stats[key] = 0
            except Exception as e:
                print(f"Error in {key}: {e}")
                stats[key] = 0

        return jsonify(stats)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({'status': 'OK', 'database': 'Oracle', 'version': 'Python Flask', 'schema': 'Database.txt'})

if __name__ == '__main__':
    port = int(os.getenv('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
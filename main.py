import pyrebase
from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import verify_jwt_in_request, create_access_token, JWTManager, jwt_required, get_jwt_identity
import secrets
import time

########################################################################################################################################################################
#                                                                       DATABASE CONFIGURATION                                                                         #
########################################################################################################################################################################


firebaseConfig = {
  "apiKey": "AIzaSyBCVtFN52QTQ8MaChScu9ImN3aNk79VVTU",
  "authDomain": "web-hw3-667b0.firebaseapp.com",
  "projectId": "web-hw3-667b0",
  "storageBucket": "web-hw3-667b0.appspot.com",
  "messagingSenderId": "1044509657789",
  "appId": "1:1044509657789:web:a33e5159cf9c6dec7f45d4",
  "databaseURL": "https://web-hw3-667b0-default-rtdb.europe-west1.firebasedatabase.app",
}

firebase = pyrebase.initialize_app(firebaseConfig)
db = firebase.database()
app = Flask(__name__)
secret_key = secrets.token_urlsafe(32)
app.config["JWT_SECRET_KEY"] = secret_key
jwt = JWTManager(app)
CORS(app)

########################################################################################################################################################################
#                                                                       ADMIN ROUTES                                                                                   #
########################################################################################################################################################################

@app.route('/admin/register', methods=['POST'])
def admin_register():
    name = ""
    surname = ""
    email = ""
    phone = ""
    password = ""
    
    try:
        data = request.get_json()
        name = data['name']
        surname = data['surname']
        email = data['email']
        phone = data['phone']
        password = data['password']
        
        if name == "" or surname == "" or email == "" or phone == "" or password == "":
            return jsonify({"message": "Please fill all the fields"}), 400
        
        admins = db.child("admins").get()
        for admin in admins.each():
            if admin.val()['email'] == email:
                return jsonify({"message": "Admin with this email already exists"}), 400
        
        if len(password) < 6:
            return jsonify({"message": "Password must contain at least 6 characters"}), 400
        
        if not any(char.isdigit() for char in password):
            return jsonify({"message": "Password must contain at least one number"}), 400
        
        if not any(char.isupper() for char in password):
            return jsonify({"message": "Password must contain at least one uppercase letter"}), 400 
        
        db.child("admins").push({
            "name": name,
            "surname": surname,
            "email": email,
            "phone": phone,
            "password": password
        })
        
        return jsonify({"message": "Admin registered successfully"}), 201  # Created
    except Exception as e:
        return f"An Error Occured: {e}"
    

@app.route('/admin/login', methods=['POST'])
def admin_login():
    email = ""
    password = ""
    
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']

        if email == "" or password == "":
            return jsonify({"message": "Please fill all the fields"}), 400
        
        admins = db.child("admins").get()
        for admin in admins.each():
            if admin.val()['email'] == email:
                if admin.val()['password'] == password:
                    access_token = create_access_token(identity= {"type": "admin", "id": admin.key()})
                    return jsonify({"access_token": access_token}), 200
    
                else:
                    return jsonify({"message": "Wrong password"}), 400
                
    except Exception as e:
        return f"Login failed: {e}"

@app.route('/admin/add-coffee', methods=['POST'])
@jwt_required()
def add_coffee():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "admin":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
    try:
        data = request.get_json()
        coffee_image = data["link"]
        coffee_name = data["name"]
        coffee_s_price = data["small_price"]
        coffee_m_price = data["medium_price"]
        coffee_l_price = data["large_price"]

        coffees = db.child("coffees").get()
        for coffee in coffees.each():
            if coffee.val()['name'] == coffee_name:
                return jsonify({"message": "Coffee with this name already exists"}), 400

                
        db.child("coffees").push({
            "link": coffee_image,
            "name": coffee_name,
            "small_price": coffee_s_price,
            "medium_price": coffee_m_price,
            "large_price": coffee_l_price,
        })
        
        return jsonify({"message": "Coffee added successfully"}), 201
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
@app.route('/admin/update-coffee', methods=['PUT'])
@jwt_required()
def update_coffee():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "admin":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
    try:
        data = request.get_json()
        coffee_image = data["link"]
        coffee_name = data["name"]
        coffee_s_price = data["small_price"]
        coffee_m_price = data["medium_price"]
        coffee_l_price = data["large_price"]
        coffee_id = data["id"]
        
        db.child("coffees").child(coffee_id).update({
           "link": coffee_image,
            "name": coffee_name,
            "small_price": coffee_s_price,
            "medium_price": coffee_m_price,
            "large_price": coffee_l_price,
        })
        
        return jsonify({"message": "Coffee updated successfully"}), 200
    
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/admin/delete-coffee', methods=['DELETE'])
@jwt_required()
def delete_coffee():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "admin":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
    try:
        data = request.get_json()
        coffee_id = data["id"]
        
        db.child("coffees").child(coffee_id).remove()
        
        return jsonify({"message": "Coffee deleted successfully"}), 200
    
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/admin/all-coffees', methods=['GET'])
@jwt_required()
def get_all_coffees_admin():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "admin":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"

    
    try:
        coffees = db.child("coffees").get()
        return jsonify(coffees.val()), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@app.route('/admin/all-orders', methods=['GET'])
@jwt_required()
def get_all_orders_admin():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "admin":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
    
    try:
        orders = db.child("orders").get()
        
        if len(orders.val()) == 0:
            return jsonify({"message": "No orders found"}), 400
        
        return jsonify({"message": "Orders found successfully", "orders": orders.val(), "count": len(orders.val())}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
@app.route('/admin/last-10-orders', methods=['GET'])
@jwt_required()
def get_last_10_orders_admin():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "admin":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
    try:
        orders = db.child("orders").get()
        last_10_orders = {}
        
        if len(orders.val()) == 0:
            return jsonify({"message": "No orders found"}), 400
        
        count = 0
        for order in reversed(orders.each()):
            if count == 10:
                break
            last_10_orders[order.key()] = order.val()
            count += 1
        return jsonify({"message": "Last 10 orders found successfully", "last_10_orders": last_10_orders}), 200
    
        
    except Exception as e:
        return f"An Error Occured: {e}"

########################################################################################################################################################################
#                                                                       CUSTOMER ROUTES                                                                                #
########################################################################################################################################################################


@app.route('/customer/register', methods=['POST'])
def customer_register():
    name = ""
    surname = ""
    email = ""
    phone = ""
    password = ""
    
    try:
        data = request.get_json()
        name = data['name']
        surname = data['surname']
        email = data['email']
        phone = data['phone']
        password = data['password']
        
        if name == "" or surname == "" or email == "" or phone == "" or password == "":
            return jsonify({"message": "Please fill all the fields"}), 400
        
        customers = db.child("customers").get()
        for customer in customers.each():
            if customer.val()['email'] == email:
                return jsonify({"message": "User with this email already exists"}), 400
    
        
        if len(password) < 6:
            return jsonify({"message": "Password must contain at least 6 characters"}), 400
        
        if not any(char.isdigit() for char in password):
            return jsonify({"message": "Password must contain at least one number"}), 400
        
        if not any(char.isupper() for char in password):
            return jsonify({"message": "Password must contain at least one uppercase letter"}), 400
        
        
        db.child("customers").push({
            "name": name,
            "surname": surname,
            "email": email,
            "phone": phone,
            "password": password
        })
        
        return jsonify({"message": "Customer registered successfully"}), 201  
    except Exception as e:
        return f"An Error Occured: {e}"
    
@app.route('/customer/login', methods=['POST'])
def customer_login():
    email = ""
    password = ""
    
    try:
        data = request.get_json()
        email = data['email']
        password = data['password']
        
        if email == "" or password == "":
            return jsonify({"message": "Please fill all the fields"}), 400
        
        customers = db.child("customers").get()
        for customer in customers.each():
            if customer.val()['email'] == email:
                if customer.val()['password'] == password:
                    access_token = create_access_token(identity= {"type": "customer", "id": customer.key()})
                    return {"access_token": access_token, "customer_id": customer.key()}, 200
    
                else:
                    return jsonify({"message": "Wrong password"}), 400
                
        return jsonify({"message": "User with this email does not exist"}), 400
    
    except Exception as e:
        return f"An Error Occured: {e}"
    

    
@app.route('/customer/all-coffees', methods=['GET'])
@jwt_required()
def get_all_coffees_customer():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "customer":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"

    try:
        coffees = db.child("coffees").get()
        return jsonify(coffees.val()), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/customer/cal-price', methods=['POST'])
@jwt_required()
def call_price():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "customer":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
    try:
        data = request.get_json()
        coffee_list = data["coffee_list"]
        price_dict = {}

        coffees = db.child("coffees").get()
        for coffee in coffee_list:
            valid_coffee_name = False
            for c in coffees.each():
                if coffee["coffee_name"] == c.val()["name"]:
                    valid_coffee_name = True

                    if coffee["coffee_size"] == "Small":
                        price_dict[coffee["key"]] = {
                            "coffee_name": coffee["coffee_name"],
                            "price": int(c.val()["small_price"]) * int(coffee["coffee_quantity"]),
                            "quantity": coffee["coffee_quantity"]
                        }
                        
                    elif coffee["coffee_size"] == "Medium":
                        price_dict[coffee["key"]] = {
                            "coffee_name": coffee["coffee_name"],
                            "price": int(c.val()["medium_price"]) * int(coffee["coffee_quantity"]),
                            "quantity": coffee["coffee_quantity"]
                        }
                    elif coffee["coffee_size"] == "Large":
                        price_dict[coffee["key"]] = {
                            "coffee_name": coffee["coffee_name"],
                            "price": int(c.val()["large_price"]) * int(coffee["coffee_quantity"]),
                            "quantity": coffee["coffee_quantity"]
                            
                        }
                    else:
                        return jsonify({"message": "Invalid coffee size"}), 400

                    break

        if not valid_coffee_name:
            return jsonify({"message": "Invalid coffee name"}), 400

        return jsonify({"message": "Price calculated successfully", "price": price_dict}), 200
        
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
@app.route('/customer/give-order', methods=['POST'])
@jwt_required()
def give_order():
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "customer":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
    try:
        data = request.get_json()
        customer_id = data["customer_id"]
        coffee_list = data["coffee_list"]
        price = data["total_price"]
        delivery_time = data["delivery_time"]
        order_time = time.strftime("%d/%m/%Y %H:%M:%S")
        
        db.child("orders").push({
            "customer_id": customer_id,
            "coffee_list": coffee_list,
            "price": price,
            "delivery_time": delivery_time,
            "order_time": order_time
        })
        
        orders = db.child("orders").get()
        order_id = ""
        for order in orders.each():
            if order.val()["order_time"] == order_time and order.val()["customer_id"] == customer_id:
                order_id = order.key()
                break
            
        return jsonify({"message": "Order given successfully", "order_id": order_id}), 201
       
       
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/customer/<string:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    
    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "customer":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    
    
    try:
        customer = db.child("customers").child(customer_id).get()
        return jsonify(customer.val()), 200
    except Exception as e:
        return f"An Error Occured: {e}"

@app.route('/customer/order-history/<string:customer_id>', methods=['GET'])
@jwt_required()
def get_order_history(customer_id):

    try:
        jwt_identity = get_jwt_identity()
        user_type = jwt_identity['type']
        
        if user_type != "customer":
            return jsonify({"message": "Invalid token"}), 400
        
    
    except Exception as e:
        return f"An Error Occured: {e}"
    try:
        orders = db.child("orders").get()
        order_history = {}
        count = 0
        for order in orders.each():
            if order.val()["customer_id"] == customer_id:
                order_history[order.key()] = order.val()
                count += 1
        if count == 0:
            return jsonify({"message": "No orders found"}), 400
        return jsonify({"message": "Order history found successfully", "order_history": order_history}), 200
    except Exception as e:
        return f"An Error Occured: {e}"
    
if __name__ == '__main__':
    app.run(debug=True)



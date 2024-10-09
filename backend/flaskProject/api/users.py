from io import BytesIO

from flask import Blueprint, current_app, make_response, abort, send_file

from flask import request, jsonify, Response
import jwt
import bcrypt
import datetime
from utils import get_db_connection, token_required

# Define the blueprint for users
users_blueprint = Blueprint('users', __name__)
# Apply CORS to the blueprint

@users_blueprint.route('/get', methods=['GET'])
@token_required
def get_users():
    # Example API to return a list of users
    return jsonify({'users': ['Alice', 'Bob', 'Charlie']})


#Login API for both user and Serviceman
@users_blueprint.route('/auth', methods=['POST'])
def auth():

    username = request.json.get("username")
    password = request.json.get("password")
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT pass_hash, role, user_id, full_name, pin_code, approval FROM Users WHERE username = ?', (username,))
    result = cursor.fetchone()


    conn.close()
    if result and bcrypt.checkpw(password.encode('utf-8'), result['pass_hash'].encode('utf-8')):
        token = jwt.encode({
            'user_id': result['user_id'],
            'username': username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=90)
        }, current_app.config['SECRET_KEY'])
        print(result['approval'])
        return jsonify({
            "Success": True,
            "message": "Login Successful",
            "token": token,
            "role": result['role'],
            "user_id": result['user_id'],
            "full_name": result['full_name'],
            "pin_code": result['pin_code'],
            "approval": result['approval']
        }), 200
    return jsonify({"Success": False,"message":"Something Went Wrong!"}), 401

#Registration API for both user and Serviceman

@users_blueprint.route('/register', methods=['POST'])
def register():
    action = request.form.get("action")  # For form data
    base_url = request.host_url

    username = request.form.get("username")
    password = request.form.get("password")
    mail = request.form.get("mail")
    mobile = request.form.get("mobile")
    full_name = request.form.get("full_name")
    address = request.form.get("address")
    pin_code = request.form.get("pin_code")
    date_created = datetime.datetime.utcnow().date()

    if action == "service_reg":
        service = request.form.get("subservice")
        exp = request.form.get("experience")
        experience = int(exp) if exp else None
        # Handle file upload
        portfolio_file = request.files.get('portfolio')
        portfolio = portfolio_file.read() if portfolio_file else None

    pass_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_db_connection()
    cursor = conn.cursor()

    cursor.execute('SELECT COUNT(*) FROM Users WHERE username = ?', (username,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return Response('Username already exists! Try another username.', mimetype='text/plain'), 409

    cursor.execute('SELECT COUNT(*) FROM Users WHERE mail = ?', (mail,))
    if cursor.fetchone()[0] > 0:
        conn.close()
        return Response('Email already exists! Try another email.', mimetype='text/plain'), 409

    if action == "cust_reg":
        cursor.execute('INSERT INTO Users (username, pass_hash, role, mail, mobile, full_name, address, pin_code, date_created) VALUES (?,?,?,?,?,?,?,?,?)',
                       (username, pass_hash, "customer", mail, mobile, full_name, address, pin_code, date_created))

    elif action == "service_reg":
        cursor.execute('INSERT INTO Users (username, pass_hash, role, mail, mobile, full_name, address, pin_code, date_created, service, experience, portfolio) VALUES (?,?,?,?,?,?,?,?,?,?,?,?)',
                       (username, pass_hash, "serviceman", mail, mobile, full_name, address, pin_code, date_created, service, experience, portfolio))
    else:
        return Response('An Error has Occurred!.', mimetype='text/plain'), 500
    conn.commit()
    conn.close()
    return Response('Registration successful!', mimetype='text/plain'), 200


# Route to get all servicemen and their relevant data
@users_blueprint.route('/getServicemen', methods=['GET'])
@token_required
def get_servicemen():
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to select relevant fields from Users table where role is 'serviceman'
        query = """
        SELECT user_id, full_name, service, Rating, experience, pin_code, approval, date_created 
        FROM Users 
        WHERE role = 'serviceman'
        """

        cursor.execute(query)
        servicemen = cursor.fetchall()
        cursor.close()
        conn.close()
        # If no servicemen found, return a 404 response
        if not servicemen:
            return jsonify({"message": "No servicemen found"}), 404

        # Format the result into a list of dictionaries
        result = []
        for serviceman in servicemen:
            result.append({
                "user_id": serviceman[0],
                "full_name": serviceman[1],
                "service": serviceman[2],
                "Rating": serviceman[3],
                "experience": serviceman[4],
                "pin_code": serviceman[5],
                "approval": serviceman[6],
                "date_created": serviceman[7]
            })

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_blueprint.route('/getCustomers', methods=['GET'])
@token_required
def get_customers():
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to select relevant fields from Users table where role is 'serviceman'
        query = """
        SELECT user_id, full_name, mail, mobile, pin_code, approval, username, date_created
        FROM Users 
        WHERE role = 'customer'
        """

        cursor.execute(query)
        servicemen = cursor.fetchall()
        cursor.close()
        conn.close()
        # If no servicemen found, return a 404 response
        if not servicemen:
            return jsonify({"message": "No customer found"}), 404

        # Format the result into a list of dictionaries
        result = []
        for serviceman in servicemen:
            result.append({
                "user_id": serviceman[0],
                "full_name": serviceman[1],
                "mail": serviceman[2],
                "mobile": serviceman[3],
                "pin_code": serviceman[4],
                "approval": serviceman[5],
                "username": serviceman[6],
                "date_created": serviceman[7]
            })

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500



@users_blueprint.route('/update_profile', methods=['PUT'])
@token_required
def update_profile():
    data = request.form
    data_token = request.token_data
    user_id = data_token['user_id']
    role = data_token['role']

    conn = get_db_connection()
    cursor = conn.cursor()

    updates = {}

    # Common fields for both customer and serviceman
    common_fields = ['password', 'mail', 'mobile', 'full_name', 'address', 'pin_code']
    for field in common_fields:
        if field in data:
            if field == 'password':
                hashed = bcrypt.hashpw(data[field].encode('utf-8'), bcrypt.gensalt())
                updates['pass_hash'] = hashed.decode('utf-8')
            else:
                updates[field] = data[field]

    # Additional fields for serviceman
    if role == 'serviceman':
        if 'experience' in data:
            updates['experience'] = data['experience']
        if 'portfolio' in request.files:
            portfolio_file = request.files['portfolio']
            updates['portfolio'] = portfolio_file.read()
        if 'subservice' in data:
            updates['service'] = data['subservice']
    # Construct the SQL query
    update_fields = ', '.join([f"{k} = ?" for k in updates.keys()])
    query = f"UPDATE Users SET {update_fields} WHERE user_id = ?"

    try:
        cursor.execute(query, list(updates.values()) + [user_id])
        conn.commit()
        return jsonify({"message": "Profile updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        conn.close()


@users_blueprint.route('/getpdf/<int:serviceman_id>', methods=['GET'])
#@token_required
def get_pdf(serviceman_id):
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT portfolio FROM Users WHERE user_id = ?", (serviceman_id,))
        result = cursor.fetchone()

        if not result or result[0] is None:
            abort(404, description="PDF not found")

        pdf_blob = result[0]

        # Create a BytesIO object from the blob
        pdf_file = BytesIO(pdf_blob)

        # Use send_file to return the PDF
        return send_file(
            pdf_file,
            mimetype='application/pdf',
            as_attachment=True,
            download_name=f'serviceman_{serviceman_id}.pdf'
        )

    except Exception as e:
        print(f"Error retrieving PDF: {str(e)}")
        abort(500, description="Internal server error")

    finally:
        if conn:
            conn.close()


@users_blueprint.route('/update_approval/<int:user_id>', methods=['PUT'])
@token_required
def update_approval(user_id):
    data_token = request.token_data
    data = request.json
    role = data_token['role']

    #Authenticating
    if role == 'admin':
        conn = get_db_connection()
        cursor = conn.cursor()

        if data.get('approval') == 'true':
            cursor.execute(f"UPDATE Users SET approval = true WHERE user_id = {user_id}")

        elif data.get('approval') == 'false':
            cursor.execute(f"UPDATE Users SET approval = false WHERE user_id = {user_id}")

        else:
            return Response('Invalid approval status was sent!.', mimetype='text/plain'), 500

        conn.commit()
        conn.close()
        return Response("Approval updated successfully", mimetype='text/plain'), 200
    else:
        return Response("You are not Authorized!", mimetype='text/plain'), 401


#individual customer and serviceman
@users_blueprint.route('/getServiceman/<int:serviceman_id>', methods=['GET','OPTIONS'])
@token_required
def get_serviceman(serviceman_id):
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        the_id = serviceman_id
        # Query to select relevant fields from Users table where role is 'serviceman'
        query = """
        SELECT user_id, full_name, address, service, experience, pin_code, date_created, mail, mobile
        FROM Users 
        WHERE user_id = ?
        """

        cursor.execute(query, (the_id,))
        servicemen = cursor.fetchall()
        cursor.close()
        conn.close()
        # If no servicemen found, return a 404 response
        if not servicemen:
            return jsonify({"message": "No servicemen found"}), 404

        # Format the result into a list of dictionaries
        result = []
        for serviceman in servicemen:
            result.append({
                "user_id": serviceman[0],
                "full_name": serviceman[1],
                "address": serviceman[2],
                "service": serviceman[3],
                "experience": serviceman[4],
                "pin_code": serviceman[5],
                "date_created": serviceman[6],
                "mail": serviceman[7],
                "mobile": serviceman[8]
            })

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@users_blueprint.route('/getCustomer/<int:customer_id>', methods=['GET','OPTIONS'])
@token_required
def get_customer(customer_id):
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()
        # Query to select relevant fields from Users table where role is 'serviceman'
        query = """
        SELECT full_name, mail, mobile, pin_code, address
        FROM Users 
        WHERE user_id = ?
        """

        cursor.execute(query, (customer_id,))
        servicemen = cursor.fetchone()
        cursor.close()
        conn.close()
        # If no servicemen found, return a 404 response
        if not servicemen:
            return jsonify({"message": "No customer found"}), 404
        print(servicemen[4])
        # Format the result into a list of dictionaries
        result = []
        result.append({
            "full_name": servicemen[0],
            "mail": servicemen[1],
            "mobile": servicemen[2],
            "pin_code": servicemen[3],
            "address": servicemen[4]
            })

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
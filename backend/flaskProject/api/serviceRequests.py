import datetime
from flask import Blueprint, jsonify, Response, request
from utils import get_db_connection, token_required


# Define the blueprint for requests
requests_blueprint = Blueprint('requests', __name__)


# Define the route to get services for a specific serviceman
@requests_blueprint.route('/listServices/<int:serviceman_id>', methods=['GET'])
@token_required
def get_services(serviceman_id):
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get all relevant fields from ServiceRequests for the given serviceman_id
        query = """
        SELECT serviceRequest_id, customer_id, serviceman_id, status, service, 
               customer_name, customer_address, rating, request_begin_date, request_end_date
        FROM ServiceRequests
        WHERE serviceman_id = ?
        """

        # Execute the query with the provided serviceman_id
        cursor.execute(query, (serviceman_id,))
        service_requests = cursor.fetchall()
        cursor.close()
        conn.close()
        # If no service requests found, return a 404 response
        if not service_requests:
            return jsonify({"message": "No service requests found for this serviceman"}), 404

        # Format the result into a list of dictionaries
        result = []
        for request in service_requests:
            result.append({
                "serviceRequest_id": request[0],
                "customer_id": request[1],
                "serviceman_id": request[2],
                "status": request[3],
                "service": request[4],
                "customer_name": request[5],
                "customer_address": request[6],
                "rating": request[7],
                "request_begin_date": request[8],
                "request_end_date": request[9]
            })

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@requests_blueprint.route('/listMyServices/<int:customer_id>', methods=['GET'])
@token_required
def get_MyServices(customer_id):
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get all relevant fields from ServiceRequests for the given customer_id
        query = """
        SELECT serviceRequest_id, customer_id, serviceman_id, serviceman_name, status, service, rating, request_begin_date, request_end_date
        FROM ServiceRequests
        WHERE customer_id = ?
        """

        # Execute the query with the provided serviceman_id
        cursor.execute(query, (customer_id,))
        service_requests = cursor.fetchall()
        cursor.close()
        conn.close()
        # If no service requests found, return a 404 response
        if not service_requests:
            return jsonify({"message": "No service requests found from this customer"}), 404

        # Format the result into a list of dictionaries
        result = []
        for request in service_requests:
            result.append({
                "serviceRequest_id": request[0],
                "customer_id": request[1],
                "serviceman_id": request[2],
                "serviceman_name": request[3],
                "status": request[4],
                "service": request[5],
                "rating": request[6],
                "request_begin_date": request[7],
                "request_end_date": request[8]
            })

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@requests_blueprint.route('/addServiceRequest', methods=['POST'])
@token_required
def add_service_request():
    try:
        # Get the data from the request body (assuming JSON format)
        data = request.get_json()

        # Extract the fields from the data
        customer_id = data.get('customer_id')
        serviceman_id = data.get('serviceman_id')
        serviceman_name = data.get('serviceman_Fullname')
        status = data.get('status')
        service = data.get('service')
        customer_name = data.get('cust_Fullname')
        customer_address = data.get('pin_code')
        subservice_id = data.get('subservice_id')  # Extract SubService_id from the request
        date = datetime.datetime.utcnow().date()

        print(customer_address)

        # Check if all required fields are provided
        if not all([customer_id, serviceman_id, status, service, customer_name, customer_address, subservice_id]):
            return jsonify({"message": "All fields are required"}), 400

        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Check if the service request already exists for the given serviceman and customer
        cursor.execute("""
         SELECT COUNT(*)
         FROM ServiceRequests
         WHERE serviceman_id = ? AND customer_id = ? AND (status = ? OR status = ?)
         """, (serviceman_id, customer_id, "requested", "active"))

        # If a service request is already active or requested, return an error
        if cursor.fetchone()[0] > 0:
            conn.close()
            return jsonify({"message": "Service request already exists"}), 400

        # Insert the new service request into the ServiceRequests table with SubService_id
        query = """
        INSERT INTO ServiceRequests (customer_id, serviceman_id, serviceman_name, status, service, customer_name, customer_address, SubService_id, request_begin_date)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # Execute the query with the provided data, including SubService_id
        cursor.execute(query, (customer_id, serviceman_id, serviceman_name, status, service, customer_name, customer_address, subservice_id, date))

        # Commit the transaction
        conn.commit()

        # Close the connection
        cursor.close()
        conn.close()

        # Return a success response
        return jsonify({"message": "Service request added successfully"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@requests_blueprint.route('/editRequest', methods=['PUT', 'OPTIONS'])
@token_required
def edit_service_request():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    try:
        data = request.token_data
        serviceRequest_id = request.json.get('serviceRequest_id')
        status = request.json.get('status')
        date = datetime.datetime.utcnow().date()
        if data['role'] == "customer" and (status == "completed" or status == "withdrawn"):
            conn = get_db_connection()
            cursor = conn.cursor()
            if status == "completed":
                rating = request.json.get('rating')
                cursor.execute("""
                    UPDATE ServiceRequests
                    SET status = ?, rating = ?, request_end_date = ?
                    WHERE serviceRequest_id = ?
                    """,(status, rating, date, serviceRequest_id))
                conn.commit()
                conn.close()
                return Response("Service updated successfully -- Service Completed"), 200
            if status == "withdrawn":
                cursor.execute("""UPDATE ServiceRequests
                SET status = ?, request_end_date = ?
                Where serviceRequest_id = ?
                """,(status, date,  serviceRequest_id))
                conn.commit()
                conn.close()
                return Response("Service updated successfully -- Service Withdrawn"), 200

        elif data['role'] == "serviceman" and (status == "rejected" or status == "active"):
            conn = get_db_connection()
            cursor = conn.cursor()
            query1 = """UPDATE ServiceRequests
                            SET status = ?, request_end_date = ?
                            Where serviceRequest_id = ?
                            """
            query2 = """UPDATE ServiceRequests
                            SET status = ?
                            Where serviceRequest_id = ?
                            """

            if status == "rejected":
                cursor.execute(query1, (status, date, serviceRequest_id))
                conn.commit()
                conn.close()
                return Response("Service updated successfully -- Service Rejected"), 200
            elif status == "active":
                cursor.execute(query2, (status, serviceRequest_id))
                conn.commit()
                conn.close()
                return Response("Service updated successfully -- Service Active"), 200
        else:
            return jsonify({"message": "Invalid role or status submitted"}), 400

    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500


@requests_blueprint.route('/listAllServices', methods=['get'])
@token_required
def get_Allservices():
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get all relevant fields from ServiceRequests for the given serviceman_id
        query = """
        SELECT serviceRequest_id, customer_id, serviceman_id, status, service, 
               customer_name, customer_address, rating, serviceman_name, request_begin_date, request_end_date
        FROM ServiceRequests
        """

        # Execute the query with the provided serviceman_id
        cursor.execute(query)
        service_requests = cursor.fetchall()
        cursor.close()
        conn.close()
        # If no service requests found, return a 404 response
        # Format the result into a list of dictionaries
        result = []
        for request in service_requests:
            result.append({
                "serviceRequest_id": request[0],
                "customer_id": request[1],
                "serviceman_id": request[2],
                "status": request[3],
                "service": request[4],
                "customer_name": request[5],
                "customer_address": request[6],
                "rating": request[7],
                "serviceman_name": request[8],
                "request_begin_date": request[9],
                "request_end_date": request[10]
            })

        # Return the result as JSON
        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@requests_blueprint.route('/averageRating/<int:serviceman_id>', methods=['get'])
@token_required
def get_average_rating(serviceman_id):
    try:
        # Establish database connection
        conn = get_db_connection()
        cursor = conn.cursor()

        # Query to get the average rating for completed services of the specified serviceman_id
        query = """
        SELECT AVG(rating) as average_rating
        FROM ServiceRequests
        WHERE serviceman_id = ? AND status = 'completed'
        """

        # Execute the query with the provided serviceman_id
        cursor.execute(query, (serviceman_id,))
        result = cursor.fetchone()
        cursor.close()
        conn.close()

        # Check if the result is None or if there's no rating data available
        average_rating = result[0] if result and result[0] is not None else "No ratings available"

        # Return the average rating as JSON
        return jsonify({"serviceman_id": serviceman_id, "average_rating": average_rating}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

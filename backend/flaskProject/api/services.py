import datetime
from flask import Blueprint, jsonify, Response, request
from utils import get_db_connection, token_required
# Define the blueprint for services
services_blueprint = Blueprint('services', __name__)

@services_blueprint.route('/listServices', methods=['GET'])
def get_services():
    # Connect to the database
    conn = get_db_connection()
    cursor = conn.cursor()

    # Query to retrieve the services along with their subservices
    cursor.execute('''  
        SELECT s.Service_Actual_id, s.service_name, s.service_desc, s.servicemen_count, s.date_created,
               ss.SubService_id, ss.SubService_Name, ss.base_rate
        FROM Services s
        LEFT JOIN SubServices ss ON s.Service_Actual_id = ss.Service_Actual_id
    ''')

    # Fetch all results
    services_data = cursor.fetchall()

    # Close the database connection
    conn.close()

    # Structure the results into a dictionary where each service contains its subservices
    result = {}
    for row in services_data:
        service_id = row[0]
        service = {
            'service_name': row[1],
            'service_desc': row[2],
            'servicemen': row[3],
            'date_created': row[4]
        }

        subservice = {
            'subservice_id': row[5],
            'subservice_name': row[6],
            'base_rate': row[7]
        }

        if service_id not in result:
            result[service_id] = {
                'service_info': service,
                'subservices': []
            }

        # Add subservice info only if it exists (subservice_id might be None if no subservices)
        if subservice['subservice_id'] is not None:
            result[service_id]['subservices'].append(subservice)

    # Convert the result dictionary into a list for JSON response
    final_result = []
    for service_id, data in result.items():
        final_result.append({
            'service_id': service_id,
            'service_info': data['service_info'],
            'subservices': data['subservices']
        })

    # Return the results as JSON
    return jsonify(final_result), 200


@services_blueprint.route('/createService', methods=['POST'])
@token_required
def create_service():
    action = request.json.get("action")
    data = request.token_data
    if data['role'] == "admin":
        if action == "createService":
            service_name = request.json.get("service_name")
            service_desc = request.json.get("service_description")
            date_created = datetime.datetime.utcnow().date()
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM Services WHERE service_name = ?', (service_name,))
            if cursor.fetchone()[0] > 0:
                conn.close()
                return Response('Service Already Exists!', mimetype='text/plain'), 409

            cursor.execute(
                'INSERT INTO Services (service_name, service_desc, date_created) VALUES (?,?,?)',
                (service_name, service_desc, date_created))
            conn.commit()
            conn.close()
            return Response("Service Created!", 201)

        elif action == "deleteService":
            service_name = request.json.get("service_name")

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM Services WHERE service_name = ?', (service_name,))
            conn.commit()
            conn.close()

            return Response("Service Deleted!", 201)
        else:
            return Response("An error occurred", 500)
    else:
        return Response("You are not allowed to edit Services", 403)


@services_blueprint.route('/SubService', methods=['POST', 'OPTIONS'])
@token_required
def create_subservice():
    if request.method == 'OPTIONS':
        return jsonify({}), 200
    action = request.json.get("action")
    data = request.token_data
    if data['role'] == "admin":
        if action == "createService":
            sub_name = request.json.get("sub_name")
            service_actual_id = request.json.get("service_actual_id")
            rate = request.json.get("base_rate")
            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('SELECT COUNT(*) FROM SubServices WHERE SubService_Name = ?', (sub_name,))

            if cursor.fetchone()[0] > 0:

                conn.close()
                return Response('Service Already Exists!', mimetype='text/plain'), 409

            cursor.execute(
                'INSERT INTO SubServices (Service_Actual_id, SubService_Name, base_rate) VALUES (?,?,?)',
                (service_actual_id, sub_name, rate))
            conn.commit()
            conn.close()
            return Response("Service Created!", 201)

        elif action == "deleteService":
            sub_name = request.json.get("sub_name")

            conn = get_db_connection()
            cursor = conn.cursor()

            cursor.execute('DELETE FROM SubServices WHERE SubService_Name = ?', (sub_name,))
            conn.commit()
            conn.close()

            return Response("Sub-Service Deleted!", 201)
        else:
            return Response("An error occurred", 500)
    else:
        return Response("You are not allowed to edit Sub Services", 403)


@services_blueprint.route('/EditService', methods=['PUT'])
@token_required
def edit_service():
    try:
        conn = get_db_connection()
        cursor = conn.cursor()
        action = request.json.get("action")

        if action == "service":
            service_actual_id = request.json.get("service_actual_id")
            service_name = request.json.get("service_name")
            service_desc = request.json.get("service_description")
            cursor.execute("""
                                UPDATE Services
                                SET service_name = ?, service_desc = ?
                                WHERE Service_Actual_id = ?
                                """,(service_name, service_desc, service_actual_id))

            conn.commit()
            conn.close()
            return Response("Service Edited!", 201)
        if action == "subservice":
            subservice_id = request.json.get("subservice_id")
            subservice_name = request.json.get("subservice_name")
            subservice_previous_name = request.json.get("subservice_previous_name")
            base_rate = request.json.get("base_rate")
            cursor.execute("""
                                  UPDATE SubServices
                                  SET SubService_Name = ?, base_rate = ?
                                  WHERE SubService_id = ?
                                  """, (subservice_name, base_rate, subservice_id))
            cursor.execute("""
                                  UPDATE ServiceRequests
                                  SET service = ?
                                  WHERE SubService_id = ?
                                  """, (subservice_name, subservice_id))
            cursor.execute("""
                                  UPDATE Users
                                  SET service = ?
                                  WHERE service = ?
                                  """, (subservice_name, subservice_previous_name))

            conn.commit()
            conn.close()
            return Response("Sub-Service Edited!", 201)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 500
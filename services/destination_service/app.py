# services/destination_service/app.py
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.destination_service.destinations import DestinationManager
from services.auth_service.auth import authenticate_token, is_admin

app = Flask(__name__)

destination_manager = DestinationManager()

SWAGGER_URL = '/docs'
API_URL = '/static/swagger.yaml'
swaggerui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={'app_name': "Destination Service"}
)
app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

@app.route('/destinations', methods=['GET'])
@authenticate_token
def get_destinations(current_user):
    try:
        # Fix: Properly check admin status from the current_user object
        admin_status = bool(getattr(current_user, 'is_admin', False))
        destinations = destination_manager.get_all_destinations(is_admin=admin_status)
        return jsonify(destinations), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/destinations', methods=['POST'])
@authenticate_token
@is_admin
def add_destination(current_user):
    try:
        data = request.get_json()
        if not all(k in data for k in ('name', 'description', 'location')):
            return jsonify({'error': 'Missing required fields'}), 400
        
        destination_id = destination_manager.add_destination(
            data['name'],
            data['description'],
            data['location']
        )
        return jsonify({'message': 'Destination added successfully', 'id': destination_id}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/destinations/<destination_id>', methods=['DELETE'])
@authenticate_token
@is_admin
def delete_destination(current_user, destination_id):
    try:
        if destination_manager.delete_destination(destination_id):
            return jsonify({'message': 'Destination deleted successfully'}), 200
        return jsonify({'error': 'Destination not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(port=5001, debug=True)
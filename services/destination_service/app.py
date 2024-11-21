# services/destination_service/app.py
from flask import Flask, request, jsonify
from flask_swagger_ui import get_swaggerui_blueprint
import os
import sys

# Add parent directory to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.destination_service.destinations import DestinationManager
from services.auth_service.auth import authenticate_token, is_admin

app = Flask(__name__)

# Initialize Destination Manager
destination_manager = DestinationManager()

# Swagger Configuration
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
        destinations = destination_manager.get_all_destinations()
        return jsonify(destinations), 200
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
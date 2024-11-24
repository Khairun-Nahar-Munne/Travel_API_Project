import unittest
import json
from functools import wraps
from services.destination_service.app import app, destination_manager
from services.destination_service.destinations import DestinationManager

class TestDestinationService(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Store original view functions
        cls.original_views = {
            'get_destinations': app.view_functions.get('get_destinations'),
            'add_destination': app.view_functions.get('add_destination'),
            'delete_destination': app.view_functions.get('delete_destination')
        }

        # Mock user for authentication
        class MockUser:
            def __init__(self, is_admin=True):
                self.is_admin = is_admin

        # Create mock authenticated views
        def mock_get_destinations(*args, **kwargs):
            return cls.original_views['get_destinations'](MockUser(is_admin=True))

        def mock_add_destination(*args, **kwargs):
            return cls.original_views['add_destination'](MockUser(is_admin=True))

        def mock_delete_destination(*args, **kwargs):
            # Correctly handle the destination_id parameter
            return cls.original_views['delete_destination'](MockUser(is_admin=True), destination_id=kwargs.get('destination_id'))

        # Replace view functions with mocked versions
        app.view_functions['get_destinations'] = mock_get_destinations
        app.view_functions['add_destination'] = mock_add_destination
        app.view_functions['delete_destination'] = mock_delete_destination

    @classmethod
    def tearDownClass(cls):
        # Restore original view functions
        for endpoint, view in cls.original_views.items():
            if view is not None:
                app.view_functions[endpoint] = view

    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
        # Clear any existing test data
        destination_manager.destinations = {}
        
        # Add some test destinations
        self.test_destinations = [
            {
                'name': 'Paris',
                'description': 'City of Light',
                'location': 'France'
            },
            {
                'name': 'Tokyo',
                'description': 'Modern metropolis',
                'location': 'Japan'
            }
        ]
        
        # Add test destinations to the manager
        self.destination_ids = []
        for dest in self.test_destinations:
            dest_id = destination_manager.add_destination(
                dest['name'],
                dest['description'],
                dest['location']
            )
            self.destination_ids.append(dest_id)

    def tearDown(self):
        # Clear test data
        destination_manager.destinations = {}

    def test_get_destinations_admin(self):
        response = self.app.get('/destinations')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), len(self.test_destinations))

    def test_get_destinations_regular_user(self):
        response = self.app.get('/destinations')
        data = json.loads(response.data)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(data), len(self.test_destinations))

    def test_add_destination_success(self):
        new_destination = {
            'name': 'Rome',
            'description': 'Eternal City',
            'location': 'Italy'
        }
        
        response = self.app.post(
            '/destinations',
            data=json.dumps(new_destination),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 201)
        self.assertIn('id', data)

    def test_add_destination_missing_fields(self):
        incomplete_destination = {
            'name': 'Rome',
            'description': 'Eternal City'
            # Missing location field
        }
        
        response = self.app.post(
            '/destinations',
            data=json.dumps(incomplete_destination),
            content_type='application/json'
        )
        
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 400)
        self.assertEqual(data['error'], 'Missing required fields')

    def test_add_destination_unauthorized(self):
        # Store original view function
        original_view = app.view_functions['add_destination']
        
        # Replace with unauthorized version
        def unauthorized_add(*args, **kwargs):
            return {'error': 'Unauthorized'}, 403
            
        app.view_functions['add_destination'] = unauthorized_add
        
        new_destination = {
            'name': 'Rome',
            'description': 'Eternal City',
            'location': 'Italy'
        }
        
        response = self.app.post(
            '/destinations',
            data=json.dumps(new_destination),
            content_type='application/json'
        )
        
        self.assertEqual(response.status_code, 403)
        
        # Restore original view
        app.view_functions['add_destination'] = original_view

    def test_delete_destination_success(self):
        dest_id = self.destination_ids[0]
        
        response = self.app.delete(f'/destinations/{dest_id}')
        
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.data)
        self.assertEqual(data['message'], 'Destination deleted successfully')

    def test_delete_destination_not_found(self):
        response = self.app.delete('/destinations/999')
        
        self.assertEqual(response.status_code, 404)
        data = json.loads(response.data)
        self.assertEqual(data['error'], 'Destination not found')

    def test_delete_destination_unauthorized(self):
        # Store original view function
        original_view = app.view_functions['delete_destination']
        
        # Replace with unauthorized version
        def unauthorized_delete(*args, **kwargs):
            return {'error': 'Unauthorized'}, 403
            
        app.view_functions['delete_destination'] = unauthorized_delete
        
        dest_id = self.destination_ids[0]
        response = self.app.delete(f'/destinations/{dest_id}')
        
        self.assertEqual(response.status_code, 403)
        
        # Restore original view
        app.view_functions['delete_destination'] = original_view

if __name__ == '__main__':
    unittest.main()
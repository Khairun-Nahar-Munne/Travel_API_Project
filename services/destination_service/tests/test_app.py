import unittest
from unittest.mock import Mock, patch
import json
from flask import Flask
from services.destination_service.app import app, destination_manager
from services.destination_service.destinations import DestinationManager

class TestDestinationService(unittest.TestCase):
    def setUp(self):
        self.app = app.test_client()
        self.app.testing = True
        
    @patch('services.destination_service.app.authenticate_token')
    def test_get_destinations_success(self, mock_authenticate):
        # Create a mock user and set authentication
        mock_user = Mock()
        mock_user.is_admin = False
        mock_authenticate.return_value = lambda f: lambda *args, **kwargs: f(mock_user, *args, **kwargs)
        
        # Mock destination manager's get_all_destinations method
        with patch.object(destination_manager, 'get_all_destinations', return_value=[
            {'id': '1', 'name': 'Test Destination', 'description': 'Test Description'}
        ]):
            # Send request
            response = self.app.get('/destinations')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        destinations = json.loads(response.data)
        self.assertEqual(len(destinations), 1)
        self.assertEqual(destinations[0]['name'], 'Test Destination')
    
    @patch('services.destination_service.app.authenticate_token')
    @patch('services.destination_service.app.is_admin')
    def test_add_destination_success(self, mock_is_admin, mock_authenticate):
        # Create mock user and set authentication
        mock_user = Mock()
        mock_authenticate.return_value = lambda f: lambda *args, **kwargs: f(mock_user, *args, **kwargs)
        mock_is_admin.return_value = lambda f: lambda *args, **kwargs: f(mock_user, *args, **kwargs)
        
        # Mock destination manager's add_destination method
        with patch.object(destination_manager, 'add_destination', return_value='123'):
            # Prepare test data
            destination_data = {
                'name': 'New Destination',
                'description': 'A wonderful place',
                'location': 'Test Location'
            }
            
            # Send request
            response = self.app.post('/destinations', 
                                     data=json.dumps(destination_data), 
                                     content_type='application/json')
        
        # Assertions
        self.assertEqual(response.status_code, 201)
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Destination added successfully')
        self.assertEqual(result['id'], '123')
    
    @patch('services.destination_service.app.authenticate_token')
    def test_add_destination_missing_fields(self, mock_authenticate):
        # Create mock user and set authentication
        mock_user = Mock()
        mock_authenticate.return_value = lambda f: lambda *args, **kwargs: f(mock_user, *args, **kwargs)
        
        # Prepare incomplete destination data
        destination_data = {
            'name': 'Incomplete Destination'
        }
        
        # Send request
        response = self.app.post('/destinations', 
                                 data=json.dumps(destination_data), 
                                 content_type='application/json')
        
        # Assertions
        self.assertEqual(response.status_code, 400)
        result = json.loads(response.data)
        self.assertEqual(result['error'], 'Missing required fields')
    
    @patch('services.destination_service.app.authenticate_token')
    @patch('services.destination_service.app.is_admin')
    def test_delete_destination_success(self, mock_is_admin, mock_authenticate):
        # Create mock user and set authentication
        mock_user = Mock()
        mock_authenticate.return_value = lambda f: lambda *args, **kwargs: f(mock_user, *args, **kwargs)
        mock_is_admin.return_value = lambda f: lambda *args, **kwargs: f(mock_user, *args, **kwargs)
        
        # Mock destination manager's delete_destination method
        with patch.object(destination_manager, 'delete_destination', return_value=True):
            # Send request
            response = self.app.delete('/destinations/123')
        
        # Assertions
        self.assertEqual(response.status_code, 200)
        result = json.loads(response.data)
        self.assertEqual(result['message'], 'Destination deleted successfully')
    
    @patch('services.destination_service.app.authenticate_token')
    @patch('services.destination_service.app.is_admin')
    def test_delete_destination_not_found(self, mock_is_admin, mock_authenticate):
        # Create mock user and set authentication
        mock_user = Mock()
        mock_authenticate.return_value = lambda f: lambda *args, **kwargs: f(mock_user, *args, **kwargs)
        mock_is_admin.return_value = lambda f: lambda *args, **kwargs: f(mock_user, *args, **kwargs)
        
        # Mock destination manager's delete_destination method
        with patch.object(destination_manager, 'delete_destination', return_value=False):
            # Send request
            response = self.app.delete('/destinations/999')
        
        # Assertions
        self.assertEqual(response.status_code, 404)
        result = json.loads(response.data)
        self.assertEqual(result['error'], 'Destination not found')

if __name__ == '__main__':
    unittest.main()
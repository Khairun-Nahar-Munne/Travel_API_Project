import uuid
import unittest
from unittest.mock import MagicMock
import os
import sys

sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from services.destination_service.destinations import DestinationManager

class TestDestinationManager(unittest.TestCase):
    
    def setUp(self):
        # Mocking the DestinationDatabase class
        self.mock_db = MagicMock()
        self.manager = DestinationManager()
        self.manager.db = self.mock_db  # Use the mocked db in place of the actual one

    def test_initialize_default_destinations(self):
        # Simulate an empty database (no destinations)
        self.mock_db.get_all_destinations.return_value = []
        
        # Call the private method _initialize_default_destinations indirectly
        self.manager._initialize_default_destinations()

        # Assert that add_destination was called twice for default destinations
        self.assertEqual(self.mock_db.add_destination.call_count, 2)

    def test_get_all_destinations(self):
        # Simulate returning a list of destinations from the database
        sample_destinations = [
            {'id': '123', 'name': 'Paris', 'description': 'City of Lights', 'location': 'France'},
            {'id': '456', 'name': 'Tokyo', 'description': 'Modern metropolis', 'location': 'Japan'}
        ]
        self.mock_db.get_all_destinations.return_value = sample_destinations
        
        # Call the method
        result = self.manager.get_all_destinations()

        # Assert that the returned result is the same as what was mocked
        self.assertEqual(result, sample_destinations)

    def test_delete_destination(self):
        # Set up for deleting a destination
        destination_id = '123'
        self.mock_db.delete_destination.return_value = True  # Mocking a successful delete

        # Call the delete method
        result = self.manager.delete_destination(destination_id)

        # Assert that delete_destination was called with the correct argument
        self.mock_db.delete_destination.assert_called_once_with(destination_id)

        # Assert the result is True (successful deletion)
        self.assertTrue(result)

    def test_add_destination(self):
        # Mock the UUID generation to return a fixed value for comparison
        fixed_uuid = 'a9d9bb37-1761-4462-94ab-65bae3705da3'
        new_destination = {
            'id': fixed_uuid,
            'name': 'New York',
            'description': 'The Big Apple',
            'location': 'USA'
        }

        # Mock add_destination method (it doesn't need to return anything)
        self.mock_db.add_destination.return_value = None

        # Mock uuid.uuid4() to return our fixed UUID
        with unittest.mock.patch('uuid.uuid4', return_value=uuid.UUID(fixed_uuid)):
            # Call the add_destination method
            destination_id = self.manager.add_destination(
                'New York', 'The Big Apple', 'USA'
            )

        # Assert that the add_destination method was called with the correct destination
        self.mock_db.add_destination.assert_called_once_with(new_destination)

        # Assert that the returned destination id matches the fixed UUID
        self.assertEqual(destination_id, fixed_uuid)


if __name__ == '__main__':
    unittest.main()

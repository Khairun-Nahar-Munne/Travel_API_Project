import unittest
import os
import shutil
import tempfile
from data.destinations import DestinationDatabase

class TestDestinationDatabase(unittest.TestCase):
    def setUp(self):
        """Create a temporary directory and database file before each test"""
        self.test_dir = tempfile.mkdtemp()
        self.test_db_file = os.path.join(self.test_dir, "test_destinations.py")
        self.db = DestinationDatabase(filename=self.test_db_file)
        
        # Sample destination data for testing
        self.sample_destination = {
            'id': 'dest123',
            'name': 'Paris',
            'country': 'France',
            'description': 'City of Light',
            'attractions': ['Eiffel Tower', 'Louvre']
        }

    def tearDown(self):
        """Clean up the temporary directory after each test"""
        shutil.rmtree(self.test_dir)

    def test_database_initialization(self):
        """Test if database file is created and initialized properly"""
        self.assertTrue(os.path.exists(self.test_db_file))
        with open(self.test_db_file, 'r') as f:
            content = f.read()
        self.assertEqual(content.strip(), "destinations = {}")

    def test_add_destination(self):
        """Test adding a destination to the database"""
        self.db.add_destination(self.sample_destination)
        
        # Verify destination was added
        loaded_destination = self.db.get_destination_by_id('dest123')
        self.assertEqual(loaded_destination, self.sample_destination)

    def test_delete_destination(self):
        """Test deleting a destination from the database"""
        # First add a destination
        self.db.add_destination(self.sample_destination)
        
        # Test successful deletion
        result = self.db.delete_destination('dest123')
        self.assertTrue(result)
        
        # Verify destination was deleted
        loaded_destination = self.db.get_destination_by_id('dest123')
        self.assertIsNone(loaded_destination)
        
        # Test deleting non-existent destination
        result = self.db.delete_destination('nonexistent')
        self.assertFalse(result)

    def test_get_destination_by_id(self):
        """Test retrieving a destination by ID"""
        # Test with non-existent destination
        result = self.db.get_destination_by_id('nonexistent')
        self.assertIsNone(result)
        
        # Add destination and test retrieval
        self.db.add_destination(self.sample_destination)
        result = self.db.get_destination_by_id('dest123')
        self.assertEqual(result, self.sample_destination)

    def test_get_all_destinations(self):
        """Test retrieving all destinations"""
        # Initially should be empty
        destinations = self.db.get_all_destinations()
        self.assertEqual(len(destinations), 0)
        
        # Add multiple destinations
        destination1 = self.sample_destination
        destination2 = {
            'id': 'dest456',
            'name': 'London',
            'country': 'UK',
            'description': 'British Capital',
            'attractions': ['Big Ben', 'Tower Bridge']
        }
        
        self.db.add_destination(destination1)
        self.db.add_destination(destination2)
        
        # Test retrieving all destinations
        destinations = self.db.get_all_destinations()
        self.assertEqual(len(destinations), 2)
        self.assertIn(destination1, destinations)
        self.assertIn(destination2, destinations)

    def test_update_existing_destination(self):
        """Test updating an existing destination"""
        # Add initial destination
        self.db.add_destination(self.sample_destination)
        
        # Update the destination
        updated_destination = self.sample_destination.copy()
        updated_destination['name'] = 'Updated Paris'
        updated_destination['description'] = 'Updated description'
        
        self.db.add_destination(updated_destination)
        
        # Verify the update
        loaded_destination = self.db.get_destination_by_id('dest123')
        self.assertEqual(loaded_destination['name'], 'Updated Paris')
        self.assertEqual(loaded_destination['description'], 'Updated description')

if __name__ == '__main__':
    unittest.main()
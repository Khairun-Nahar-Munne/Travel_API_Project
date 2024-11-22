import uuid
import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

from data.destinations import DestinationDatabase

class DestinationManager:
    def __init__(self):
        self.db = DestinationDatabase()
        self._initialize_default_destinations()

    def _initialize_default_destinations(self):
        if not self.db.get_all_destinations():
            default_destinations = [
                {
                    'id': str(uuid.uuid4()),
                    'name': 'Paris',
                    'description': 'City of Lights',
                    'location': 'France'
                },
                {
                    'id': str(uuid.uuid4()),
                    'name': 'Tokyo',
                    'description': 'Modern metropolis',
                    'location': 'Japan'
                }
            ]
            for dest in default_destinations:
                self.db.add_destination(dest)

    def get_all_destinations(self, is_admin=False):
        destinations = self.db.get_all_destinations()
        # If not admin, explicitly remove the ID field
        
        return destinations

    def delete_destination(self, destination_id):
        return self.db.delete_destination(destination_id)

    def add_destination(self, name, description, location):
        destination = {
            'id': str(uuid.uuid4()),
            'name': name,
            'description': description,
            'location': location
        }
        self.db.add_destination(destination)
        return destination['id']

# services/destination_service/destinations.py
import uuid

class DestinationManager:
    def __init__(self):
        # Using a dictionary to store destinations
        self.destinations = {
            str(uuid.uuid4()): {
                'name': 'Paris',
                'description': 'City of Lights',
                'location': 'France'
            },
            str(uuid.uuid4()): {
                'name': 'Tokyo',
                'description': 'Modern metropolis',
                'location': 'Japan'
            }
        }

    def get_all_destinations(self):
        return list(self.destinations.values())

    def delete_destination(self, destination_id):
        if destination_id in self.destinations:
            del self.destinations[destination_id]
            return True
        return False

    def add_destination(self, name, description, location):
        destination_id = str(uuid.uuid4())
        self.destinations[destination_id] = {
            'name': name,
            'description': description,
            'location': location
        }
        return destination_id
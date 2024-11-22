# data/destination_database.py
import os

class DestinationDatabase:
    def __init__(self, filename='destinations_data.py'):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self._initialize_database()

    def _initialize_database(self):
        if not os.path.exists(self.filename):
            with open(self.filename, 'w') as f:
                f.write("destinations = {}")

    def _load_destinations(self):
        with open(self.filename, 'r') as f:
            exec(f.read(), globals())
            return globals()['destinations']

    def _save_destinations(self, destinations):
        with open(self.filename, 'w') as f:
            f.write(f"destinations = {repr(destinations)}")

    def add_destination(self, destination):
        destinations = self._load_destinations()
        destinations[destination['id']] = destination
        self._save_destinations(destinations)

    def delete_destination(self, destination_id):
        destinations = self._load_destinations()
        if destination_id in destinations:
            del destinations[destination_id]
            self._save_destinations(destinations)
            return True
        return False

    def get_destination_by_id(self, destination_id):
        destinations = self._load_destinations()
        return destinations.get(destination_id)

    def get_all_destinations(self):
        return list(self._load_destinations().values())

import json
import os

class DBHandler:
    def __init__(self, filename="data.json"):
        # Explicitly get the absolute path where the script lives
        base_dir = os.path.dirname(os.path.abspath(__file__))
        self.filename = os.path.join(base_dir, filename)
        self.ensure_file_exists()

    def ensure_file_exists(self):
        if not os.path.exists(self.filename) or os.path.getsize(self.filename) == 0:
            default_data = {
                "movies": [
                    {"movie_id": 1, "title": "Avengers Endgame", "genre": "Action", "price": 250, "rows": 5, "cols": 6},
                    {"movie_id": 2, "title": "Mirzapur", "genre": "Crime", "price": 200, "rows": 5, "cols": 6},
                    {"movie_id": 3, "title": "The Love Hypothesis", "genre": "Romance", "price": 180, "rows": 5, "cols": 6},
                    {"movie_id": 4, "title": "3 Idiots", "genre": "Comedy/Drama", "price": 220, "rows": 5, "cols": 6},
                    {"movie_id": 5, "title": "Interstellar", "genre": "Sci-Fi", "price": 280, "rows": 5, "cols": 6}
                ],
                "bookings": []
            }
            self.save_data(default_data)

    def load_data(self):
        try:
            with open(self.filename, 'r') as file:
                return json.load(file)
        except Exception:
            self.ensure_file_exists()
            with open(self.filename, 'r') as file:
                return json.load(file)

    def save_data(self, data):
        with open(self.filename, 'w') as file:
            json.dump(data, file, indent=4)
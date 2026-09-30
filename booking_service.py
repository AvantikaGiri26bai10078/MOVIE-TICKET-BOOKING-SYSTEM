from db_handler import DBHandler
from movie import Movie

class BookingService:
    def __init__(self):
        self.db = DBHandler()
        self.movies = {}
        self.bookings = []
        self.load_all_data()

    def load_all_data(self):
        # Class ka object (self.db) use karke load_data call kar rahe hain
        data = self.db.load_data()
        
        self.movies.clear()
        for m in data.get("movies", []):
            movie_obj = Movie(
                m["movie_id"],
                m["title"],
                m["genre"],
                m["price"],
                m.get("rows", 5),
                m.get("cols", 6)
            )
            self.movies[m["movie_id"]] = movie_obj

        self.bookings = data.get("bookings", [])

        # Sync existing bookings to seat matrix
        for b in self.bookings:
            m_id = b["movie_id"]
            if m_id in self.movies:
                for r, c in b["seats"]:
                    self.movies[m_id].seats.grid[r][c] = 1

    def save_all_data(self):
        movies_data = [m.to_dict() for m in self.movies.values()]
        full_data = {
            "movies": movies_data,
            "bookings": self.bookings
        }
        self.db.save_data(full_data)

    def book_tickets(self, movie_id, seats_list):
        if movie_id not in self.movies:
            return None

        movie = self.movies[movie_id]
        if not movie.seats.reserve_seats(seats_list):
            return None

        subtotal = len(seats_list) * movie.price
        tax = subtotal * 0.10
        total = subtotal + tax

        booking_id = f"BK{len(self.bookings) + 1}{movie_id}00"
        booking_record = {
            "booking_id": booking_id,
            "movie_id": movie_id,
            "movie_title": movie.title,
            "seats": seats_list,
            "total_bill": total
        }

        self.bookings.append(booking_record)
        self.save_all_data()
        return booking_record, subtotal, tax, total

    def cancel_booking(self, booking_id):
        target = None
        for b in self.bookings:
            if b["booking_id"] == booking_id:
                target = b
                break

        if not target:
            return False

        m_id = target["movie_id"]
        if m_id in self.movies:
            self.movies[m_id].seats.unreserve_seats(target["seats"])

        self.bookings.remove(target)
        self.save_all_data()
        return True
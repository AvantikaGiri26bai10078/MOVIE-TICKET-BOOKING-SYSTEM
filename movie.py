from seat_matrix import SeatMatrix

class Movie:
    def __init__(self, movie_id, title, genre, price, rows=5, cols=6):
        self.movie_id = movie_id
        self.title = title
        self.genre = genre
        self.price = price
        self.seats = SeatMatrix(rows, cols)

    def to_dict(self):
        return {
            "movie_id": self.movie_id,
            "title": self.title,
            "genre": self.genre,
            "price": self.price,
            "rows": self.seats.rows,
            "cols": self.seats.cols
        }
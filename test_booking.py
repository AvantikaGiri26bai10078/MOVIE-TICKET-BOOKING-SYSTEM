import unittest
from booking_service import BookingService

class TestMovieBookingSystem(unittest.TestCase):
    def setUp(self):
        self.service = BookingService()

    def test_movies_existence(self):
        """Verify that specific movies exist in the catalog"""
        movie_titles = [m.title.lower() for m in self.service.movies.values()]

        # Checking for all 5 movies in catalog
        self.assertTrue(any("avengers" in t for t in movie_titles), "Avengers not found")
        self.assertTrue(any("mirzapur" in t for t in movie_titles), "Mirzapur not found")
        self.assertTrue(any("the love hypothesis" in t for t in movie_titles), "The Love Hypothesis not found")
        self.assertTrue(any("3 idiots" in t for t in movie_titles), "3 Idiots not found")
        self.assertTrue(any("interstellar" in t for t in movie_titles), "Interstellar not found")

    def test_booking_calculation(self):
        """Test calculation accuracy for booking tickets"""
        first_m_id = list(self.service.movies.keys())[0]
        movie = self.service.movies[first_m_id]

        # Ensure test seat is free before testing
        test_seat = [(0, 0)]
        movie.seats.unreserve_seats(test_seat)

        res = self.service.book_tickets(first_m_id, test_seat)
        self.assertIsNotNone(res)

        b_data, subtotal, tax, total = res
        expected_subtotal = movie.price * 1
        expected_tax = expected_subtotal * 0.10
        expected_total = expected_subtotal + expected_tax

        self.assertEqual(subtotal, expected_subtotal)
        self.assertEqual(tax, expected_tax)
        self.assertEqual(total, expected_total)

if __name__ == '__main__':
    unittest.main()
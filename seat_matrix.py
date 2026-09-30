class SeatMatrix:
    def __init__(self, rows=5, cols=6):
        self.rows = rows
        self.cols = cols
        self.grid = []
        for r in range(rows):
            row_list = []
            for c in range(cols):
                row_list.append(0)
            self.grid.append(row_list)

    def display_seats(self, movie_title):
        print(f"\n--- Seat Layout for {movie_title} ---")
        header = "      "
        for c in range(self.cols):
            header += f"C{c+1} "
        print(header)
        print("     " + "---" * self.cols)

        for r in range(self.rows):
            row_str = f"R{r+1} | "
            for c in range(self.cols):
                if self.grid[r][c] == 1:
                    row_str += "[X] "
                else:
                    row_str += "[O] "
            print(row_str)
        print("\nNote: [O] = Free, [X] = Booked")

    def reserve_seats(self, seat_list):
        for r, c in seat_list:
            if r < 0 or r >= self.rows or c < 0 or c >= self.cols:
                return False
            if self.grid[r][c] == 1:
                return False

        for r, c in seat_list:
            self.grid[r][c] = 1
        return True

    def unreserve_seats(self, seat_list):
        for r, c in seat_list:
            if 0 <= r < self.rows and 0 <= c < self.cols:
                self.grid[r][c] = 0
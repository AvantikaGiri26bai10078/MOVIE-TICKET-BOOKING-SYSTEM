from booking_service import BookingService

def main():
    service = BookingService()

    while True:
        print("\n==================================")
        print("  MOVIE TICKET BOOKING SYSTEM")
        print("==================================")
        print("1. Display All Movies")
        print("2. Display Seat Layout")
        print("3. Book Movie Tickets")
        print("4. Cancel Booking")
        print("5. Exit")

        choice = input("\nEnter choice (1-5): ").strip()

        if choice == "1":
            print("\n---------------- AVAILABLE MOVIES ----------------")
            print(f"{'ID':<5} {'Title':<20} {'Genre':<12} {'Price':<8}")
            print("--------------------------------------------------")
            for m_id, m in service.movies.items():
                print(f"{m_id:<5} {m.title:<20} {m.genre:<12} Rs {m.price}")

        elif choice == "2":
            try:
                m_id = int(input("Enter Movie ID: "))
                if m_id in service.movies:
                    m = service.movies[m_id]
                    m.seats.display_seats(m.title)
                else:
                    print("Invalid Movie ID!")
            except ValueError:
                print("Please enter a valid number ID.")

        elif choice == "3":
            try:
                m_id = int(input("Enter Movie ID to book: "))
                if m_id not in service.movies:
                    print("Invalid Movie ID!")
                    continue

                movie = service.movies[m_id]
                movie.seats.display_seats(movie.title)

                count = int(input("\nHow many seats do you want to book? "))
                if count <= 0:
                    print("Seat count must be at least 1.")
                    continue

                requested_seats = []
                print("Enter seat choices (Row and Column):")
                for i in range(count):
                    r = int(input(f"  Seat {i+1} Row number (1-{movie.seats.rows}): ")) - 1
                    c = int(input(f"  Seat {i+1} Col number (1-{movie.seats.cols}): ")) - 1
                    requested_seats.append((r, c))

                # --- YES / NO CONFIRMATION PROMPT ---
                confirm = input("\nDo you want to confirm this booking? (yes/no): ").strip().lower()
                if confirm not in ['y', 'yes']:
                    print("\nBooking cancelled by user.")
                    continue

                res = service.book_tickets(m_id, requested_seats)
                if res:
                    b_data, subtotal, tax, total = res
                    print("\n================ RECEIPT ================")
                    print(f"Booking ID  : {b_data['booking_id']}")
                    print(f"Movie Name  : {movie.title}")
                    print(f"Seats Count : {count}")
                    print(f"Subtotal    : Rs {subtotal:.2f}")
                    print(f"Tax (10%)   : Rs {tax:.2f}")
                    print(f"Total Amount: Rs {total:.2f}")
                    print("=========================================")
                else:
                    print("\nBooking Failed! Selected seats are invalid or already booked.")

            except ValueError:
                print("Invalid input! Please enter numbers only.")

        elif choice == "4":
            b_id = input("Enter Booking ID to cancel (e.g. BK123): ").strip().upper()
            
            # --- YES / NO CONFIRMATION PROMPT FOR CANCELLATION ---
            confirm = input(f"Are you sure you want to cancel booking {b_id}? (yes/no): ").strip().lower()
            if confirm in ['y', 'yes']:
                if service.cancel_booking(b_id):
                    print(f"Booking {b_id} successfully cancelled and refunded.")
                else:
                    print("Booking ID not found!")
            else:
                print("Cancellation process aborted.")

        elif choice == "5":
            print("\nThank you for using the booking system. Goodbye!")
            break

        else:
            print("Invalid choice! Please choose 1 to 5.")

if __name__ == "__main__":
    main()
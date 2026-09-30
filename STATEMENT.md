# Problem Statement & System Requirements

## 1. Project Title
**Python-Based Movie Ticket Booking System (CLI & GUI)**

## 2. Problem Overview
The traditional movie ticketing process often suffers from inefficient manual record-keeping, seat allocation overlaps, and lack of immediate booking verification. This project delivers an integrated, file-backed Python system featuring both a Command-Line Interface (CLI) and a Graphical User Interface (GUI) to handle movie listing, real-time interactive seat booking, cost calculation with taxes, and booking cancellations.

## 3. Functional Requirements (FRs)
- **FR1: Dynamic Catalog Management**: Load movies dynamically from `data.json` including fields such as `title`, `genre`, `price`, `rows`, and `cols`.
- **FR2: Interactive Seat Matrix**: Display row/column seat status (Available vs. Booked vs. Selected) using color coding in the GUI and formatted matrix layouts in the CLI.
- **FR3: Ticket Reservation & Taxation**: Calculate subtotal based on price per ticket, add a 10% tax rate, and generate unique booking reference IDs.
- **FR4: Double-Booking Prevention**: Validate seat availability prior to booking confirmation and flag already occupied seats.
- **FR5: Booking Cancellation & Seat Release**: Allow users to cancel bookings using their Booking ID and restore seat availability in real time.
- **FR6: Data Persistence**: Automatically sync all booking operations back to `data.json`.

## 4. Non-Functional Requirements (NFRs)
- **NFR1: Portability**: Built using standard Python libraries (`tkinter`, `json`, `unittest`), requiring no external dependencies.
- **NFR2: Usability**: Provide an intuitive, responsive GUI layout with a distinct screen direction indicator and visual color cues.
- **NFR3: Reliability & Data Integrity**: Prevent race conditions or state inconsistencies by maintaining uniform backend logic shared between CLI and GUI modes.
- **NFR4: Testability**: Maintain high unit test coverage (`unittest`) for catalog validation, financial calculations, double-booking prevention, and seat release mechanisms.

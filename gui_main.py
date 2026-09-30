import tkinter as tk
from tkinter import messagebox, ttk
from booking_service import BookingService

class MovieBookingGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("🎬 Premium Cinema Ticket Booking System")
        self.root.geometry("750x820")
        self.root.configure(bg="#0F172A")  # Dark Slate Background

        self.service = BookingService()
        self.selected_seats = []
        self.seat_buttons = {}
        self.selected_movie_id = None

        self.apply_styles()
        self.create_widgets()

    def apply_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure(
            "TCombobox", 
            fieldbackground="#1E293B", 
            background="#334155", 
            foreground="#F8FAFC", 
            padding=6,
            arrowcolor="#F59E0B"
        )
        style.map("TCombobox", fieldbackground=[("readonly", "#1E293B")], foreground=[("readonly", "#F8FAFC")])

    def create_widgets(self):
        # Header Banner
        header_frame = tk.Frame(self.root, bg="#1E1E2E", pady=18)
        header_frame.pack(fill=tk.X)
        
        tk.Label(
            header_frame, 
            text="🎬 CINEMA TICKET BOOKING", 
            font=("Segoe UI", 20, "bold"), 
            fg="#F59E0B",  # Gold accent
            bg="#1E1E2E"
        ).pack()

        # Main Container
        main_container = tk.Frame(self.root, bg="#0F172A", padx=25, pady=15)
        main_container.pack(fill=tk.BOTH, expand=True)

        # Movie Selection Area Card
        movie_card = tk.Frame(main_container, bg="#1E293B", bd=0, padx=15, pady=12)
        movie_card.pack(fill=tk.X, pady=(0, 10))

        tk.Label(
            movie_card, 
            text="Select Movie:", 
            font=("Segoe UI", 11, "bold"), 
            bg="#1E293B", 
            fg="#94A3B8"
        ).pack(side=tk.LEFT, padx=(0, 10))

        # Dynamic Movie List Generation
        self.movie_map = {}
        combo_values = []
        for m_id, m in self.service.movies.items():
            label = f"{m.title} | {m.genre} | Rs. {m.price}"
            self.movie_map[label] = m_id
            combo_values.append(label)

        self.movie_combo = ttk.Combobox(
            movie_card, 
            values=combo_values, 
            state="readonly", 
            font=("Segoe UI", 10)
        )
        self.movie_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
        self.movie_combo.bind("<<ComboboxSelected>>", self.on_movie_select)

        # Movie Details Info Card
        self.info_card = tk.Frame(main_container, bg="#334155", pady=8, padx=10)
        self.info_card.pack(fill=tk.X, pady=(0, 15))

        self.info_label = tk.Label(
            self.info_card, 
            text=" Please select a movie to view seat matrix.", 
            font=("Segoe UI", 10, "bold"), 
            bg="#334155", 
            fg="#F8FAFC"
        )
        self.info_label.pack()

        # Seat Matrix Container Card
        self.grid_container = tk.Frame(main_container, bg="#1E293B", padx=20, pady=20)
        self.grid_container.pack(fill=tk.BOTH, expand=True)

        # Legend / Color Guide
        legend_frame = tk.Frame(main_container, bg="#0F172A", pady=12)
        legend_frame.pack()

        self.draw_legend(legend_frame, "#10B981", "Available")
        self.draw_legend(legend_frame, "#EF4444", "Booked")
        self.draw_legend(legend_frame, "#F59E0B", "Selected")

        # Bottom Action Bar
        action_frame = tk.Frame(main_container, bg="#0F172A", pady=10)
        action_frame.pack()

        tk.Button(
            action_frame, 
            text=" Confirm Booking", 
            bg="#10B981", 
            fg="#FFFFFF", 
            activebackground="#059669",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 11, "bold"), 
            padx=20, 
            pady=10, 
            bd=0, 
            cursor="hand2",
            command=self.book_tickets
        ).grid(row=0, column=0, padx=12)

        tk.Button(
            action_frame, 
            text=" Cancel Booking", 
            bg="#EF4444", 
            fg="#FFFFFF", 
            activebackground="#DC2626",
            activeforeground="#FFFFFF",
            font=("Segoe UI", 11, "bold"), 
            padx=20, 
            pady=10, 
            bd=0, 
            cursor="hand2",
            command=self.cancel_booking
        ).grid(row=0, column=1, padx=12)

        # Auto select first movie
        if combo_values:
            self.movie_combo.current(0)
            self.on_movie_select(None)

    def draw_legend(self, parent, color, text):
        box = tk.Frame(parent, bg=color, width=16, height=16)
        box.pack(side=tk.LEFT, padx=(15, 6))
        lbl = tk.Label(parent, text=text, font=("Segoe UI", 10, "bold"), bg="#0F172A", fg="#CBD5E1")
        lbl.pack(side=tk.LEFT)

    def on_movie_select(self, event):
        selected_text = self.movie_combo.get()
        if selected_text in self.movie_map:
            self.selected_movie_id = self.movie_map[selected_text]
            movie = self.service.movies[self.selected_movie_id]
            self.info_label.config(
                text=f"🎬 {movie.title}  |  Genre: {movie.genre}  |  Ticket Price: Rs. {movie.price}"
            )
            self.render_seat_grid()

    def render_seat_grid(self):
        for widget in self.grid_container.winfo_children():
            widget.destroy()

        self.selected_seats.clear()
        self.seat_buttons.clear()

        if not self.selected_movie_id:
            return

        movie = self.service.movies[self.selected_movie_id]
        matrix = movie.seats

        # Curved Screen Graphic
        screen_frame = tk.Frame(self.grid_container, bg="#38BDF8", height=6)
        screen_frame.pack(fill=tk.X, padx=40, pady=(5, 2))

        screen_lbl = tk.Label(
            self.grid_container, 
            text="━━━ SCREEN THIS WAY ━━━", 
            bg="#1E293B", 
            fg="#38BDF8", 
            font=("Segoe UI", 9, "bold")
        )
        screen_lbl.pack(pady=(0, 20))

        # Centered Seat Grid Box
        seats_frame = tk.Frame(self.grid_container, bg="#1E293B")
        seats_frame.pack(anchor="center")

        for r in range(matrix.rows):
            seats_frame.grid_rowconfigure(r, weight=1)
            for c in range(matrix.cols):
                seats_frame.grid_columnconfigure(c, weight=1)
                is_booked = (matrix.grid[r][c] == 1)
                seat_code = f"R{r+1}C{c+1}"

                bg_color = "#EF4444" if is_booked else "#10B981"

                btn = tk.Button(
                    seats_frame, 
                    text=seat_code, 
                    width=7, 
                    height=2,
                    bg=bg_color,
                    fg="#FFFFFF",
                    activebackground="#F59E0B",
                    activeforeground="#FFFFFF",
                    font=("Segoe UI", 9, "bold"),
                    bd=0,
                    relief=tk.FLAT,
                    cursor="hand2" if not is_booked else "no",
                    state=tk.DISABLED if is_booked else tk.NORMAL,
                    command=lambda row=r, col=c: self.toggle_seat_selection(row, col)
                )
                btn.grid(row=r, column=c, padx=6, pady=6)
                self.seat_buttons[(r, c)] = btn

    def toggle_seat_selection(self, r, c):
        btn = self.seat_buttons[(r, c)]
        if (r, c) in self.selected_seats:
            self.selected_seats.remove((r, c))
            btn.config(bg="#10B981")
        else:
            self.selected_seats.append((r, c))
            btn.config(bg="#F59E0B")

    def book_tickets(self):
        if not self.selected_movie_id:
            messagebox.showwarning("Warning", "Please select a movie first!")
            return

        if not self.selected_seats:
            messagebox.showwarning("Warning", "Please select at least one seat!")
            return

        res = self.service.book_tickets(self.selected_movie_id, self.selected_seats)
        if res:
            b_data, subtotal, tax, total = res
            receipt_msg = (
                f"🎉 BOOKING CONFIRMED!\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Booking ID  : {b_data['booking_id']}\n"
                f"Movie       : {b_data['movie_title']}\n"
                f"Seats       : {len(self.selected_seats)} Ticket(s)\n\n"
                f"Subtotal    : Rs {subtotal:.2f}\n"
                f"Tax (10%)   : Rs {tax:.2f}\n"
                f"━━━━━━━━━━━━━━━━━━━━━━\n"
                f"Total Paid  : Rs {total:.2f}"
            )
            messagebox.showinfo("Receipt", receipt_msg)
            self.render_seat_grid()
        else:
            messagebox.showerror("Error", "Booking failed! Seats are already taken.")

    def cancel_booking(self):
        cancel_win = tk.Toplevel(self.root)
        cancel_win.title("Cancel Booking")
        cancel_win.geometry("340x200")
        cancel_win.configure(bg="#1E293B")

        tk.Label(cancel_win, text="Enter Booking ID to Cancel:", font=("Segoe UI", 11, "bold"), bg="#1E293B", fg="#F8FAFC").pack(pady=(20, 8))
        
        entry_id = tk.Entry(cancel_win, font=("Segoe UI", 11), justify="center", bd=1, relief=tk.FLAT, bg="#334155", fg="#FFFFFF", insertbackground="white")
        entry_id.pack(pady=5, ipady=5, padx=20, fill=tk.X)

        def process_cancel():
            b_id = entry_id.get().strip().upper()
            if self.service.cancel_booking(b_id):
                messagebox.showinfo("Success", f"Booking {b_id} cancelled successfully!")
                cancel_win.destroy()
                if self.selected_movie_id:
                    self.render_seat_grid()
            else:
                messagebox.showerror("Error", "Invalid Booking ID!")

        tk.Button(
            cancel_win, 
            text="Confirm Cancellation", 
            bg="#EF4444", 
            fg="white", 
            font=("Segoe UI", 10, "bold"), 
            padx=12, 
            pady=6, 
            bd=0,
            cursor="hand2",
            command=process_cancel
        ).pack(pady=15)

if __name__ == "__main__":
    root = tk.Tk()
    app = MovieBookingGUI(root)
    root.mainloop()
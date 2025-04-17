import customtkinter as ctk
from tkinter import ttk, messagebox
from datetime import datetime, date
from db_helper import DatabaseManager


class HotelReservationsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Initialize data
        self.reservations = []
        self.selected_reservation_id = None
        self.sort_column = None
        self.sort_descending = False

        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Create components
        self.create_sidebar()
        self.create_main_content()

        # Bind to frame activation
        self.bind("<Visibility>", lambda e: self.load_data())

    def load_data(self):
        """Load reservations data from database"""
        try:
            # Ensure database connection
            if not hasattr(self.controller, 'db'):
                self.controller.db = DatabaseManager()

            if not self.controller.db.connection.is_connected():
                self.controller.db.connect()

            with self.controller.db.connection.cursor(dictionary=True) as cursor:
                cursor.execute("""
                    SELECT 
                        reservation_id as id,
                        guest_name as name,
                        DATE_FORMAT(checkin_date, '%b %d, %Y') as checkin,
                        CONCAT('$', FORMAT(booking_amount, 2)) as amount
                    FROM reservations
                    WHERE user_id = %s
                    ORDER BY checkin_date DESC
                """, (self.controller.current_user['user_id'],))
                self.reservations = cursor.fetchall()

            # Update the UI with the loaded data
            self.display_reservations()

        except Exception as e:
            self.reservations = []
            self.display_reservations()

    def save_data(self, reservation_data=None, delete_id=None):
        """Save or delete reservation data in database"""
        try:
            # Ensure database connection
            if not hasattr(self.controller, 'db') or not self.controller.db.connection.is_connected():
                self.controller.db = DatabaseManager()
                self.controller.db.connect()

            with self.controller.db.connection.cursor() as cursor:
                if reservation_data and 'id' in reservation_data:
                    # Parse the date string into a datetime object first
                    try:
                        checkin_date = datetime.strptime(reservation_data['checkin'], "%b %d, %Y").date()
                        amount = float(reservation_data['amount'].replace('$', '').replace(',', ''))
                    except ValueError as e:
                        messagebox.showerror("Error", f"Invalid format: {str(e)}")
                        return False

                    # Update existing reservation
                    if any(r['id'] == reservation_data['id'] for r in self.reservations):
                        cursor.execute("""
                            UPDATE reservations 
                            SET guest_name = %s, 
                                checkin_date = %s, 
                                booking_amount = %s
                            WHERE reservation_id = %s AND user_id = %s
                        """, (
                            reservation_data['name'],
                            checkin_date,
                            amount,
                            reservation_data['id'],
                            self.controller.current_user['user_id']
                        ))
                    else:
                        # Insert new reservation
                        cursor.execute("""
                            INSERT INTO reservations 
                            (reservation_id, user_id, guest_name, checkin_date, booking_amount)
                            VALUES (%s, %s, %s, %s, %s)
                        """, (
                            reservation_data['id'],
                            self.controller.current_user['user_id'],
                            reservation_data['name'],
                            checkin_date,
                            amount
                        ))
                elif delete_id:
                    # Delete reservation
                    cursor.execute("""
                        DELETE FROM reservations 
                        WHERE reservation_id = %s AND user_id = %s
                    """, (delete_id, self.controller.current_user['user_id']))

                self.controller.db.connection.commit()
                self.load_data()  # Refresh data after changes
                return True

        except Exception as e:
            messagebox.showerror("Error", f"Database operation failed: {str(e)}")
            if "MySQL Connection not available" in str(e):
                try:
                    self.controller.db.connect()
                    return self.save_data(reservation_data, delete_id)
                except:
                    pass
            return False

    def create_sidebar(self):
        """Create the sidebar navigation"""
        sidebar = ctk.CTkFrame(self, width=250, fg_color="#f0f9ff", corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")

        # Navigation items
        nav_items = [
            ("Dashboard", "📊", "HotelBookingDashboard"),
            ("Reservations", "🛒", "HotelReservationsPage"),
            ("Customers", "👥", "CustomerManagementScreen"),
            ("Reports", "📄", "HotelReportsPage")
        ]

        # Add padding
        padding = ctk.CTkLabel(sidebar, text="", fg_color="transparent")
        padding.pack(pady=(20, 10))

        # Add navigation buttons
        for item, icon, frame_name in nav_items:
            is_active = frame_name == "HotelReservationsPage"
            btn_color = "#dbeafe" if is_active else "transparent"

            btn_frame = ctk.CTkFrame(sidebar, fg_color=btn_color, corner_radius=8)
            btn_frame.pack(fill="x", padx=15, pady=5)

            content_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
            content_frame.pack(pady=8, padx=15, anchor="w")

            ctk.CTkLabel(
                content_frame,
                text=icon,
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(side="left", padx=(0, 10))

            btn = ctk.CTkButton(
                content_frame,
                text=item,
                font=("Arial", 14),
                text_color="#64748b",
                fg_color="transparent",
                hover_color="#f0f0f0",
                anchor="w",
                command=lambda fn=frame_name: self.controller.show_frame(fn)
            )
            btn.pack(side="left")

        # Add logout button
        logout_frame = ctk.CTkFrame(sidebar, fg_color="transparent")
        logout_frame.pack(side="bottom", fill="x", padx=15, pady=20)

        ctk.CTkButton(
            logout_frame,
            text="Logout",
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.logout
        ).pack(fill="x")

    def logout(self):
        """Handle user logout"""
        self.controller.current_user = None
        self.controller.show_frame("LoginApp")

    def create_main_content(self):
        """Create the main content area with reservations table"""
        # Main container
        main = ctk.CTkFrame(self, fg_color="white")
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)

        # Header section
        header_frame = ctk.CTkFrame(main, height=70, fg_color="white", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=0)
        header_frame.grid_columnconfigure(1, weight=1)
        header_frame.grid_columnconfigure(2, weight=0)

        # Logo
        logo_label = ctk.CTkLabel(
            header_frame,
            text="Hotel Booking and Management System",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        )
        logo_label.grid(row=0, column=0, padx=(20, 10), pady=20, sticky="w")

        # Navigation items in header
        nav_items = [
            ("Dashboard", "HotelBookingDashboard"),
            ("Customers", "CustomerManagementScreen"),
            ("Reservations", "HotelReservationsPage"),
            ("Reports", "HotelReportsPage")
        ]

        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=1, sticky="")

        for item, frame_name in nav_items:
            text_color = "#3b82f6" if frame_name == self.__class__.__name__ else "#64748b"
            btn = ctk.CTkButton(
                nav_frame,
                text=item,
                fg_color="transparent",
                text_color=text_color,
                hover_color="#f8f8f8",
                corner_radius=5,
                height=32,
                border_width=0,
                command=lambda fn=frame_name: self.controller.show_frame(fn)
            )
            btn.pack(side="left", padx=15)

        # User info
        icons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        icons_frame.grid(row=0, column=2, padx=20, sticky="e")

        if hasattr(self.controller, 'current_user') and self.controller.current_user:
            username = self.controller.current_user.get('full_name', '').split()[0]
            if username:
                ctk.CTkLabel(
                    icons_frame,
                    text=username,
                    font=("Arial", 14),
                    text_color="#64748b"
                ).pack(side="left", padx=5)

        # Scrollable content area
        content_frame = ctk.CTkFrame(main, fg_color="#f8fafc")
        content_frame.grid(row=1, column=0, sticky="nsew")
        content_frame.grid_rowconfigure(1, weight=1)
        content_frame.grid_columnconfigure(0, weight=1)

        # Page title
        title_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        title_frame.grid(row=0, column=0, sticky="ew", padx=30, pady=(30, 20))
        title_frame.grid_columnconfigure(0, weight=1)

        ctk.CTkLabel(
            title_frame,
            text="All Reservations",
            font=("Arial", 24, "bold"),
            text_color="#2c3e50"
        ).grid(row=0, column=0, sticky="w")

        # Action buttons
        action_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        action_frame.grid(row=0, column=1, sticky="e")

        new_btn = ctk.CTkButton(
            action_frame,
            text="New Reservation",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.add_reservation
        )
        new_btn.pack(side="left", padx=5)

        edit_btn = ctk.CTkButton(
            action_frame,
            text="Edit",
            fg_color="#f59e0b",
            hover_color="#d97706",
            command=self.edit_reservation
        )
        edit_btn.pack(side="left", padx=5)

        delete_btn = ctk.CTkButton(
            action_frame,
            text="Delete",
            fg_color="#ef4444",
            hover_color="#dc2626",
            command=self.delete_reservation
        )
        delete_btn.pack(side="left", padx=5)

        # Search bar
        search_frame = ctk.CTkFrame(content_frame, fg_color="transparent")
        search_frame.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 20))

        self.search_entry = ctk.CTkEntry(
            search_frame,
            placeholder_text="Search by ID, Name or Date",
            width=400,
            height=40,
            fg_color="white",
            border_color="#d1d5db",
            border_width=1,
            corner_radius=8
        )
        self.search_entry.pack(side="left")
        self.search_entry.bind("<KeyRelease>", self.search_reservations)

        # Treeview Table Frame
        table_container = ctk.CTkFrame(content_frame, fg_color="white", corner_radius=12)
        table_container.grid(row=2, column=0, sticky="nsew", padx=30, pady=(0, 30))
        table_container.grid_rowconfigure(0, weight=1)
        table_container.grid_columnconfigure(0, weight=1)

        # Create Treeview with scrollbar
        self.tree_frame = ctk.CTkFrame(table_container, fg_color="white")
        self.tree_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Create Treeview with scrollbar
        style = ttk.Style()
        style.theme_use("default")

        # Configure the Treeview style
        style.configure("Treeview",
                        background="#ffffff",
                        foreground="#475569",
                        rowheight=40,
                        fieldbackground="#ffffff",
                        font=("Arial", 12)
                        )
        style.configure("Treeview.Heading",
                        font=("Arial", 12, "bold"),
                        foreground="#64748b"
                        )

        # Selection colors
        style.map('Treeview',
                  background=[('selected', '#e0f2fe')],
                  foreground=[('selected', '#475569')]
                  )

        # Create scrollbar
        scrollbar = ttk.Scrollbar(self.tree_frame)
        scrollbar.pack(side="right", fill="y")

        # Create Treeview
        self.tree = ttk.Treeview(
            self.tree_frame,
            columns=("id", "name", "checkin", "amount"),
            show="headings",
            height=10,
            yscrollcommand=scrollbar.set
        )
        scrollbar.config(command=self.tree.yview)

        # Define column headings - ensure all are left-aligned
        column_data = [
            ("id", "ID Number", 120),
            ("name", "Guest Name", 200),
            ("checkin", "Check-in Date", 150),
            ("amount", "Total Booking Amount", 200)
        ]

        for col_id, col_name, col_width in column_data:
            self.tree.heading(col_id, text=col_name, anchor="w")  # Set heading to left-aligned
            self.tree.column(col_id, width=col_width, anchor="w")  # Set column content to left-aligned

        # Add sorting functionality
        for col in ["id", "name", "checkin", "amount"]:
            self.tree.heading(col, command=lambda c=col: self.sort_treeview(c))

        self.tree.pack(fill="both", expand=True)

        # Bind selection event
        self.tree.bind("<<TreeviewSelect>>", self.on_tree_select)

        # Add padding to left of first column for better appearance
        style.layout("Treeview", [
            ('Treeview.treearea', {'sticky': 'nswe'})
        ])

    def display_reservations(self, reservations=None):
        """Display reservations in the treeview"""
        # Clear existing rows
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Reset selection
        self.selected_reservation_id = None

        # Use filtered reservations if provided
        display_data = reservations if reservations is not None else self.reservations

        if not display_data:
            # Show empty message if needed
            return

        # Insert data into treeview
        for reservation in display_data:
            # Add a space prefix to each value for visual padding
            item = self.tree.insert("", "end", values=(
                f" {reservation['id']}",
                f" {reservation['name']}",
                f" {reservation['checkin']}",
                f" {reservation['amount']}"
            ))

    def on_tree_select(self, event):
        """Handle treeview row selection"""
        selection = self.tree.selection()
        if selection:
            item = self.tree.item(selection[0])
            values = item["values"]
            # Strip the space we added for padding when getting the ID
            self.selected_reservation_id = values[0].strip()  # ID is the first column

    def search_reservations(self, event=None):
        """Filter reservations based on search query"""
        query = self.search_entry.get().lower()

        if not query:
            self.display_reservations()
            return

        filtered = [
            r for r in self.reservations
            if (query in r["id"].lower() or
                query in r["name"].lower() or
                query in r["checkin"].lower())
        ]

        self.display_reservations(filtered)

    def sort_treeview(self, column):
        """Sort the treeview by the given column"""
        # Determine sort order
        if self.sort_column == column:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = column
            self.sort_descending = False

        # Define sort key functions
        if column == "checkin":
            def sort_key(x):
                try:
                    return datetime.strptime(x[column], "%b %d, %Y")
                except:
                    return datetime.min
        elif column == "amount":
            def sort_key(x):
                try:
                    return float(x[column].replace("$", "").replace(",", ""))
                except:
                    return 0.0
        else:
            def sort_key(x):
                return x[column].lower()

        # Sort the reservations
        sorted_reservations = sorted(
            self.reservations,
            key=sort_key,
            reverse=self.sort_descending
        )

        # Display the sorted data
        self.display_reservations(sorted_reservations)

    # Helper method to validate check-in date
    def validate_date(self, date_str):
        """Validate that a date is today or in the future"""
        try:
            checkin_date = datetime.strptime(date_str, "%b %d, %Y").date()
            today = date.today()

            if checkin_date < today:
                return False, "Check-in date cannot be in the past. Please select today or a future date."
            return True, ""
        except ValueError as e:
            return False, f"Invalid date format: {str(e)}"

    def add_reservation(self):
        """Open dialog to add a new reservation"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Reservation")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        # Add today's date in placeholder for better guidance
        today_formatted = datetime.now().strftime("%b %d, %Y")

        fields = [
            ("ID Number", "#", "id"),
            ("Guest Name", "Full name", "name"),
            ("Check-in Date", f"Format: {today_formatted} (today or future dates only)", "checkin"),
            ("Total Booking Amount", "$0.00", "amount")
        ]

        entries = {}

        for i, (label, placeholder, key) in enumerate(fields):
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=10)

            ctk.CTkLabel(
                frame,
                text=label,
                font=("Arial", 14),
                text_color="#475569"
            ).pack(anchor="w")

            entry = ctk.CTkEntry(
                frame,
                placeholder_text=placeholder,
                height=40,
                fg_color="white",
                border_color="#d1d5db",
                border_width=1,
                corner_radius=8
            )
            # Pre-fill with today's date as a convenience
            if key == "checkin":
                entry.insert(0, today_formatted)

            entry.pack(fill="x")
            entries[key] = entry

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)

        def save():
            new_reservation = {}
            for key, entry in entries.items():
                value = entry.get().strip()
                if not value:
                    messagebox.showerror("Error", f"Please enter {key}")
                    return
                new_reservation[key] = value

            # Validate amount
            try:
                float(new_reservation["amount"].replace("$", "").replace(",", ""))
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid amount format: {str(e)}")
                return

            # Validate checkin date
            valid_date, error_msg = self.validate_date(new_reservation["checkin"])
            if not valid_date:
                messagebox.showerror("Error", error_msg)
                return

            # Check for duplicate ID
            if any(r["id"] == new_reservation["id"] for r in self.reservations):
                messagebox.showerror("Error", "Reservation ID already exists")
                return

            if self.save_data(reservation_data=new_reservation):
                dialog.destroy()
                messagebox.showinfo("Success", "Reservation added successfully")

        ctk.CTkButton(
            button_frame,
            text="Save",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=save
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            fg_color="#64748b",
            hover_color="#475569",
            command=dialog.destroy
        ).pack(side="left", padx=10)

    def edit_reservation(self):
        """Open dialog to edit selected reservation"""
        if not self.selected_reservation_id:
            messagebox.showwarning("Warning", "Please select a reservation to edit")
            return

        reservation = next(
            (r for r in self.reservations if r["id"] == self.selected_reservation_id),
            None
        )

        if not reservation:
            messagebox.showerror("Error", "Selected reservation not found")
            return

        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Reservation")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()

        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (dialog.winfo_screenwidth() // 2) - (width // 2)
        y = (dialog.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f"{width}x{height}+{x}+{y}")

        fields = [
            ("ID Number", "id", False),
            ("Guest Name", "name", True),
            ("Check-in Date", "checkin", True),
            ("Total Booking Amount", "amount", True)
        ]

        entries = {}

        for i, (label, key, editable) in enumerate(fields):
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=10)

            label_text = label
            if key == "checkin":
                label_text = f"{label} (today or future dates only)"

            ctk.CTkLabel(
                frame,
                text=label_text,
                font=("Arial", 14),
                text_color="#475569"
            ).pack(anchor="w")

            entry = ctk.CTkEntry(
                frame,
                height=40,
                fg_color="white",
                border_color="#d1d5db",
                border_width=1,
                corner_radius=8
            )
            entry.insert(0, reservation[key])
            entry.configure(state="normal" if editable else "disabled")
            entry.pack(fill="x")
            entries[key] = entry

        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)

        def save():
            updated_reservation = {'id': reservation['id']}
            for key, entry in entries.items():
                if entry.cget("state") != "disabled":
                    value = entry.get().strip()
                    if not value:
                        messagebox.showerror("Error", f"Please enter {key}")
                        return
                    updated_reservation[key] = value

            # Validate amount
            if "amount" in updated_reservation:
                try:
                    float(updated_reservation["amount"].replace("$", "").replace(",", ""))
                except ValueError as e:
                    messagebox.showerror("Error", f"Invalid amount format: {str(e)}")
                    return

            # Validate checkin date
            if "checkin" in updated_reservation:
                valid_date, error_msg = self.validate_date(updated_reservation["checkin"])
                if not valid_date:
                    messagebox.showerror("Error", error_msg)
                    return

            if self.save_data(reservation_data=updated_reservation):
                dialog.destroy()
                messagebox.showinfo("Success", "Reservation updated successfully")

        ctk.CTkButton(
            button_frame,
            text="Save",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=save
        ).pack(side="left", padx=10)

        ctk.CTkButton(
            button_frame,
            text="Cancel",
            fg_color="#64748b",
            hover_color="#475569",
            command=dialog.destroy
        ).pack(side="left", padx=10)

    def delete_reservation(self):
        """Delete selected reservation"""
        if not self.selected_reservation_id:
            messagebox.showwarning("Warning", "Please select a reservation to delete")
            return

        reservation = next(
            (r for r in self.reservations if r["id"] == self.selected_reservation_id),
            None
        )

        if not reservation:
            messagebox.showerror("Error", "Selected reservation not found")
            return

        if not messagebox.askyesno(
                "Confirm",
                f"Are you sure you want to delete reservation {reservation['id']} for {reservation['name']}?"
        ):
            return

        if self.save_data(delete_id=self.selected_reservation_id):
            self.selected_reservation_id = None
            messagebox.showinfo("Success", "Reservation deleted successfully")
import customtkinter as ctk
from tkinter import messagebox
from datetime import datetime
from db_helper import DatabaseManager

class HotelReservationsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Initialize data
        self.reservations = []
        self.selected_row = None
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
            # Check if user is logged in
            if not hasattr(self.controller, 'current_user') or self.controller.current_user is None:
                messagebox.showerror("Error", "User not logged in")
                self.controller.show_frame("LoginApp")
                return
                
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
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            self.reservations = []
            self.display_reservations()

    def save_data(self, reservation_data=None, delete_id=None):
        """Save or delete reservation data in database"""
        try:
            # Check if user is logged in
            if not hasattr(self.controller, 'current_user') or self.controller.current_user is None:
                messagebox.showerror("Error", "User not logged in")
                self.controller.show_frame("LoginApp")
                return False
                
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
            text="Hotel Booking System", 
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
        
        # Right side icons
        icons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        icons_frame.grid(row=0, column=2, padx=20, sticky="e")
        
        search_icon = ctk.CTkLabel(icons_frame, text="🔍", font=("Arial", 20))
        search_icon.pack(side="left", padx=10)
        
        notification_icon = ctk.CTkLabel(icons_frame, text="🔔", font=("Arial", 20))
        notification_icon.pack(side="left", padx=10)
        
        profile_icon = ctk.CTkLabel(icons_frame, text="👤", font=("Arial", 20))
        profile_icon.pack(side="left", padx=10)
        
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
        canvas_frame = ctk.CTkFrame(main, fg_color="#f8fafc")
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        canvas = ctk.CTkCanvas(canvas_frame, bg="#f8fafc", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(canvas_frame, orientation="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.grid(row=0, column=0, sticky="nsew")
        
        content = ctk.CTkFrame(canvas, fg_color="#f8fafc")
        canvas_window = canvas.create_window((0, 0), window=content, anchor="nw")
        
        # Page title
        title_frame = ctk.CTkFrame(content, fg_color="transparent")
        title_frame.pack(fill="x", padx=30, pady=(30, 20))
        
        ctk.CTkLabel(
            title_frame,
            text="All Reservations",
            font=("Arial", 24, "bold"),
            text_color="#2c3e50"
        ).pack(side="left")
        
        # Action buttons
        action_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        action_frame.pack(side="right")
        
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
        search_frame = ctk.CTkFrame(content, fg_color="transparent")
        search_frame.pack(fill="x", padx=30, pady=(0, 20))
        
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
        
        # Reservations table
        self.table_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        self.table_frame.pack(fill="both", expand=True, padx=30, pady=(0, 30))
        
        # Table headers
        headers = ["ID Number", "Guest Name", "Check-in Date", "Total Booking Amount"]
        
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        for col, header in enumerate(headers):
            header_label = ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 14, "bold"),
                text_color="#64748b",
                cursor="hand2"
            )
            header_label.grid(row=0, column=col, padx=(0, 40), sticky="w")
            header_label.bind("<Button-1>", lambda e, c=col: self.sort_table(c))
            header_frame.grid_columnconfigure(col, weight=1)
        
        separator = ctk.CTkFrame(self.table_frame, height=1, fg_color="#e2e8f0")
        separator.pack(fill="x", padx=20, pady=(0, 10))
        
        # Configure scroll region
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        content.bind("<Configure>", configure_scroll_region)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)

    def display_reservations(self, reservations=None):
        """Display reservations in the table"""
        # Clear existing rows
        for widget in self.table_frame.winfo_children()[2:]:
            widget.destroy()
        
        # Reset selection
        self.selected_row = None
        self.selected_reservation_id = None
        
        # Use filtered reservations if provided
        display_data = reservations if reservations is not None else self.reservations
        
        if not display_data:
            empty_frame = ctk.CTkFrame(self.table_frame, fg_color="white")
            empty_frame.pack(fill="x", padx=20, pady=40)
            
            ctk.CTkLabel(
                empty_frame,
                text="No reservations found",
                font=("Arial", 16),
                text_color="#64748b"
            ).pack()
            return
        
        for row, reservation in enumerate(display_data):
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="white")
            row_frame.pack(fill="x", padx=20, pady=10)
            row_frame.reservation_id = reservation["id"]
            row_frame.bind("<Button-1>", lambda e, f=row_frame: self.select_row(f))
            
            cell_values = [
                reservation["id"],
                reservation["name"],
                reservation["checkin"],
                reservation["amount"]
            ]
            
            for col, value in enumerate(cell_values):
                cell_label = ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=("Arial", 14),
                    text_color="#475569",
                    fg_color="white"
                )
                cell_label.grid(row=0, column=col, padx=(0, 40), sticky="w")
                row_frame.grid_columnconfigure(col, weight=1)
                cell_label.bind("<Button-1>", lambda e, f=row_frame: self.select_row(f))
            
            if row < len(display_data) - 1:
                separator = ctk.CTkFrame(self.table_frame, height=1, fg_color="#f1f5f9")
                separator.pack(fill="x", padx=20)

    def select_row(self, row_frame):
        """Select a row in the table"""
        if hasattr(self, 'selected_row') and self.selected_row:
            for widget in self.selected_row.winfo_children():
                widget.configure(fg_color="white")
            self.selected_row.configure(fg_color="white")
        
        row_frame.configure(fg_color="#e0f2fe")
        for widget in row_frame.winfo_children():
            widget.configure(fg_color="#e0f2fe")
        
        self.selected_row = row_frame
        self.selected_reservation_id = row_frame.reservation_id

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

    def sort_table(self, column_index):
        """Sort reservations by the selected column"""
        column_keys = ["id", "name", "checkin", "amount"]
        key = column_keys[column_index]
        
        if self.sort_column == column_index:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = column_index
            self.sort_descending = False
        
        if key == "checkin":
            def sort_key(x):
                try:
                    return datetime.strptime(x[key], "%b %d, %Y")
                except:
                    return datetime.min
        elif key == "amount":
            def sort_key(x):
                try:
                    return float(x[key].replace("$", "").replace(",", ""))
                except:
                    return 0.0
        else:
            def sort_key(x):
                return x[key].lower()
        
        sorted_reservations = sorted(
            self.reservations,
            key=sort_key,
            reverse=self.sort_descending
        )
        
        self.display_reservations(sorted_reservations)

    def add_reservation(self):
        """Open dialog to add a new reservation"""
        if not hasattr(self.controller, 'current_user') or self.controller.current_user is None:
            messagebox.showerror("Error", "User not logged in")
            self.controller.show_frame("LoginApp")
            return
            
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
        
        fields = [
            ("ID Number", "#", "id"),
            ("Guest Name", "Full name", "name"),
            ("Check-in Date", "MMM DD, YYYY", "checkin"),
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
            
            try:
                datetime.strptime(new_reservation["checkin"], "%b %d, %Y")
                float(new_reservation["amount"].replace("$", "").replace(",", ""))
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid format: {str(e)}")
                return
            
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
        if not hasattr(self.controller, 'current_user') or self.controller.current_user is None:
            messagebox.showerror("Error", "User not logged in")
            self.controller.show_frame("LoginApp")
            return
            
        if not hasattr(self, 'selected_reservation_id') or not self.selected_reservation_id:
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
            
            ctk.CTkLabel(
                frame,
                text=label,
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
            
            try:
                if "checkin" in updated_reservation:
                    datetime.strptime(updated_reservation["checkin"], "%b %d, %Y")
                if "amount" in updated_reservation:
                    float(updated_reservation["amount"].replace("$", "").replace(",", ""))
            except ValueError as e:
                messagebox.showerror("Error", f"Invalid format: {str(e)}")
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
        if not hasattr(self.controller, 'current_user') or self.controller.current_user is None:
            messagebox.showerror("Error", "User not logged in")
            self.controller.show_frame("LoginApp")
            return
            
        if not hasattr(self, 'selected_reservation_id') or not self.selected_reservation_id:
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
            self.selected_row = None
            self.selected_reservation_id = None
            messagebox.showinfo("Success", "Reservation deleted successfully")
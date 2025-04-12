import customtkinter as ctk
import json
import os
from tkinter import messagebox
from datetime import datetime

class HotelReservationsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Initialize data
        self.reservations = []
        self.load_data()
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create components
        self.create_sidebar()
        self.create_main_content()
    
    def load_data(self):
        """Load reservations data from JSON file"""
        try:
            if os.path.exists("reservations.json"):
                with open("reservations.json", "r") as f:
                    self.reservations = json.load(f)
            else:
                # Default data if file doesn't exist
                self.reservations = [
                    {"id": "#12345", "name": "Jack Smith", "checkin": "Jun 23, 2024", "amount": "$450.00"},
                    {"id": "#12346", "name": "Emily Johnson", "checkin": "Jun 22, 2024", "amount": "$500.00"},
                    {"id": "#12347", "name": "Michael Williams", "checkin": "Jun 21, 2024", "amount": "$400.00"},
                    {"id": "#12348", "name": "Sophia Brown", "checkin": "Jun 20, 2024", "amount": "$850.00"},
                    {"id": "#12349", "name": "Liam Davis", "checkin": "Jun 19, 2024", "amount": "$600.00"},
                    {"id": "#12350", "name": "Tim Cook", "checkin": "Jun 18, 2024", "amount": "$350.00"},
                    {"id": "#12351", "name": "Mark Zuckerberg", "checkin": "Jun 17, 2024", "amount": "$650.00"},
                    {"id": "#12352", "name": "Jack Dorsey", "checkin": "Jun 16, 2024", "amount": "$700.00"},
                    {"id": "#12353", "name": "Reed Hastings", "checkin": "Jun 15, 2024", "amount": "$300.00"},
                    {"id": "#12354", "name": "Brian Chesky", "checkin": "Jun 14, 2024", "amount": "$750.00"}
                ]
                self.save_data()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
    
    def save_data(self):
        """Save reservations data to JSON file"""
        try:
            with open("reservations.json", "w") as f:
                json.dump(self.reservations, f, indent=2)
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save data: {str(e)}")
    
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
            command=lambda: self.controller.show_frame("LoginApp")
        ).pack(fill="x")
    
    def create_main_content(self):
        """Create the main content area with reservations table"""
        # Main container
        main = ctk.CTkFrame(self, fg_color="white")
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        
        # ===== HEADER SECTION =====
        header_frame = ctk.CTkFrame(main, height=70, fg_color="white", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Create header with evenly spaced items
        header_frame.grid_columnconfigure(0, weight=0)  # Logo
        header_frame.grid_columnconfigure(1, weight=1)  # Nav Items (centered)
        header_frame.grid_columnconfigure(2, weight=0)  # Icons
        
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
        
        # Right side icons
        icons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        icons_frame.grid(row=0, column=2, padx=20, sticky="e")
        
        # Search, notification and profile icons
        search_icon = ctk.CTkLabel(icons_frame, text="🔍", font=("Arial", 20))
        search_icon.pack(side="left", padx=10)
        
        notification_icon = ctk.CTkLabel(icons_frame, text="🔔", font=("Arial", 20))
        notification_icon.pack(side="left", padx=10)
        
        profile_icon = ctk.CTkLabel(icons_frame, text="👤", font=("Arial", 20))
        profile_icon.pack(side="left", padx=10)
        
        # ===== SCROLLABLE CONTENT AREA =====
        # Create a canvas for scrolling
        canvas_frame = ctk.CTkFrame(main, fg_color="#f8fafc")
        canvas_frame.grid(row=1, column=0, sticky="nsew")
        canvas_frame.grid_rowconfigure(0, weight=1)
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Create canvas and scrollbar
        canvas = ctk.CTkCanvas(canvas_frame, bg="#f8fafc", highlightthickness=0)
        scrollbar = ctk.CTkScrollbar(canvas_frame, orientation="vertical", command=canvas.yview)
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Place canvas and scrollbar
        scrollbar.grid(row=0, column=1, sticky="ns")
        canvas.grid(row=0, column=0, sticky="nsew")
        canvas_frame.grid_columnconfigure(0, weight=1)
        
        # Create frame inside canvas to hold content
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
        
        # Action buttons frame (New, Edit, Delete)
        action_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        action_frame.pack(side="right")
        
        # New Reservation button
        new_btn = ctk.CTkButton(
            action_frame,
            text="New Reservation",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.add_reservation
        )
        new_btn.pack(side="left", padx=5)
        
        # Edit button
        edit_btn = ctk.CTkButton(
            action_frame,
            text="Edit",
            fg_color="#f59e0b",
            hover_color="#d97706",
            command=self.edit_reservation
        )
        edit_btn.pack(side="left", padx=5)
        
        # Delete button
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
        
        # Table headers with clickable sorting
        headers = ["ID Number", "Guest Name", "Check-in Date", "Total Booking Amount"]
        self.sort_column = None
        self.sort_descending = False
        
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
        
        # Add a separator line
        separator = ctk.CTkFrame(self.table_frame, height=1, fg_color="#e2e8f0")
        separator.pack(fill="x", padx=20, pady=(0, 10))
        
        # Display reservations
        self.display_reservations()
        
        # Configure scroll region and bindings
        def configure_scroll_region(event):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        content.bind("<Configure>", configure_scroll_region)
        
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        canvas.bind_all("<MouseWheel>", on_mousewheel)
        canvas.bind_all("<Button-4>", lambda e: canvas.yview_scroll(-1, "units"))
        canvas.bind_all("<Button-5>", lambda e: canvas.yview_scroll(1, "units"))
        
        def on_frame_configure(event):
            canvas.configure(width=event.width)
            canvas.itemconfig(canvas_window, width=event.width)
        
        canvas.bind("<Configure>", on_frame_configure)
    
    def display_reservations(self, reservations=None):
        """Display reservations in the table"""
        # Clear existing rows
        for widget in self.table_frame.winfo_children()[2:]:  # Skip header and separator
            widget.destroy()
        
        # Use filtered reservations if provided, otherwise use all
        display_data = reservations if reservations is not None else self.reservations
        
        for row, reservation in enumerate(display_data):
            row_frame = ctk.CTkFrame(self.table_frame, fg_color="white")
            row_frame.pack(fill="x", padx=20, pady=10)
            
            # Store reservation ID as a property of the row frame for selection
            row_frame.reservation_id = reservation["id"]
            
            # Make the row selectable
            row_frame.bind("<Button-1>", lambda e, f=row_frame: self.select_row(f))
            
            # Display reservation data
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
                    text_color="#475569"
                )
                cell_label.grid(row=0, column=col, padx=(0, 40), sticky="w")
                row_frame.grid_columnconfigure(col, weight=1)
            
            # Add a separator line except after the last row
            if row < len(display_data) - 1:
                separator = ctk.CTkFrame(self.table_frame, height=1, fg_color="#f1f5f9")
                separator.pack(fill="x", padx=20)
        
        # Reset selection
        self.selected_row = None
    
    def select_row(self, row_frame):
        """Select a row in the table"""
        # Reset previous selection
        if hasattr(self, 'selected_row') and self.selected_row:
            self.selected_row.configure(fg_color="white")
        
        # Set new selection
        row_frame.configure(fg_color="#e0f2fe")
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
        
        # If clicking the same column, reverse the sort order
        if self.sort_column == column_index:
            self.sort_descending = not self.sort_descending
        else:
            self.sort_column = column_index
            self.sort_descending = False
        
        # Special handling for dates and amounts
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
        
        self.reservations.sort(
            key=sort_key,
            reverse=self.sort_descending
        )
        
        self.save_data()
        self.display_reservations()
    
    def add_reservation(self):
        """Open dialog to add a new reservation"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Reservation")
        dialog.geometry("500x400")
        dialog.transient(self)
        dialog.grab_set()
        
        # Form fields
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
        
        # Action buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        def save():
            # Validate and save new reservation
            new_reservation = {}
            for key, entry in entries.items():
                value = entry.get().strip()
                if not value:
                    messagebox.showerror("Error", f"Please enter {key}")
                    return
                new_reservation[key] = value
            
            # Check for duplicate ID
            if any(r["id"] == new_reservation["id"] for r in self.reservations):
                messagebox.showerror("Error", "Reservation ID already exists")
                return
            
            self.reservations.append(new_reservation)
            self.save_data()
            self.display_reservations()
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
        if not hasattr(self, 'selected_reservation_id') or not self.selected_reservation_id:
            messagebox.showwarning("Warning", "Please select a reservation to edit")
            return
        
        # Find the selected reservation
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
        
        # Form fields
        fields = [
            ("ID Number", "id", False),  # ID shouldn't be editable
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
        
        # Action buttons
        button_frame = ctk.CTkFrame(dialog, fg_color="transparent")
        button_frame.pack(fill="x", padx=20, pady=20)
        
        def save():
            # Update reservation data
            for key, entry in entries.items():
                if entry.cget("state") != "disabled":
                    reservation[key] = entry.get().strip()
            
            self.save_data()
            self.display_reservations()
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
        if not hasattr(self, 'selected_reservation_id') or not self.selected_reservation_id:
            messagebox.showwarning("Warning", "Please select a reservation to delete")
            return
        
        # Confirm deletion
        if not messagebox.askyesno("Confirm", "Are you sure you want to delete this reservation?"):
            return
        
        # Find and remove the reservation
        for i, r in enumerate(self.reservations):
            if r["id"] == self.selected_reservation_id:
                del self.reservations[i]
                self.save_data()
                self.display_reservations()
                messagebox.showinfo("Success", "Reservation deleted successfully")
                return
        
        messagebox.showerror("Error", "Selected reservation not found")
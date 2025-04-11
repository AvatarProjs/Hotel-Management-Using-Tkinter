import customtkinter as ctk
import json
import os
from tkinter import messagebox
from datetime import datetime

class HotelReservationsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Initialize data
        self.reservations = []
        self.load_data()
        
        # Create components
        self.create_sidebar()
        self.create_main_content()
    
    def create_sidebar(self):
        self.sidebar = ctk.CTkFrame(self, width=250, fg_color="#f0f9ff", corner_radius=0)
        self.sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Navigation items
        nav_items = [
            ("Dashboard", "📊", "Dashboard"),
            ("Reservations", "🛒", "Reservations"),
            ("Customers", "👥", "Customers"),
            ("Reports", "📄", "Reports")
        ]
        
        # Add padding at the top
        padding = ctk.CTkLabel(self.sidebar, text="", fg_color="transparent")
        padding.pack(pady=(20, 10))
        
        for item, icon, view_name in nav_items:
            btn_frame = ctk.CTkFrame(
                self.sidebar, 
                fg_color="#dbeafe" if view_name == "Reservations" else "transparent", 
                corner_radius=8
            )
            btn_frame.view_name = view_name  # Store view name for reference
            btn_frame.pack(fill="x", padx=15, pady=5)
            
            # Container for icon and text
            content_frame = ctk.CTkFrame(btn_frame, fg_color="transparent")
            content_frame.pack(pady=8, padx=15, anchor="w")
            
            # Icon
            ctk.CTkLabel(
                content_frame,
                text=icon,
                font=("Arial", 16),
                text_color="#64748b"
            ).pack(side="left", padx=(0, 10))
            
            # Text (clickable)
            btn = ctk.CTkButton(
                content_frame,
                text=item,
                font=("Arial", 14),
                text_color="#64748b",
                fg_color="transparent",
                hover_color="#f0f9ff",  # Changed from "transparent" to a light blue color
                command=lambda v=view_name: self.controller.show_frame(f"Hotel{v}Page"),
                anchor="w",
                width=140
            )
            btn.pack(side="left")
            
            # Make entire frame clickable
            btn_frame.bind("<Button-1>", lambda e, v=view_name: self.controller.show_frame(f"Hotel{v}Page"))
            for child in btn_frame.winfo_children():
                child.bind("<Button-1>", lambda e, v=view_name: self.controller.show_frame(f"Hotel{v}Page"))
        
        # Add logout button
        logout_frame = ctk.CTkFrame(self.sidebar, fg_color="transparent")
        logout_frame.pack(side="bottom", fill="x", padx=15, pady=20)
        
        ctk.CTkButton(
            logout_frame,
            text="Logout",
            fg_color="#ef4444",
            text_color="white",
            command=lambda: self.controller.show_frame("LoginApp")
        ).pack(fill="x")
    
    def create_main_content(self):
        """Create main content area with header"""
        # Main container
        self.main_frame = ctk.CTkFrame(self, fg_color="white")
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)
        
        # Header section
        self.create_header()
        
        # Content frame
        self.content_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        self.content_frame.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # Add reservations content
        self.setup_reservations_ui()
    
    def create_header(self):
        """Create the header with navigation"""
        header_frame = ctk.CTkFrame(self.main_frame, height=70, fg_color="white", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        
        # Header layout
        header_frame.grid_columnconfigure(0, weight=0)  # Logo
        header_frame.grid_columnconfigure(1, weight=1)  # Nav Items
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
            ("Dashboard", "HotelDashboardPage"),
            ("Customers", "CustomerManagementScreen"),
            ("Reservations", "HotelReservationsPage"),
            ("Reports", "HotelReportsPage")
        ]
        
        nav_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        nav_frame.grid(row=0, column=1, sticky="")
        
        for item, view_name in nav_items:
            btn = ctk.CTkButton(
                nav_frame,
                text=item,
                fg_color="#3b82f6" if view_name == "HotelReservationsPage" else "transparent",
                text_color="white" if view_name == "HotelReservationsPage" else "#64748b",
                hover_color="#f0f0f0",  # This was already set to a valid color
                corner_radius=5,
                height=32,
                border_width=0,
                command=lambda v=view_name: self.controller.show_frame(v)
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
    
    def setup_reservations_ui(self):
        """Setup the reservations UI components"""
        # Title
        ctk.CTkLabel(
            self.content_frame,
            text="Reservations Management",
            font=("Arial", 20, "bold"),
            text_color="#2c3e50"
        ).pack(pady=(0, 20), anchor="w")
        
        # Action buttons
        action_frame = ctk.CTkFrame(self.content_frame, fg_color="transparent")
        action_frame.pack(fill="x", pady=(0, 20))
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            action_frame,
            placeholder_text="Search reservations...",
            width=300
        )
        self.search_entry.pack(side="left", padx=5)
        
        # Add reservation button
        add_btn = ctk.CTkButton(
            action_frame,
            text="+ Add Reservation",
            fg_color="#3b82f6",
            command=self.open_add_reservation_dialog
        )
        add_btn.pack(side="left", padx=5)
        
        # Filter buttons
        filter_frame = ctk.CTkFrame(action_frame, fg_color="transparent")
        filter_frame.pack(side="right")
        
        ctk.CTkButton(
            filter_frame,
            text="All",
            fg_color="#3b82f6",
            width=80
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Active",
            fg_color="#e2e8f0",
            text_color="#2c3e50",
            width=80
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Upcoming",
            fg_color="#e2e8f0",
            text_color="#2c3e50",
            width=80
        ).pack(side="left", padx=5)
        
        # Reservations table
        self.create_reservations_table()
    
    def create_reservations_table(self):
        """Create the reservations table"""
        # Table container
        table_frame = ctk.CTkFrame(self.content_frame, fg_color="white")
        table_frame.pack(fill="both", expand=True)
        
        # Table headers
        headers = ["ID", "Guest Name", "Check-In", "Amount", "Status", "Actions"]
        header_frame = ctk.CTkFrame(table_frame, fg_color="#f8fafc")
        header_frame.pack(fill="x", padx=0, pady=0)
        
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#64748b"
            ).grid(row=0, column=col, padx=10, pady=10, sticky="w")
            header_frame.grid_columnconfigure(col, weight=1 if col < len(headers)-1 else 0)
        
        # Separator
        ctk.CTkFrame(table_frame, height=1, fg_color="#e2e8f0").pack(fill="x")
        
        # Table content
        scrollable_frame = ctk.CTkScrollableFrame(table_frame, fg_color="white")
        scrollable_frame.pack(fill="both", expand=True)
        
        # Add sample data
        for reservation in self.reservations:
            self.add_reservation_row(scrollable_frame, reservation)
    
    def add_reservation_row(self, parent, reservation):
        """Add a single reservation row to the table"""
        row_frame = ctk.CTkFrame(parent, fg_color="white")
        row_frame.pack(fill="x", pady=5)
        
        # ID
        ctk.CTkLabel(
            row_frame,
            text=reservation["id"],
            font=("Arial", 12),
            text_color="#2c3e50"
        ).grid(row=0, column=0, padx=10, sticky="w")
        
        # Guest Name
        ctk.CTkLabel(
            row_frame,
            text=reservation["name"],
            font=("Arial", 12),
            text_color="#2c3e50"
        ).grid(row=0, column=1, padx=10, sticky="w")
        
        # Check-In
        ctk.CTkLabel(
            row_frame,
            text=reservation["checkin"],
            font=("Arial", 12),
            text_color="#2c3e50"
        ).grid(row=0, column=2, padx=10, sticky="w")
        
        # Amount
        ctk.CTkLabel(
            row_frame,
            text=reservation["amount"],
            font=("Arial", 12),
            text_color="#2c3e50"
        ).grid(row=0, column=3, padx=10, sticky="w")
        
        # Status
        status_frame = ctk.CTkFrame(
            row_frame,
            fg_color="#10b981",
            corner_radius=12
        )
        status_frame.grid(row=0, column=4, padx=10, sticky="w")
        ctk.CTkLabel(
            status_frame,
            text="Confirmed",
            font=("Arial", 10),
            text_color="white",
            padx=10,
            pady=2
        ).pack()
        
        # Actions
        action_frame = ctk.CTkFrame(row_frame, fg_color="transparent")
        action_frame.grid(row=0, column=5, padx=10, sticky="e")
        
        ctk.CTkButton(
            action_frame,
            text="Edit",
            width=60,
            height=25,
            fg_color="#3b82f6"
        ).pack(side="left", padx=2)
        
        ctk.CTkButton(
            action_frame,
            text="Cancel",
            width=60,
            height=25,
            fg_color="#ef4444"
        ).pack(side="left", padx=2)
        
        row_frame.grid_columnconfigure(5, weight=0)
    
    def open_add_reservation_dialog(self):
        """Open dialog to add new reservation"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Reservation")
        dialog.geometry("500x600")
        dialog.grab_set()
        
        # Form fields
        fields = [
            ("Guest Name", "text"),
            ("Check-In Date", "date"),
            ("Check-Out Date", "date"),
            ("Room Type", "combo"),
            ("Amount", "text"),
            ("Status", "combo")
        ]
        
        entries = {}
        
        for i, (label, field_type) in enumerate(fields):
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(frame, text=label).pack(anchor="w")
            
            if field_type == "text":
                entry = ctk.CTkEntry(frame)
                entry.pack(fill="x")
                entries[label] = entry
            elif field_type == "date":
                entry = ctk.CTkEntry(frame, placeholder_text="MM/DD/YYYY")
                entry.pack(fill="x")
                entries[label] = entry
            elif field_type == "combo":
                if label == "Room Type":
                    values = ["Standard", "Deluxe", "Suite", "Executive"]
                else:
                    values = ["Confirmed", "Pending", "Cancelled"]
                
                combo = ctk.CTkComboBox(frame, values=values)
                combo.pack(fill="x")
                entries[label] = combo
        
        # Submit button
        ctk.CTkButton(
            dialog,
            text="Add Reservation",
            command=lambda: self.add_reservation(entries, dialog)
        ).pack(pady=20)
    
    def add_reservation(self, entries, dialog):
        """Add new reservation to the system"""
        try:
            new_reservation = {
                "id": f"#{len(self.reservations) + 10000}",
                "name": entries["Guest Name"].get(),
                "checkin": entries["Check-In Date"].get(),
                "amount": f"${entries['Amount'].get()}",
                "status": entries["Status"].get()
            }
            
            if all(new_reservation.values()):
                self.reservations.append(new_reservation)
                self.save_data()
                dialog.destroy()
                messagebox.showinfo("Success", "Reservation added successfully!")
                # Refresh table
                self.setup_reservations_ui()
            else:
                messagebox.showerror("Error", "Please fill in all fields")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to add reservation: {str(e)}")
    
    def load_data(self):
        """Load reservations data from JSON file"""
        try:
            if os.path.exists("reservations.json"):
                with open("reservations.json", "r") as f:
                    self.reservations = json.load(f)
            else:
                # Default data if file doesn't exist
                self.reservations = [
                    {"id": "#12345", "name": "Jack Smith", "checkin": "Jun 23, 2024", "amount": "$450.00", "status": "Confirmed"},
                    {"id": "#12346", "name": "Emily Johnson", "checkin": "Jun 22, 2024", "amount": "$500.00", "status": "Confirmed"},
                    {"id": "#12347", "name": "Michael Williams", "checkin": "Jun 21, 2024", "amount": "$400.00", "status": "Confirmed"},
                    {"id": "#12348", "name": "Sophia Brown", "checkin": "Jun 20, 2024", "amount": "$850.00", "status": "Pending"},
                    {"id": "#12349", "name": "Liam Davis", "checkin": "Jun 19, 2024", "amount": "$600.00", "status": "Confirmed"}
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
import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HotelBookingDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create components
        self.create_sidebar()
        self.create_main_content()
    
    def create_sidebar(self):
        sidebar = ctk.CTkFrame(self, width=250, fg_color="#f0f9ff", corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Navigation buttons with explicit frame names
        nav_items = [
            ("Dashboard", "📊", "HotelBookingDashboard"),
            ("Reservations", "🛒", "HotelReservationsPage"),
            ("Customers", "👥", "CustomerManagementScreen"),
            ("Reports", "📄", "HotelReportsPage")
        ]
        
        # Add padding at the top
        padding = ctk.CTkLabel(sidebar, text="", fg_color="transparent")
        padding.pack(pady=(20, 10))
        
        for item, icon, frame_name in nav_items:
            # Determine if this is the active item
            is_active = frame_name == "HotelBookingDashboard"
            btn_color = "#dbeafe" if is_active else "transparent"
            
            btn_frame = ctk.CTkFrame(sidebar, fg_color=btn_color, corner_radius=8)
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
            
            # Text
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
            
        # Logout button at the bottom
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
        """Create the main content area with dashboard widgets"""
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
            text_color = "#3b82f6" if frame_name == "HotelBookingDashboard" else "#64748b"
            btn = ctk.CTkButton(
                nav_frame,
                text=item,
                fg_color="transparent",
                text_color=text_color,
                hover_color="#f0f0f0",
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
        
        # ===== CONTENT AREA =====
        content = ctk.CTkScrollableFrame(main, fg_color="#f8fafc")
        content.grid(row=1, column=0, sticky="nsew")
        
        # Welcome message
        welcome_frame = ctk.CTkFrame(content, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            welcome_frame,
            text="Good morning, User",
            font=("Arial", 20, "bold"),
            text_color="#2c3e50"
        ).pack(side="left")
        
        # ===== METRICS CARDS =====
        metrics_frame = ctk.CTkFrame(content, fg_color="transparent")
        metrics_frame.pack(fill="x", padx=20, pady=20)
        
        metrics = [
            ("$8,512", "Total bookings cost"),
            ("1,200", "Active customers"),
            ("4,000", "Total reservations"),
            ("6,000", "Total revenue")
        ]
        
        for value, label in metrics:
            card = ctk.CTkFrame(
                metrics_frame,
                fg_color="white",
                corner_radius=12,
                height=120
            )
            card.pack(side="left", expand=True, fill="both", padx=10)
            
            ctk.CTkLabel(
                card,
                text=value,
                font=("Arial", 24, "bold"),
                text_color="#2c3e50"
            ).pack(pady=(25, 5), padx=20, anchor="w")
            
            ctk.CTkLabel(
                card,
                text=label,
                font=("Arial", 14),
                text_color="#7f8c8d"
            ).pack(pady=(0, 20), padx=20, anchor="w")
        
        # ===== MONTHLY REVENUE GRAPH =====
        revenue_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        revenue_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            revenue_frame,
            text="Monthly revenue",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        ).pack(pady=(20, 15), padx=20, anchor="w")
        
        # Create matplotlib figure
        fig, ax = plt.subplots(figsize=(10, 3), dpi=100)
        months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul']
        revenue = [5000, 5500, 6200, 5800, 6500, 7000, 7500]
        
        ax.plot(months, revenue, color='#3b82f6', linewidth=2, marker='o')
        ax.fill_between(months, revenue, color='#3b82f6', alpha=0.1)
        ax.grid(axis='y', linestyle='--', alpha=0.7)
        ax.set_facecolor('white')
        fig.patch.set_facecolor('white')
        
        # Remove borders
        for spine in ax.spines.values():
            spine.set_visible(False)
        
        # Embed in Tkinter
        canvas = FigureCanvasTkAgg(fig, master=revenue_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill="x", padx=20, pady=(0, 20))
        
        # ===== QUICK ACCESS (SINGLE ROW) =====
        quick_access_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        quick_access_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            quick_access_frame,
            text="Quick access",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        ).pack(pady=(20, 15), padx=20, anchor="w")
        
        # Single row frame for all items
        row_frame = ctk.CTkFrame(quick_access_frame, fg_color="transparent")
        row_frame.pack(padx=20, pady=(0, 20), fill="x")
        
        quick_items = [
            ("👥", "Customers", "CustomerManagementScreen"),
            ("📅", "Reservations", "HotelReservationsPage"),
            ("📊", "Reports", "HotelReportsPage")
        ]
        
        for icon, title, frame_name in quick_items:
            card = ctk.CTkFrame(
                row_frame,
                fg_color="#f8fafc",
                corner_radius=12,
                height=100,
                width=200
            )
            card.pack(side="left", expand=True, fill="both", padx=10)
            
            # Icon and title row
            icon_frame = ctk.CTkFrame(card, fg_color="transparent")
            icon_frame.pack(pady=(15, 5), padx=15, anchor="w")
            
            ctk.CTkLabel(
                icon_frame,
                text=icon,
                font=("Arial", 20),
                text_color="#3b82f6"
            ).pack(side="left", padx=(0, 10))
            
            btn = ctk.CTkButton(
                icon_frame,
                text=title,
                font=("Arial", 14, "bold"),
                text_color="#2c3e50",
                fg_color="transparent",
                hover_color="#f0f0f0",
                command=lambda fn=frame_name: self.controller.show_frame(fn)
            )
            btn.pack(side="left")
            
            # Description
            ctk.CTkLabel(
                card,
                text=f"View and manage your {title.lower()}",
                font=("Arial", 12),
                text_color="#7f8c8d",
                anchor="w",
                justify="left"
            ).pack(pady=(0, 15), padx=15, fill="x")
        
        # ===== RECENT BOOKINGS =====
        bookings_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        bookings_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        ctk.CTkLabel(
            bookings_frame,
            text="Recent bookings",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        ).pack(pady=(20, 15), padx=20, anchor="w")
        
        # Table headers
        headers = ["ID Number", "Status", "Payment Status", "Fulfillment Status", "Total Amount"]
        
        # Create a frame to hold the header labels
        header_frame = ctk.CTkFrame(bookings_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20)
        
        for i in range(len(headers)):
            header_frame.grid_columnconfigure(i, weight=1)
        
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#7f8c8d"
            ).grid(row=0, column=col, padx=5, pady=5, sticky="ew")
        
        # Table data
        bookings = [
            ("#12345", "Paid", "Not paid", "Pending", "$450.00"),
            ("#12346", "Paid", "Not paid", "Pending", "$500.00"),
            ("#12347", "Paid", "Not paid", "Pending", "$400.00"),
            ("#12348", "Paid", "Not paid", "Pending", "$550.00"),
            ("#12349", "Paid", "Not paid", "Pending", "$600.00")
        ]
        
        for row, booking in enumerate(bookings, 1):
            row_frame = ctk.CTkFrame(
                bookings_frame,
                fg_color="#f8fafc" if row % 2 == 0 else "white"
            )
            row_frame.pack(fill="x", padx=20, pady=2)
            
            for i in range(len(booking)):
                row_frame.grid_columnconfigure(i, weight=1)
            
            for col, value in enumerate(booking):
                fg_color = "transparent"
                text_color = "#2c3e50"
                
                if (row == 1 or row == 2) and col == 1 and value == "Paid":
                    fg_color = "#3b82f6"
                    text_color = "white"
                elif row == 3 and col == 3 and value == "Pending":
                    fg_color = "#f59e0b"
                    text_color = "white"
                elif row == 4 and col == 2 and value == "Not paid":
                    fg_color = "#ef4444"
                    text_color = "white"
                elif row == 5 and col == 1 and value == "Paid":
                    fg_color = "#3b82f6"
                    text_color = "white"
                
                ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=("Arial", 12),
                    text_color=text_color,
                    fg_color=fg_color,
                    corner_radius=4,
                    padx=8,
                    pady=2
                ).grid(row=0, column=col, padx=5, sticky="ew")

    def update_user_display(self, user_data):
        """Update the display with user information"""
        # You can implement this to update the welcome message or other user-specific elements
        pass
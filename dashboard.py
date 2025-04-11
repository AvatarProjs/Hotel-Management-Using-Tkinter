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
        sidebar = ctk.CTkFrame(self, width=250, fg_color="white", corner_radius=0)
        sidebar.grid(row=0, column=0, sticky="nsew")
        
        # Sidebar content
        ctk.CTkLabel(
            sidebar, 
            text="Hotel Admin",
            font=("Arial", 18, "bold"),
            text_color="#2c3e50"
        ).pack(pady=(20, 30), padx=10)
        
        # Store references to all navigation buttons
        self.nav_buttons = []
        
        # Navigation buttons
        nav_items = ["Dashboard", "Customers", "Reservations", "Reports"]
        for item in nav_items:
            btn = ctk.CTkButton(
                sidebar,
                text=item,
                fg_color="#3b82f6" if item == "Dashboard" else "transparent",
                text_color="white" if item == "Dashboard" else "#2c3e50",
                anchor="w",
                height=40,
                corner_radius=8,
                hover=False,
                command=lambda x=item: self.on_nav_button_click(x)
            )
            btn.pack(fill="x", padx=10, pady=5)
            self.nav_buttons.append(btn)
        
        # Add logout button at bottom
        logout_btn = ctk.CTkButton(
            sidebar,
            text="Logout",
            fg_color="#ef4444",
            text_color="white",
            anchor="w",
            height=40,
            corner_radius=8,
            command=lambda: self.controller.show_frame("LoginApp")
        )
        logout_btn.pack(side="bottom", fill="x", padx=10, pady=20)
    
    def on_nav_button_click(self, button_name):
        # Update the selected button appearance
        for btn in self.nav_buttons:
            if btn.cget("text") == button_name:
                btn.configure(fg_color="#3b82f6", text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color="#2c3e50")
        
        # Route to the appropriate page
        if button_name == "Dashboard":
            self.controller.show_frame("HotelBookingDashboard")
        elif button_name == "Customers":
            self.controller.show_frame("CustomerManagementScreen")
        elif button_name == "Reservations":
            self.controller.show_frame("HotelReservationsPage")
        elif button_name == "Reports":
            self.controller.show_frame("HotelReportsPage")
    
    def create_main_content(self):
        # Main container
        main = ctk.CTkFrame(self, fg_color="#f5f7fa")
        main.grid(row=0, column=1, sticky="nsew")
        main.grid_rowconfigure(1, weight=1)
        main.grid_columnconfigure(0, weight=1)
        
        # ===== HEADER SECTION =====
        header_frame = ctk.CTkFrame(main, height=70, fg_color="white", corner_radius=0)
        header_frame.grid(row=0, column=0, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(0, weight=1)
        header_frame.grid_columnconfigure(2, weight=1)
        
        # Left side - Logo and Navigation
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=20, sticky="w")
        
        # Logo placeholder
        logo_label = ctk.CTkLabel(
            left_frame, 
            text="Hotel Management", 
            font=("Arial", 16, "bold"), 
            text_color="#2c3e50"
        )
        logo_label.pack(side="left", padx=(0, 20))
        
        # Center - Search bar
        search_entry = ctk.CTkEntry(
            header_frame, 
            placeholder_text="Search...", 
            width=300, 
            height=35,
            fg_color="#f0f0f0", 
            border_color="#d1d5db",
            border_width=1,
            corner_radius=8
        )
        search_entry.grid(row=0, column=1, padx=20)
        
        # Right side icons
        icons_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        icons_frame.grid(row=0, column=2, padx=20, sticky="e")
        
        # Notification and profile icons
        notification_icon = ctk.CTkButton(
            icons_frame, 
            text="🔔", 
            font=("Arial", 16),
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#f0f0f0",
            text_color="black"
        )
        notification_icon.pack(side="left", padx=10)
        
        profile_icon = ctk.CTkButton(
            icons_frame, 
            text="👤", 
            font=("Arial", 16),
            width=40,
            height=40,
            fg_color="transparent",
            hover_color="#f0f0f0",
            text_color="black"
        )
        profile_icon.pack(side="left", padx=10)
        
        # ===== CONTENT AREA =====
        content = ctk.CTkScrollableFrame(main, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew")
        
        # Welcome message
        welcome_frame = ctk.CTkFrame(content, fg_color="transparent")
        welcome_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        ctk.CTkLabel(
            welcome_frame,
            text="Good morning, Admin",
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
        
        # ===== QUICK ACCESS =====
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
            ("👥", "Customers", "Manage your customer profiles"),
            ("💳", "Cards", "View and manage your saved cards"),
            ("📅", "Reservations", "View and manage your reservations"),
            ("📊", "Reports", "View and manage your reports")
        ]
        
        for icon, title, desc in quick_items:
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
            
            ctk.CTkLabel(
                icon_frame,
                text=title,
                font=("Arial", 14, "bold"),
                text_color="#2c3e50"
            ).pack(side="left")
            
            # Description
            ctk.CTkLabel(
                card,
                text=desc,
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
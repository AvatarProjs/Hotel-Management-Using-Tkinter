import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class HotelBookingDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.user_data = None
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create components
        self.create_sidebar()
        self.create_main_content()
    
    def update_user_display(self, user_data):
        """Update UI with current user data"""
        self.user_data = user_data
        self.welcome_label.configure(text=f"Good morning, {user_data['full_name']}")
        self.profile_icon.configure(text=user_data['full_name'][0].upper())  # Show first initial
    
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
            command=self.logout
        )
        logout_btn.pack(side="bottom", fill="x", padx=10, pady=20)
    
    def logout(self):
        """Handle logout process"""
        self.controller.current_user = None
        self.controller.show_frame("LoginApp")
    
    def on_nav_button_click(self, button_name):
        # Update the selected button appearance
        for btn in self.nav_buttons:
            if btn.cget("text") == button_name:
                btn.configure(fg_color="#3b82f6", text_color="white")
            else:
                btn.configure(fg_color="transparent", text_color="#2c3e50")
        
        # Here you would add logic to switch between dashboard views
        # For now we'll just update the welcome message
        self.welcome_label.configure(text=f"{button_name} View - {self.user_data['full_name']}")
    
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
        
        # Left side - Welcome message
        left_frame = ctk.CTkFrame(header_frame, fg_color="transparent")
        left_frame.grid(row=0, column=0, padx=20, sticky="w")
        
        self.welcome_label = ctk.CTkLabel(
            left_frame, 
            text="Good morning", 
            font=("Arial", 16, "bold"), 
            text_color="#2c3e50"
        )
        self.welcome_label.pack(side="left", padx=(0, 20))
        
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
        
        # Notification icon
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
        
        # Profile icon (shows user initial)
        self.profile_icon = ctk.CTkButton(
            icons_frame, 
            text="👤", 
            font=("Arial", 16),
            width=40,
            height=40,
            fg_color="#3b82f6",
            hover_color="#2563eb",
            text_color="white",
            corner_radius=20
        )
        self.profile_icon.pack(side="left", padx=10)
        
        # ===== CONTENT AREA =====
        content = ctk.CTkScrollableFrame(main, fg_color="transparent")
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        
        # ===== METRICS CARDS =====
        metrics_frame = ctk.CTkFrame(content, fg_color="transparent")
        metrics_frame.pack(fill="x", pady=(0, 20))
        
        metrics = [
            ("$8,512", "Total bookings cost", "#3b82f6"),
            ("1,200", "Active customers", "#10b981"),
            ("4,000", "Total reservations", "#f59e0b"),
            ("6,000", "Total revenue", "#6366f1")
        ]
        
        for value, label, color in metrics:
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
                text_color=color
            ).pack(pady=(25, 5), padx=20, anchor="w")
            
            ctk.CTkLabel(
                card,
                text=label,
                font=("Arial", 14),
                text_color="#7f8c8d"
            ).pack(pady=(0, 20), padx=20, anchor="w")
        
        # ===== MONTHLY REVENUE GRAPH =====
        revenue_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        revenue_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            revenue_frame,
            text="Monthly Revenue",
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
        
        # ===== QUICK ACTIONS =====
        quick_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        quick_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            quick_frame,
            text="Quick Actions",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        ).pack(pady=(20, 15), padx=20, anchor="w")
        
        # Action buttons
        actions = [
            ("➕ New Booking", "#3b82f6"),
            ("👥 Add Customer", "#10b981"),
            ("📅 View Calendar", "#f59e0b"),
            ("📊 Generate Report", "#6366f1")
        ]
        
        action_frame = ctk.CTkFrame(quick_frame, fg_color="transparent")
        action_frame.pack(fill="x", padx=20, pady=(0, 20))
        
        for text, color in actions:
            btn = ctk.CTkButton(
                action_frame,
                text=text,
                fg_color=color,
                hover_color=self.darken_color(color, 0.2),
                height=40,
                corner_radius=8
            )
            btn.pack(side="left", expand=True, padx=10)
        
        # ===== RECENT BOOKINGS TABLE =====
        bookings_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        bookings_frame.pack(fill="x", pady=(0, 20))
        
        ctk.CTkLabel(
            bookings_frame,
            text="Recent Bookings",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        ).pack(pady=(20, 15), padx=20, anchor="w")
        
        # Table data
        bookings = [
            ["#1001", "Deluxe Suite", "2023-06-15", "$450", "Confirmed"],
            ["#1002", "Standard Room", "2023-06-16", "$200", "Pending"],
            ["#1003", "Executive Suite", "2023-06-17", "$380", "Confirmed"],
            ["#1004", "Family Room", "2023-06-18", "$320", "Cancelled"]
        ]
        
        # Create table header
        headers = ["Booking ID", "Room Type", "Date", "Price", "Status"]
        header_frame = ctk.CTkFrame(bookings_frame, fg_color="#f3f4f6")
        header_frame.pack(fill="x", padx=20, pady=(0, 5))
        
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#4b5563"
            ).grid(row=0, column=col, padx=10, pady=5, sticky="w")
            header_frame.grid_columnconfigure(col, weight=1)
        
        # Create table rows
        for row, booking in enumerate(bookings, 1):
            row_frame = ctk.CTkFrame(
                bookings_frame,
                fg_color="white",
                height=40
            )
            row_frame.pack(fill="x", padx=20, pady=2)
            
            for col, value in enumerate(booking):
                # Determine status color
                if col == 4:  # Status column
                    if value == "Confirmed":
                        text_color = "#10b981"
                    elif value == "Pending":
                        text_color = "#f59e0b"
                    else:
                        text_color = "#ef4444"
                else:
                    text_color = "#4b5563"
                
                ctk.CTkLabel(
                    row_frame,
                    text=value,
                    font=("Arial", 12),
                    text_color=text_color
                ).grid(row=0, column=col, padx=10, sticky="w")
                row_frame.grid_columnconfigure(col, weight=1)
    
    def darken_color(self, hex_color, factor=0.2):
        """Darken a hex color by a given factor"""
        hex_color = hex_color.lstrip('#')
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        darkened = tuple(max(0, int(channel * (1 - factor))) for channel in rgb)
        return f"#{darkened[0]:02x}{darkened[1]:02x}{darkened[2]:02x}"
    
    def __del__(self):
        """Clean up resources"""
        plt.close('all')  # Close matplotlib figures
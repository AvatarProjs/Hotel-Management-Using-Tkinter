import customtkinter as ctk
import json
import os
from tkinter import messagebox
from datetime import datetime

class HotelReportsPage(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Initialize data
        self.reports_data = self.load_data()
        
        # Configure grid layout
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)
        
        # Create components
        self.create_sidebar()
        self.create_main_content()
    
    def load_data(self):
        """Load reports data"""
        try:
            if os.path.exists("reports_data.json"):
                with open("reports_data.json", "r") as f:
                    return json.load(f)
            else:
                # Default data if file doesn't exist
                data = {
                    "new_customers": {
                        "Jul": 512,
                        "Aug": 580,
                        "Sep": 425,
                        "Oct": 620,
                        "Nov": 575,
                        "Dec": 430
                    },
                    "total_customers": {
                        "Jul": 4500,
                        "Aug": 4750,
                        "Sep": 4950,
                        "Oct": 5250,
                        "Nov": 5000,
                        "Dec": 5000
                    },
                    "new_customers_list": [
                        {"name": "George Smith", "email": "george@gmail.com", "phone": "123-456-7890", "signup_date": "November 1, 2024"},
                        {"name": "Sarah Brown", "email": "sarah@gmail.com", "phone": "234-567-8901", "signup_date": "November 2, 2024"},
                        {"name": "Michael Johnson", "email": "michael@gmail.com", "phone": "345-678-9012", "signup_date": "November 3, 2024"},
                        {"name": "Emily Davis", "email": "emily@gmail.com", "phone": "456-789-0123", "signup_date": "November 4, 2024"},
                        {"name": "Daniel Miller", "email": "daniel@gmail.com", "phone": "567-890-1234", "signup_date": "November 5, 2024"}
                    ],
                    "revenue_data": {
                        "Jul": 45000,
                        "Aug": 52000,
                        "Sep": 48000,
                        "Oct": 63000,
                        "Nov": 57000,
                        "Dec": 51000
                    },
                    "occupancy_data": {
                        "Jul": 78,
                        "Aug": 85,
                        "Sep": 72,
                        "Oct": 90,
                        "Nov": 82,
                        "Dec": 75
                    }
                }
                
                with open("reports_data.json", "w") as f:
                    json.dump(data, f, indent=2)
                return data
        except Exception as e:
            messagebox.showerror("Error", f"Failed to load data: {str(e)}")
            return {}
    
    def create_sidebar(self):
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
            is_active = frame_name == "HotelReportsPage"
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
        """Create the main content area with reports"""
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
            text="Customer Growth Reports",
            font=("Arial", 24, "bold"),
            text_color="#2c3e50"
        ).pack(side="left")
        
        # Action buttons frame (Generate Report, Export)
        action_frame = ctk.CTkFrame(title_frame, fg_color="transparent")
        action_frame.pack(side="right")
        
        # Generate Report button
        new_btn = ctk.CTkButton(
            action_frame,
            text="Generate Report",
            fg_color="#3b82f6",
            hover_color="#2563eb",
            command=self.generate_report
        )
        new_btn.pack(side="left", padx=5)
        
        # Export button
        export_btn = ctk.CTkButton(
            action_frame,
            text="Export Data",
            fg_color="#10b981",
            hover_color="#059669",
            command=self.export_data
        )
        export_btn.pack(side="left", padx=5)
        
        # Create metrics cards section
        self.create_metrics_cards(content)
        
        # Create customer list section
        self.create_customer_list(content)
        
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
    
    def create_metrics_cards(self, parent):
        """Create metrics cards for customer growth"""
        cards_frame = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30, pady=10)
        
        # Configure grid for two cards side by side
        cards_frame.grid_columnconfigure(0, weight=1)
        cards_frame.grid_columnconfigure(1, weight=1)
        
        # New Customers Card
        new_customers_card = ctk.CTkFrame(cards_frame, fg_color="white", corner_radius=12)
        new_customers_card.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        
        # Card title
        ctk.CTkLabel(
            new_customers_card,
            text="New Customers",
            font=("Arial", 16, "bold"),
            text_color="#475569"
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Growth percentage
        ctk.CTkLabel(
            new_customers_card,
            text="+12%",
            font=("Arial", 32, "bold"),
            text_color="#3b82f6"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Monthly bar chart for new customers
        months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        new_customer_data = self.reports_data["new_customers"]
        
        max_value = max(new_customer_data.values())
        
        for month in months:
            bar_frame = ctk.CTkFrame(new_customers_card, fg_color="transparent")
            bar_frame.pack(fill="x", padx=20, pady=5)
            
            # Month label
            ctk.CTkLabel(
                bar_frame,
                text=month,
                font=("Arial", 12),
                text_color="#64748b",
                width=30
            ).pack(side="left", padx=(0, 10))
            
            # Bar container
            bar_container = ctk.CTkFrame(bar_frame, height=10, fg_color="#e2e8f0", corner_radius=5)
            bar_container.pack(side="left", fill="x", expand=True)
            
            # Calculate width percentage
            width_percent = (new_customer_data[month] / max_value) * 100
            
            # Bar value
            bar = ctk.CTkFrame(bar_container, height=10, fg_color="#3b82f6", corner_radius=5)
            bar.place(relx=0, rely=0, relwidth=width_percent/100, relheight=1)
        
        # Total Customers Card
        total_customers_card = ctk.CTkFrame(cards_frame, fg_color="white", corner_radius=12)
        total_customers_card.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        
        # Card title
        ctk.CTkLabel(
            total_customers_card,
            text="Total Customers",
            font=("Arial", 16, "bold"),
            text_color="#475569"
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Total count
        ctk.CTkLabel(
            total_customers_card,
            text="5,000",
            font=("Arial", 32, "bold"),
            text_color="#3b82f6"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Simple line chart representation
        chart_frame = ctk.CTkFrame(total_customers_card, height=150, fg_color="transparent")
        chart_frame.pack(fill="x", padx=20, pady=(10, 20))
        
        # Create a simple visualization (just placeholder in this case)
        chart_canvas = ctk.CTkCanvas(chart_frame, height=150, bg="white", highlightthickness=0)
        chart_canvas.pack(fill="x")
        
        # Draw a simple line chart (just an example visualization)
        total_customer_data = self.reports_data["total_customers"]
        months = ["Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]
        
        # Calculate coordinates
        width = 400  # Assumed width
        height = 150
        padding = 30
        
        # Draw x-axis labels
        for i, month in enumerate(months):
            x = padding + (i * ((width - 2 * padding) / (len(months) - 1)))
            chart_canvas.create_text(x, height - 10, text=month, fill="#64748b", font=("Arial", 10))
        
        # Draw line chart
        points = []
        values = [total_customer_data[month] for month in months]
        min_value = min(values)
        max_value = max(values)
        value_range = max_value - min_value
        
        for i, month in enumerate(months):
            x = padding + (i * ((width - 2 * padding) / (len(months) - 1)))
            # Scale value to chart height
            y_value = total_customer_data[month]
            y = height - padding - ((y_value - min_value) / value_range) * (height - 2 * padding)
            points.append((x, y))
        
        # Draw the line
        for i in range(len(points) - 1):
            chart_canvas.create_line(
                points[i][0], points[i][1], 
                points[i+1][0], points[i+1][1],
                fill="#3b82f6", width=2
            )
        
        # Revenue and Occupancy cards
        cards_frame_2 = ctk.CTkFrame(parent, fg_color="transparent")
        cards_frame_2.pack(fill="x", padx=30, pady=10)
        
        # Configure grid for two cards side by side
        cards_frame_2.grid_columnconfigure(0, weight=1)
        cards_frame_2.grid_columnconfigure(1, weight=1)
        
        # Revenue Card
        revenue_card = ctk.CTkFrame(cards_frame_2, fg_color="white", corner_radius=12)
        revenue_card.grid(row=0, column=0, padx=(0, 10), pady=10, sticky="nsew")
        
        # Card title
        ctk.CTkLabel(
            revenue_card,
            text="Monthly Revenue",
            font=("Arial", 16, "bold"),
            text_color="#475569"
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Revenue value
        ctk.CTkLabel(
            revenue_card,
            text="$51,000",
            font=("Arial", 32, "bold"),
            text_color="#10b981"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Simple bar chart for revenue
        revenue_canvas = ctk.CTkCanvas(revenue_card, height=100, bg="white", highlightthickness=0)
        revenue_canvas.pack(fill="x", padx=20, pady=(10, 20))
        
        # Draw simple bar chart for revenue
        revenue_data = self.reports_data["revenue_data"]
        bar_width = width / len(months) * 0.6
        spacing = width / len(months)
        
        max_revenue = max(revenue_data.values())
        
        for i, month in enumerate(months):
            x = padding + (i * spacing)
            value = revenue_data[month]
            bar_height = (value / max_revenue) * (height - 2 * padding - 20)
            
            # Draw bar
            revenue_canvas.create_rectangle(
                x, height - padding - bar_height,
                x + bar_width, height - padding,
                fill="#10b981", outline=""
            )
            
            # Month label
            revenue_canvas.create_text(x + bar_width/2, height - 10, text=month, fill="#64748b", font=("Arial", 10))
        
        # Occupancy Card
        occupancy_card = ctk.CTkFrame(cards_frame_2, fg_color="white", corner_radius=12)
        occupancy_card.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="nsew")
        
        # Card title
        ctk.CTkLabel(
            occupancy_card,
            text="Occupancy Rate",
            font=("Arial", 16, "bold"),
            text_color="#475569"
        ).pack(anchor="w", padx=20, pady=(20, 10))
        
        # Occupancy value
        ctk.CTkLabel(
            occupancy_card,
            text="75%",
            font=("Arial", 32, "bold"),
            text_color="#f59e0b"
        ).pack(anchor="w", padx=20, pady=(0, 20))
        
        # Line chart for occupancy
        occupancy_canvas = ctk.CTkCanvas(occupancy_card, height=100, bg="white", highlightthickness=0)
        occupancy_canvas.pack(fill="x", padx=20, pady=(10, 20))
        
        # Draw line chart for occupancy
        occupancy_data = self.reports_data["occupancy_data"]
        occupancy_points = []
        
        for i, month in enumerate(months):
            x = padding + (i * ((width - 2 * padding) / (len(months) - 1)))
            y_value = occupancy_data[month]
            y = height - padding - (y_value / 100) * (height - 2 * padding - 20)
            occupancy_points.append((x, y))
            
            # Month label
            occupancy_canvas.create_text(x, height - 10, text=month, fill="#64748b", font=("Arial", 10))
        
        # Draw the line
        for i in range(len(occupancy_points) - 1):
            occupancy_canvas.create_line(
                occupancy_points[i][0], occupancy_points[i][1], 
                occupancy_points[i+1][0], occupancy_points[i+1][1],
                fill="#f59e0b", width=2
            )
            
            # Draw points
            occupancy_canvas.create_oval(
                occupancy_points[i][0] - 3, occupancy_points[i][1] - 3,
                occupancy_points[i][0] + 3, occupancy_points[i][1] + 3,
                fill="#f59e0b", outline=""
            )
        
        # Last point
        occupancy_canvas.create_oval(
            occupancy_points[-1][0] - 3, occupancy_points[-1][1] - 3,
            occupancy_points[-1][0] + 3, occupancy_points[-1][1] + 3,
            fill="#f59e0b", outline=""
        )
    
    def create_customer_list(self, parent):
        """Create list of new customers"""
        # Section title
        ctk.CTkLabel(
            parent,
            text="New Customers",
            font=("Arial", 18, "bold"),
            text_color="#2c3e50"
        ).pack(anchor="w", padx=30, pady=(30, 20))
        
        # Table container
        table_frame = ctk.CTkFrame(parent, fg_color="white", corner_radius=12)
        table_frame.pack(fill="x", padx=30, pady=(0, 30), anchor="n")
        
        # Table headers
        headers = ["Name", "Email", "Phone", "Sign-up Date"]
        header_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))
        
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 14, "bold"),
                text_color="#64748b"
            ).pack(side="left", expand=True, fill="x")
        
        # Add a separator line
        separator = ctk.CTkFrame(table_frame, height=1, fg_color="#e2e8f0")
        separator.pack(fill="x", padx=20, pady=(0, 10))
        
        # Display customer data
        customers = self.reports_data["new_customers_list"]
        
        for customer in customers:
            row_frame = ctk.CTkFrame(table_frame, fg_color="transparent")
            row_frame.pack(fill="x", padx=20, pady=10)
            
            # Display customer info
            ctk.CTkLabel(
                row_frame,
                text=customer["name"],
                font=("Arial", 14),
                text_color="#475569"
            ).pack(side="left", expand=True, fill="x")
            
            ctk.CTkLabel(
                row_frame,
                text=customer["email"],
                font=("Arial", 14),
                text_color="#475569"
            ).pack(side="left", expand=True, fill="x")
            
            ctk.CTkLabel(
                row_frame,
                text=customer["phone"],
                font=("Arial", 14),
                text_color="#475569"
            ).pack(side="left", expand=True, fill="x")
            
            ctk.CTkLabel(
                row_frame,
                text=customer["signup_date"],
                font=("Arial", 14),
                text_color="#475569"
            ).pack(side="left", expand=True, fill="x")
            
            # Add separator except after the last row
            if customer != customers[-1]:
                separator = ctk.CTkFrame(table_frame, height=1, fg_color="#f1f5f9")
                separator.pack(fill="x", padx=20)
    
    def generate_report(self):
        """Generate a detailed report"""
        messagebox.showinfo("Generate Report", "Report generation functionality would open a dialog with date range and report type options.")
    
    def export_data(self):
        """Export report data"""
        messagebox.showinfo("Export Data", "Export functionality would save the report data to CSV or Excel format.")
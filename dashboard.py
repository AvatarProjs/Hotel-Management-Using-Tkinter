import customtkinter as ctk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from db_helper import DatabaseManager
import tksheet


class HotelBookingDashboard(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.db = DatabaseManager()

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
            ("Reports", "📄", "HotelReportsPage"),
            ("Staff Members", "👨‍💼", "StaffMemberScreen"),
            ("Profile", "👤", "ProfilePage")
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
            ("Reports", "HotelReportsPage"),
            ("Staff Members", "StaffMemberScreen")
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

        # Get dynamic data from database
        total_bookings_cost = self.db.get_total_bookings_cost()
        active_customers = self.db.get_active_customers_count()
        total_reservations = self.db.get_total_reservations()

        metrics = [
            (f"${total_bookings_cost:,.2f}", "Total bookings cost"),
            (f"{active_customers:,}", "Active customers"),
            (f"{total_reservations:,}", "Total reservations"),
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

        # ===== SINGLE RECENT BOOKINGS SECTION =====
        bookings_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=12)
        bookings_frame.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Header
        header_frame = ctk.CTkFrame(bookings_frame, fg_color="white")
        header_frame.pack(fill="x", padx=20, pady=(20, 10))

        ctk.CTkLabel(
            header_frame,
            text="Recent bookings",
            font=("Arial", 16, "bold"),
            text_color="#2c3e50"
        ).pack(side="left")

        # Create the sheet with proper expansion
        self.sheet = tksheet.Sheet(
            bookings_frame,
            align="w",
            header_align="center",
            column_width=150,
            show_x_scrollbar=True,
            show_y_scrollbar=True,
            height=400
        )
        self.sheet.enable_bindings()
        self.sheet.pack(fill="both", expand=True, padx=20, pady=(0, 20))

        # Set headers
        headers = ["Booking ID", "Customer", "Check-In", "Check-Out", "Status", "Payment", "Amount"]
        self.sheet.headers(headers)

        # Sample data
        data = [
            ["HRK1001", "John Doe", "2023-05-15", "2023-05-20", "Confirmed", "Paid", "$450.00"],
            ["HRK1002", "Jane Smith", "2023-05-18", "2023-05-18", "Pending", "Pending", "$500.00"],
            ["HRK1003", "Robert Johnson", "2023-05-17", "2023-05-22", "Confirmed", "Paid", "$600.00"],
            ["HRK1004", "Emily Davis", "2023-05-18", "2023-05-21", "Cancelled", "Refunded", "$0.00"],
            ["HRK1005", "Michael Wilson", "2023-05-19", "2023-05-25", "Confirmed", "Pending", "$750.00"],
            ["HRK1006", "Sarah Brown", "2023-05-20", "2023-05-23", "Pending", "Pending", "$400.00"],
            ["HRK1007", "David Taylor", "2023-05-21", "2023-05-24", "Confirmed", "Paid", "$500.00"],
            ["HRK1008", "Lisa White", "2023-05-22", "2023-05-27", "Confirmed", "Paid", "$650.00"],
            ["HRK1009", "James Black", "2023-05-23", "2023-05-26", "Pending", "Pending", "$550.00"],
            ["HRK1010", "Olivia Green", "2023-05-24", "2023-05-28", "Confirmed", "Pending", "$700.00"]
        ]
        self.sheet.set_sheet_data(data)

        # Configure column widths
        self.sheet.column_width(column=0, width=100)  # Booking ID
        self.sheet.column_width(column=1, width=150)  # Customer
        self.sheet.column_width(column=2, width=100)  # Check-In
        self.sheet.column_width(column=3, width=100)  # Check-Out
        self.sheet.column_width(column=4, width=100)  # Status
        self.sheet.column_width(column=5, width=100)  # Payment
        self.sheet.column_width(column=6, width=100)  # Amount

        # Apply formatting
        self.format_table()

    def format_table(self):
        """Apply enhanced formatting and colors to the table"""
        for r, row in enumerate(self.sheet.get_sheet_data()):
            status = row[4]  # Status column
            payment = row[5]  # Payment column

            # Default colors
            bg = "#ffffff"
            fg = "#2c3e50"
            status_bg = "#ffffff"
            status_fg = fg

            # Apply colors based on status
            if status == "Confirmed":
                status_bg = "#d4edda"  # Light green
                status_fg = "#155724"  # Dark green
            elif status == "Pending":
                status_bg = "#fff3cd"  # Light yellow
                status_fg = "#856404"  # Dark yellow
            elif status == "Cancelled":
                status_bg = "#f8d7da"  # Light red
                status_fg = "#721c24"  # Dark red

            # Apply row background color
            if r % 2 == 0:  # Alternate row colors
                bg = "#f8f9fa"  # Very light gray
            else:
                bg = "#ffffff"  # White

            # Apply payment status colors
            if payment == "Paid":
                payment_bg = "#d4edda"  # Light green
                payment_fg = "#155724"  # Dark green
            elif payment == "Pending":
                payment_bg = "#fff3cd"  # Light yellow
                payment_fg = "#856404"  # Dark yellow
            elif payment == "Refunded":
                payment_bg = "#f8d7da"  # Light red
                payment_fg = "#721c24"  # Dark red

            # Apply formatting to all cells in row
            self.sheet.highlight_cells(
                row=r,
                bg=bg,
                fg=fg,
                canvas="table"
            )

            # Apply specific formatting to status cell
            self.sheet.highlight_cells(
                row=r,
                column=4,
                bg=status_bg,
                fg=status_fg,
                canvas="table"
            )

            # Apply specific formatting to payment cell
            self.sheet.highlight_cells(
                row=r,
                column=5,
                bg=payment_bg,
                fg=payment_fg,
                canvas="table"
            )

    def update_user_display(self, user_data):
        """Update the display with user information"""
        pass
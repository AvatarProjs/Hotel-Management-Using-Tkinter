import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
from db_helper import DatabaseManager

class CustomerManagementScreen(ctk.CTkFrame):
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
        
        # Load initial data
        self.filter_customers("all")
    
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
            is_active = frame_name == "CustomerManagementScreen"
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
        """Create the main content area with customer management"""
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
        content = ctk.CTkScrollableFrame(main, fg_color="#f8fafc")
        content.grid(row=1, column=0, sticky="nsew", padx=20, pady=20)
        content.grid_columnconfigure(0, weight=1)
        
        # Search and filter section
        search_filter_frame = ctk.CTkFrame(content, fg_color="transparent")
        search_filter_frame.grid(row=0, column=0, sticky="ew", pady=(0, 20))
        search_filter_frame.grid_columnconfigure(0, weight=1)
        search_filter_frame.grid_columnconfigure(1, weight=0)
        
        # Search entry
        self.search_entry = ctk.CTkEntry(
            search_filter_frame,
            placeholder_text="Search customers...",
            width=300
        )
        self.search_entry.grid(row=0, column=0, sticky="w")
        self.search_entry.bind("<KeyRelease>", self.search_customers)
        
        # Add customer button
        ctk.CTkButton(
            search_filter_frame,
            text="+ Add Customer",
            fg_color="#3b82f6",
            command=self.open_add_customer_dialog,
            width=120
        ).grid(row=0, column=1, padx=(10, 0))
        
        # Filter buttons
        filter_frame = ctk.CTkFrame(content, fg_color="transparent")
        filter_frame.grid(row=1, column=0, sticky="w", pady=(0, 20))
        
        self.active_filter = tk.StringVar(value="all")
        
        ctk.CTkButton(
            filter_frame,
            text="All",
            fg_color="#3b82f6" if self.active_filter.get() == "all" else "#e2e8f0",
            text_color="white" if self.active_filter.get() == "all" else "#2c3e50",
            command=lambda: self.filter_customers("all"),
            width=80,
            height=30
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Active",
            fg_color="#3b82f6" if self.active_filter.get() == "active" else "#e2e8f0",
            text_color="white" if self.active_filter.get() == "active" else "#2c3e50",
            command=lambda: self.filter_customers("active"),
            width=80,
            height=30
        ).pack(side="left", padx=5)
        
        ctk.CTkButton(
            filter_frame,
            text="Inactive",
            fg_color="#3b82f6" if self.active_filter.get() == "inactive" else "#e2e8f0",
            text_color="white" if self.active_filter.get() == "inactive" else "#2c3e50",
            command=lambda: self.filter_customers("inactive"),
            width=80,
            height=30
        ).pack(side="left", padx=5)
        
        # Customer table
        self.table_frame = ctk.CTkFrame(content, fg_color="white", corner_radius=10)
        self.table_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 20))
        
        # Table headers
        headers = ["ID", "Name", "Email", "Address", "Phone", "Status", "Actions"]
        header_frame = ctk.CTkFrame(self.table_frame, fg_color="white")
        header_frame.pack(fill="x", padx=15, pady=(15, 10))
        
        for col, header in enumerate(headers):
            ctk.CTkLabel(
                header_frame,
                text=header,
                font=("Arial", 12, "bold"),
                text_color="#64748b"
            ).grid(row=0, column=col, padx=5, pady=5, sticky="w")
            header_frame.grid_columnconfigure(col, weight=1 if col < len(headers)-1 else 0)
        
        # Separator
        ctk.CTkFrame(self.table_frame, height=2, fg_color="#e2e8f0").pack(fill="x", padx=15)
        
        # Table content frame
        self.table_content = ctk.CTkFrame(self.table_frame, fg_color="white")
        self.table_content.pack(fill="both", expand=True, padx=15, pady=10)
    
    def populate_table(self, customers):
        """Populate the table with customer data"""
        # Clear existing rows
        for widget in self.table_content.winfo_children():
            widget.destroy()
        
        if not customers:
            # Show message if no customers found
            ctk.CTkLabel(
                self.table_content,
                text="No customers found",
                text_color="#64748b",
                font=("Arial", 12)
            ).pack(pady=20)
            return
        
        # Add customer rows
        for row, customer in enumerate(customers):
            row_frame = ctk.CTkFrame(self.table_content, fg_color="white")
            row_frame.pack(fill="x", pady=5)
            
            # Display customer data
            for col, field in enumerate(["customer_id", "full_name", "email", "address", "phone", "status"]):
                value = customer[field]
                if field == "status":  # Status column
                    status_frame = ctk.CTkFrame(
                        row_frame,
                        fg_color="#10b981" if value == "Active" else "#ef4444",
                        corner_radius=12,
                        width=80,
                        height=25
                    )
                    status_frame.grid(row=0, column=col, padx=5, sticky="w")
                    status_frame.grid_propagate(False)
                    
                    ctk.CTkLabel(
                        status_frame,
                        text=value,
                        font=("Arial", 10),
                        text_color="white"
                    ).place(relx=0.5, rely=0.5, anchor="center")
                else:
                    ctk.CTkLabel(
                        row_frame,
                        text=value,
                        font=("Arial", 12),
                        text_color="#334155"
                    ).grid(row=0, column=col, padx=5, sticky="w")
                
                row_frame.grid_columnconfigure(col, weight=1 if col < 5 else 0)
            
            # Action buttons
            action_frame = ctk.CTkFrame(row_frame, fg_color="white")
            action_frame.grid(row=0, column=6, padx=5, sticky="e")
            
            # Edit button
            edit_btn = ctk.CTkButton(
                action_frame,
                text="Edit",
                fg_color="#3b82f6",
                text_color="white",
                width=60,
                height=25,
                command=lambda c=customer: self.edit_customer(c)
            )
            edit_btn.pack(side="left", padx=2)
            
            # Delete button
            delete_btn = ctk.CTkButton(
                action_frame,
                text="Delete",
                fg_color="#ef4444",
                text_color="white",
                width=60,
                height=25,
                command=lambda c=customer: self.delete_customer(c)
            )
            delete_btn.pack(side="left", padx=2)
    
    def filter_customers(self, status):
        """Filter customers by status"""
        self.active_filter.set(status)
        customers = self.db.get_customers(status)
        self.populate_table(customers)
    
    def search_customers(self, event):
        """Search customers based on input"""
        query = self.search_entry.get().strip()
        
        if not query:
            self.filter_customers(self.active_filter.get())
            return
        
        customers = self.db.search_customers(query)
        self.populate_table(customers)
    
    def open_add_customer_dialog(self):
        """Open dialog to add new customer"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Add New Customer")
        dialog.geometry("500x500")
        dialog.grab_set()
        
        # Form fields
        fields = [
            ("ID Number", "text", ""),
            ("Name", "text", ""),
            ("Email", "text", ""),
            ("Address", "text", ""),
            ("Contact Number", "text", ""),
            ("Status", "combobox", "Active")
        ]
        
        self.setup_customer_form(dialog, fields, self.add_customer, "Add Customer")
    
    def edit_customer(self, customer):
        """Open dialog to edit existing customer"""
        dialog = ctk.CTkToplevel(self)
        dialog.title("Edit Customer")
        dialog.geometry("500x500")
        dialog.grab_set()
        
        # Form fields with existing data
        fields = [
            ("ID Number", "text", customer['customer_id']),
            ("Name", "text", customer['full_name']),
            ("Email", "text", customer['email']),
            ("Address", "text", customer['address']),
            ("Contact Number", "text", customer['phone']),
            ("Status", "combobox", customer['status'])
        ]
        
        self.setup_customer_form(dialog, fields, 
                               lambda entries, dlg: self.update_customer(customer['customer_id'], entries, dlg), 
                               "Update Customer")
    
    def setup_customer_form(self, dialog, fields, submit_action, submit_text):
        """Helper method to setup customer form"""
        entries = {}
        
        for label, field_type, default_value in fields:
            frame = ctk.CTkFrame(dialog, fg_color="transparent")
            frame.pack(fill="x", padx=20, pady=10)
            
            ctk.CTkLabel(frame, text=label).pack(anchor="w")
            
            if field_type == "text":
                entry = ctk.CTkEntry(frame)
                if default_value:
                    entry.insert(0, default_value)
                entry.pack(fill="x")
                entries[label] = entry
            elif field_type == "combobox":
                combo = ctk.CTkComboBox(frame, values=["Active", "Inactive"])
                combo.set(default_value)
                combo.pack(fill="x")
                entries[label] = combo
        
        # Submit button
        submit_btn = ctk.CTkButton(
            dialog,
            text=submit_text,
            command=lambda: submit_action(entries, dialog)
        )
        submit_btn.pack(pady=20)
    
    def add_customer(self, entries, dialog):
        """Add new customer to database"""
        customer_data = {
            'customer_id': entries["ID Number"].get(),
            'full_name': entries["Name"].get(),
            'email': entries["Email"].get(),
            'address': entries["Address"].get(),
            'phone': entries["Contact Number"].get(),
            'status': entries["Status"].get()
        }
        
        if not all(customer_data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self.db.add_customer(customer_data):
            messagebox.showinfo("Success", "Customer added successfully!")
            self.filter_customers(self.active_filter.get())
            dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to add customer")
    
    def update_customer(self, customer_id, entries, dialog):
        """Update existing customer in database"""
        updated_data = {
            'full_name': entries["Name"].get(),
            'email': entries["Email"].get(),
            'address': entries["Address"].get(),
            'phone': entries["Contact Number"].get(),
            'status': entries["Status"].get()
        }
        
        if not all(updated_data.values()):
            messagebox.showerror("Error", "Please fill in all fields")
            return
        
        if self.db.update_customer(customer_id, updated_data):
            messagebox.showinfo("Success", "Customer updated successfully!")
            self.filter_customers(self.active_filter.get())
            dialog.destroy()
        else:
            messagebox.showerror("Error", "Failed to update customer")
    
    def delete_customer(self, customer):
        """Delete customer from database"""
        if messagebox.askyesno("Confirm", f"Delete customer {customer['full_name']}?"):
            if self.db.delete_customer(customer['customer_id']):
                messagebox.showinfo("Success", "Customer deleted")
                self.filter_customers(self.active_filter.get())
            else:
                messagebox.showerror("Error", "Failed to delete customer")
    
    def __del__(self):
        """Clean up database connection when frame is destroyed"""
        if hasattr(self, 'db'):
            self.db.close()
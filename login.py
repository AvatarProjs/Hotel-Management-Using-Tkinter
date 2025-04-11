import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter
import tkinter.messagebox as messagebox
import hashlib
import re

class LoginApp(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure window
        self.configure(fg_color="#f0f8ff")  
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Background Image
        try:
            bg_image = Image.open("login_bg.jpg")
            bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)
            blurred_bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=5))
            self.bg_photo = ImageTk.PhotoImage(blurred_bg_image)
            self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Background image error: {e}")

        # Main login frame
        self.main_frame = ctk.CTkFrame(self, 
                                     corner_radius=22, 
                                     fg_color="white", 
                                     bg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.6)

        # Login title
        self.login_title = ctk.CTkLabel(self.main_frame, 
                                      text="Welcome Back", 
                                      font=("Arial", 32, "bold"), 
                                      text_color="#3b82f6")
        self.login_title.pack(pady=(30, 20))

        # Email Entry
        email_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        email_frame.pack(fill="x", padx=40)

        ctk.CTkLabel(email_frame, text="Email:", font=("Arial", 12, "bold")).pack(anchor="w")
        self.email_entry = ctk.CTkEntry(email_frame, 
                                      placeholder_text="Enter your email", 
                                      width=300,
                                      height=40,
                                      corner_radius=22,
                                      border_color="#d1d5db",
                                      border_width=1)
        self.email_entry.pack(fill="x", pady=(0, 10))

        # Password Entry
        password_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        password_frame.pack(fill="x", padx=40)

        ctk.CTkLabel(password_frame, text="Password:", font=("Arial", 12, "bold")).pack(anchor="w")
        
        self.password_container = ctk.CTkFrame(password_frame, fg_color="white")
        self.password_container.pack(fill="x")

        self.password_entry = ctk.CTkEntry(self.password_container,
                                         placeholder_text="Enter your password",
                                         show="*",
                                         width=300,
                                         height=40,
                                         corner_radius=22,
                                         border_color="#d1d5db",
                                         border_width=1)
        self.password_entry.pack(side="left", expand=True, fill="x")

        self.show_password_btn = ctk.CTkButton(self.password_container,
                                             text="👁",
                                             width=40,
                                             height=40,
                                             fg_color="#f0f0f0",
                                             hover_color="#e0e0e0",
                                             text_color="black",
                                             command=self.toggle_password)
        self.show_password_btn.pack(side="right", padx=(5, 0))

        # Remember Me Checkbox
        self.remember_me = ctk.CTkCheckBox(self.main_frame, 
                                         text="Remember me",
                                         font=("Arial", 10))
        self.remember_me.pack(pady=10)

        # Login Button
        self.login_button = ctk.CTkButton(self.main_frame, 
                                        text="Login", 
                                        width=350, 
                                        height=40, 
                                        corner_radius=22, 
                                        fg_color="#3b82f6", 
                                        hover_color="#2563eb",
                                        command=self.attempt_login)
        self.login_button.pack(pady=10)

        # Additional Links
        links_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        links_frame.pack(pady=10)

        self.forgot_password_link = ctk.CTkLabel(links_frame, 
                                               text="Forgot password?", 
                                               font=("Arial", 10, "bold"), 
                                               text_color="#3b82f6",
                                               cursor="hand2")
        self.forgot_password_link.pack()
        self.forgot_password_link.bind("<Button-1>", lambda e: print("Password recovery clicked"))

        self.register_link = ctk.CTkLabel(links_frame, 
                                        text="Don't have an account? Register", 
                                        font=("Arial", 10, "bold"), 
                                        text_color="#3b82f6",
                                        cursor="hand2")
        self.register_link.pack(pady=(5, 0))
        self.register_link.bind("<Button-1>", lambda e: self.controller.show_frame("RegistrationApp"))

        # Footer
        self.footer_label = ctk.CTkLabel(self.main_frame, 
                                       text="© 2024 Hotel Management System", 
                                       font=("Arial", 8, "bold"), 
                                       text_color="#6b7280")
        self.footer_label.pack(pady=(20, 10))

        # Bind Enter key to login
        self.bind('<Return>', lambda event: self.attempt_login())

    def toggle_password(self):
        """Toggle password visibility"""
        current_show = self.password_entry.cget("show")
        self.password_entry.configure(show="" if current_show == "*" else "*")
        self.show_password_btn.configure(text="🔒" if current_show == "*" else "👁")

    def attempt_login(self, event=None):
        """Handle login attempt with database verification"""
        email = self.email_entry.get().strip()
        password = self.password_entry.get()

        if not email or not password:
            messagebox.showerror("Error", "Please fill in all fields")
            return

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Please enter a valid email address")
            return

        try:
            # Pass the raw password directly to authenticate_user
            # The method will handle the hashing internally
            user = self.controller.db.authenticate_user(email, password)
            
            if user:
                messagebox.showinfo("Success", f"Welcome back, {user['full_name']}!")
                self.controller.successful_login(user)
                
                # Clear fields after successful login
                self.email_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
            else:
                messagebox.showerror("Error", "Invalid email or password")
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Login failed: {str(e)}")

    def __del__(self):
        """Clean up resources"""
        pass
import customtkinter as ctk
from PIL import Image, ImageTk, ImageFilter
import re
import tkinter.messagebox as messagebox
import mysql.connector
from dotenv import load_dotenv
import os
import hashlib

class RegistrationApp(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        
        # Configure window
        self.configure(fg_color="#f0f8ff")  
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Load environment variables
        load_dotenv()

        # Background Image
        try:
            bg_image = Image.open("registration.jpg") 
            bg_image = bg_image.resize((1920, 1080), Image.LANCZOS)
            blurred_bg_image = bg_image.filter(ImageFilter.GaussianBlur(radius=5))
            self.bg_photo = ImageTk.PhotoImage(blurred_bg_image)
            self.bg_label = ctk.CTkLabel(self, image=self.bg_photo, text="")
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        except Exception as e:
            print(f"Error loading background image: {e}")

        # Main registration frame
        self.main_frame = ctk.CTkFrame(self, 
                                     corner_radius=22, 
                                     fg_color="white", 
                                     bg_color="transparent")
        self.main_frame.place(relx=0.5, rely=0.5, anchor="center", relwidth=0.4, relheight=0.8)

        # Registration title
        self.reg_title = ctk.CTkLabel(self.main_frame, 
                                     text="Register", 
                                     font=("Arial", 32, "bold"), 
                                     text_color="blue")
        self.reg_title.pack(pady=(30, 20))

        # Full Name Entry
        full_name_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        full_name_frame.pack(fill="x", padx=40)

        ctk.CTkLabel(full_name_frame, text="Full name:", font=("Arial", 12, "bold"), anchor="w").pack(anchor="w", side="top")
        self.name_entry = ctk.CTkEntry(full_name_frame, 
                               placeholder_text="Full name", 
                               width=600, 
                               height=40, 
                               corner_radius=22,
                               border_color="lightblue",
                               border_width=1)
        self.name_entry.pack(anchor="w", pady=(0, 10))

        # Email Entry
        email_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        email_frame.pack(fill="x", padx=40)

        ctk.CTkLabel(email_frame, text="Email:", font=("Arial", 12, "bold"), anchor="w").pack(anchor="w", side="top")
        self.email_entry = ctk.CTkEntry(email_frame, 
                                placeholder_text="Email", 
                                width=600, 
                                height=40, 
                                corner_radius=22,
                                border_color="lightblue",
                                border_width=1)
        self.email_entry.pack(anchor="w", pady=(0, 5))

        self.email_error_label = ctk.CTkLabel(self.main_frame, 
                                     text="", 
                                     font=("Arial", 10), 
                                     text_color="red")
        self.email_error_label.pack(anchor="w", padx=40)

        # ctk.CTkLabel(self.main_frame, 
        #      text="You'll need to confirm this email later", 
        #      font=("Arial", 10), 
        #      text_color="gray").pack(anchor="w", padx=40)

        # Gender Entry
        gender_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        gender_frame.pack(fill="x", padx=40)

        ctk.CTkLabel(gender_frame, text="Gender:", font=("Arial", 12, "bold"), anchor="w").pack(anchor="w", side="top")
        self.gender_var = ctk.StringVar(value="Male")
        ctk.CTkRadioButton(gender_frame, text="Male", variable=self.gender_var, value="Male").pack(anchor="w", side="left", padx=5)
        ctk.CTkRadioButton(gender_frame, text="Female", variable=self.gender_var, value="Female").pack(anchor="w", side="left", padx=5)
        ctk.CTkRadioButton(gender_frame, text="Other", variable=self.gender_var, value="Other").pack(anchor="w", side="left", padx=5)

        # Password Entry
        password_frame = ctk.CTkFrame(self.main_frame, fg_color="white")
        password_frame.pack(fill="x", padx=40)

        ctk.CTkLabel(password_frame, text="Password:", font=("Arial", 12, "bold"), anchor="w").pack(anchor="w", side="top")
        self.password_entry = ctk.CTkEntry(password_frame, 
                                   placeholder_text="Password", 
                                   width=600, 
                                   height=40, 
                                   corner_radius=22,
                                   border_color="lightblue",
                                   border_width=1,
                                   show="*")
        self.password_entry.pack(anchor="w", pady=(0, 5))

        self.password_strength_label = ctk.CTkLabel(self.main_frame, 
                                           text="", 
                                           font=("Arial", 10), 
                                           text_color="red")
        self.password_strength_label.pack(anchor="w", padx=40)

        # Password visibility toggle
        self.show_password_var = ctk.BooleanVar(value=False)
        ctk.CTkCheckBox(password_frame, 
                        text="Show password", 
                        variable=self.show_password_var,
                        command=self.toggle_password_visibility).pack(anchor="w", pady=(0, 10))

        # Terms Checkbox
        self.terms_checkbox = ctk.CTkCheckBox(self.main_frame, 
                                              text="Agree to Terms of Service and Privacy Policy", 
                                              font=("Arial", 10))
        self.terms_checkbox.pack(pady=10)

        # Register Button
        self.register_button = ctk.CTkButton(self.main_frame, 
                                             text="Register", 
                                             width=350, 
                                             height=40, 
                                             corner_radius=22, 
                                             fg_color="blue", 
                                             hover_color="darkblue",
                                             command=self.register_user)
        self.register_button.pack(pady=10)

        # Sign In Link
        self.signin_link = ctk.CTkLabel(self.main_frame, 
                                        text="Already have an account? Sign in", 
                                        font=("Arial", 10, "bold"), 
                                        text_color="blue",
                                        cursor="hand2")
        self.signin_link.pack(pady=(10, 20))
        self.signin_link.bind("<Button-1>", lambda e: self.controller.show_frame("LoginApp"))

        # Footer
        self.footer_label = ctk.CTkLabel(self.main_frame, 
                                 text="© 2024 Sample University, Spring 2025", 
                                 font=("Arial", 8, "bold"), 
                                 text_color="black")
        self.footer_label.pack(pady=(20, 10))

        # Bind validation events
        self.email_entry.bind("<FocusOut>", self.validate_email)
        self.password_entry.bind("<KeyRelease>", self.check_password_strength)

    def validate_email(self, event=None):
        email = self.email_entry.get()
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            self.email_error_label.configure(text="Please enter a valid email address")
            return False
        self.email_error_label.configure(text="")
        return True

    def check_password_strength(self, event=None):
        password = self.password_entry.get()
        if len(password) == 0:
            self.password_strength_label.configure(text="")
            return
        
        strength = 0
        feedback = []
        
        if len(password) >= 8:
            strength += 1
        else:
            feedback.append("at least 8 characters")
            
        if re.search(r"[A-Z]", password):
            strength += 1
        else:
            feedback.append("uppercase letters")
            
        if re.search(r"[a-z]", password):
            strength += 1
        else:
            feedback.append("lowercase letters")
            
        if re.search(r"[0-9]", password):
            strength += 1
        else:
            feedback.append("numbers")
            
        if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
            strength += 1
        else:
            feedback.append("special characters")
        
        if strength == 5:
            self.password_strength_label.configure(text="Strong password", text_color="green")
        elif strength >= 3:
            self.password_strength_label.configure(text="Medium password", text_color="orange")
        else:
            self.password_strength_label.configure(text=f"Weak password (needs {', '.join(feedback)})", text_color="red")

    def toggle_password_visibility(self):
        if self.show_password_var.get():
            self.password_entry.configure(show="")
        else:
            self.password_entry.configure(show="*")

    def validate_form(self):
        valid = True
        
        if not self.name_entry.get().strip():
            messagebox.showerror("Error", "Please enter your full name")
            valid = False
            
        if not self.validate_email():
            valid = False
            
        if not self.password_entry.get():
            messagebox.showerror("Error", "Please enter a password")
            valid = False
        elif len(self.password_entry.get()) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters")
            valid = False
            
        if not self.terms_checkbox.get():
            messagebox.showerror("Error", "You must agree to the Terms of Service and Privacy Policy")
            valid = False
            
        return valid

    def _get_db_connection(self):
        """Establish secure MySQL connection with SSL"""
        try:
            return mysql.connector.connect(
                host=os.getenv("DB_HOST"),
                port=int(os.getenv("DB_PORT")),
                user=os.getenv("DB_USER"),
                password=os.getenv("DB_PASSWORD"),
                database=os.getenv("DB_NAME"),
                ssl_ca=None,  # SSL will be used but without certificate verification
                ssl_disabled=False
            )
        except Exception as e:
            messagebox.showerror("Database Error", f"Cannot connect to database: {str(e)}")
            return None

    def register_user(self):
        if not self.validate_form():
            return
            
        name = self.name_entry.get()
        email = self.email_entry.get()
        gender = self.gender_var.get()
        password = self.password_entry.get()
        
        # Hash password
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        
        try:
            conn = self._get_db_connection()
            if conn:
                cursor = conn.cursor()
                
                # Check if email exists
                cursor.execute("SELECT email FROM users WHERE email = %s", (email,))
                if cursor.fetchone():
                    messagebox.showerror("Error", "Email already registered")
                    return
                
                # Insert new user
                cursor.execute(
                    "INSERT INTO users (full_name, email, password_hash, gender) VALUES (%s, %s, %s, %s)",
                    (name, email, hashed_password, gender)
                )
                conn.commit()
                
                messagebox.showinfo("Success", "Registration successful!")
                
                # Clear form
                self.name_entry.delete(0, 'end')
                self.email_entry.delete(0, 'end')
                self.password_entry.delete(0, 'end')
                self.terms_checkbox.deselect()
                self.gender_var.set("Male")
                
                # Redirect to login
                self.controller.show_frame("LoginApp")
                
        except Exception as e:
            messagebox.showerror("Database Error", f"Registration failed: {str(e)}")
        finally:
            if 'conn' in locals() and conn.is_connected():
                conn.close()
import customtkinter as ctk
from dashboard import HotelBookingDashboard
from login import LoginApp
from register import RegistrationApp
from db_helper import DatabaseManager

class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System - Login")
        self.geometry("1400x900")
        ctk.set_appearance_mode("light")
        
        # Initialize database connection
        self.db = DatabaseManager()
        self.current_user = None
        
        # Create container frame
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Initialize all frames
        self.frames = {}
        
        for F in (LoginApp, RegistrationApp, HotelBookingDashboard):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show login frame first
        self.show_frame("LoginApp")
    
    def show_frame(self, page_name):
        """Show a frame and update window title"""
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Update window title
        titles = {
            "LoginApp": "Hotel Management System - Login",
            "RegistrationApp": "Hotel Management System - Register",
            "HotelBookingDashboard": "Hotel Management System - Dashboard"
        }
        self.title(titles.get(page_name, "Hotel Management System"))
        
        # Update dashboard if needed
        if page_name == "HotelBookingDashboard" and self.current_user:
            frame.update_user_display(self.current_user)
    
    def successful_login(self, user_data):
        """Handle post-login operations"""
        self.current_user = user_data
        self.show_frame("HotelBookingDashboard")
    
    def __del__(self):
        """Cleanup resources"""
        if hasattr(self, 'db'):
            self.db.close()

if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()
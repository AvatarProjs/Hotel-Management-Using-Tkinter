# import customtkinter as ctk
# from dashboard import HotelBookingDashboard
# from login import LoginApp
# from register import RegistrationApp
# from landing import HotelBookingSystem
# from password_recovery import PasswordRecoveryApp
# from mcustomer import CustomerManagementScreen
# from Report import HotelReportsPage
# from Reservations import HotelReservationsPage
# from db_helper import DatabaseManager

# class HotelApp(ctk.CTk):
#     def __init__(self):
#         super().__init__()
#         self.title("Hotel Management System")
#         self.geometry("1400x900")
#         ctk.set_appearance_mode("light")
#         ctk.set_default_color_theme("blue")
        
#         # Initialize database connection
#         self.db = DatabaseManager()
#         self.current_user = None
        
#         # Create container frame
#         self.container = ctk.CTkFrame(self)
#         self.container.pack(side="top", fill="both", expand=True)
#         self.container.grid_rowconfigure(0, weight=1)
#         self.container.grid_columnconfigure(0, weight=1)
        
#         # Initialize all frames
#         self.frames = {}
        
#         frames_classes = [
#             ("HotelBookingSystem", HotelBookingSystem),
#             ("LoginApp", LoginApp),
#             ("RegistrationApp", RegistrationApp),
#             ("PasswordRecoveryApp", PasswordRecoveryApp),
#             ("HotelBookingDashboard", HotelBookingDashboard),
#             ("CustomerManagementScreen", CustomerManagementScreen),
#             ("HotelReportsPage", HotelReportsPage),
#             ("HotelReservationsPage", HotelReservationsPage)
#         ]
        
#         for name, FrameClass in frames_classes:
#             frame = FrameClass(self.container, self)
#             self.frames[name] = frame
#             frame.grid(row=0, column=0, sticky="nsew")
        
#         # Show landing page first
#         self.show_frame("HotelBookingSystem")
    
#     def show_frame(self, page_name):
#         """Show a frame and update window title"""
#         frame = self.frames.get(page_name)
#         if not frame:
#             print(f"Error: Frame {page_name} not found!")
#             return
            
#         frame.tkraise()
        
#         # Update window title
#         titles = {
#             "HotelBookingSystem": "Hotel Booking System",
#             "LoginApp": "Login - Hotel Management",
#             "RegistrationApp": "Register - Hotel Management",
#             "PasswordRecoveryApp": "Password Recovery",
#             "HotelBookingDashboard": "DataBoard - Hotel Management",
#             "CustomerManagementScreen": "Customers - Hotel Management",
#             "HotelReportsPage": "Reports - Hotel Management",
#             "HotelReservationsPage": "Reservations - Hotel Management"
#         }
#         self.title(titles.get(page_name, "Hotel Management System"))
        
#         if page_name == "HotelBookingDashboard" and self.current_user:
#             frame.update_user_display(self.current_user)
    
#     def successful_login(self, user_data):
#         """Handle post-login operations"""
#         self.current_user = user_data
#         self.show_frame("HotelBookingDashboard")
    
#     def __del__(self):
#         """Cleanup resources"""
#         if hasattr(self, 'db'):
#             self.db.close()

# if __name__ == "__main__":
#     app = HotelApp()
#     app.mainloop()



import customtkinter as ctk
from dashboard import HotelBookingDashboard
from login import LoginApp
from register import RegistrationApp
from landing import HotelBookingSystem
from password_recovery import PasswordRecoveryApp
from mcustomer import CustomerManagementScreen
from Report import HotelReportsPage
from Reservations import HotelReservationsPage
from staff_member import StaffMemberScreen
from db_helper import DatabaseManager

class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("1400x900")
        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")
        
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
        
        frames_classes = [
            ("HotelBookingSystem", HotelBookingSystem),
            ("LoginApp", LoginApp),
            ("RegistrationApp", RegistrationApp),
            ("PasswordRecoveryApp", PasswordRecoveryApp),
            ("HotelBookingDashboard", HotelBookingDashboard),
            ("CustomerManagementScreen", CustomerManagementScreen),
            ("HotelReportsPage", HotelReportsPage),
            ("HotelReservationsPage", HotelReservationsPage),
            ("StaffMemberScreen", StaffMemberScreen)
        ]
        
        for name, FrameClass in frames_classes:
            frame = FrameClass(self.container, self)
            self.frames[name] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        # Show landing page first
        self.show_frame("HotelBookingSystem")
    
    def show_frame(self, page_name):
        """Show a frame and update window title"""
        frame = self.frames.get(page_name)
        if not frame:
            print(f"Error: Frame {page_name} not found!")
            return
            
        frame.tkraise()
        
        # Update window title
        titles = {
            "HotelBookingSystem": "Hotel Booking System",
            "LoginApp": "Login - Hotel Management",
            "RegistrationApp": "Register - Hotel Management",
            "PasswordRecoveryApp": "Password Recovery",
            "HotelBookingDashboard": "DataBoard - Hotel Management",
            "CustomerManagementScreen": "Customers - Hotel Management",
            "HotelReportsPage": "Reports - Hotel Management",
            "HotelReservationsPage": "Reservations - Hotel Management",
            "StaffMemberScreen": "Staff Members - Hotel Management"
        }
        self.title(titles.get(page_name, "Hotel Management System"))
        
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
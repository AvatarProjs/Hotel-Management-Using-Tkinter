import customtkinter as ctk
from dashboard import HotelBookingDashboard
from mcustomer import CustomerManagementScreen
from Reservations import HotelReservationsPage
from Report import HotelReportsPage
from login import LoginApp
from register import RegistrationApp
from password_recovery import PasswordRecoveryApp

class HotelApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("Hotel Management System")
        self.geometry("1400x900")
        ctk.set_appearance_mode("light")
        
        # Create container frame
        self.container = ctk.CTkFrame(self)
        self.container.pack(side="top", fill="both", expand=True)
        self.container.grid_rowconfigure(0, weight=1)
        self.container.grid_columnconfigure(0, weight=1)
        
        # Initialize all frames
        self.frames = {}
        for F in (HotelBookingDashboard, CustomerManagementScreen, 
                 HotelReservationsPage, HotelReportsPage, LoginApp,
                 RegistrationApp, PasswordRecoveryApp):
            frame = F(self.container, self)
            self.frames[F.__name__] = frame
            frame.grid(row=0, column=0, sticky="nsew")
        
        self.show_frame("LoginApp")
    
    def show_frame(self, page_name):
        frame = self.frames[page_name]
        frame.tkraise()
        
        # Update window title based on current page
        titles = {
            "HotelBookingDashboard": "Dashboard - Hotel Management System",
            "CustomerManagementScreen": "Customers - Hotel Management System",
            "HotelReservationsPage": "Reservations - Hotel Management System",
            "HotelReportsPage": "Reports - Hotel Management System",
            "LoginApp": "Login - Hotel Management System",
            "RegistrationApp": "Register - Hotel Management System",
            "PasswordRecoveryApp": "Password Recovery - Hotel Management System"
        }
        self.title(titles.get(page_name, "Hotel Management System"))

if __name__ == "__main__":
    app = HotelApp()
    app.mainloop()  
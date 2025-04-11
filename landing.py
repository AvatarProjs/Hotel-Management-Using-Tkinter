import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import os

# Set appearance mode and default color theme
ctk.set_appearance_mode("light")
ctk.set_default_color_theme("blue")

class HotelBookingSystem(ctk.CTk):
    def __init__(self):
        super().__init__()
        
        # Configure window
        self.title("Hotel Booking and Management System")
        self.geometry("1200x700")
        
        # Load the hotel lobby image
        try:
            # Get the directory of the current script
            current_dir = os.path.dirname(os.path.abspath(__file__))
            
            # Path to the hotel lobby image - adjust filename as needed
            image_path = os.path.join(current_dir, "hotel_lobby.jpg")
            
            # Load and resize the image
            self.bg_image = Image.open(image_path)
            self.bg_image = self.bg_image.resize((2000, 1000), Image.Resampling.LANCZOS)
            
            # Apply blur effect to the image
            self.blurred_image = self.bg_image.filter(ImageFilter.GaussianBlur(radius=5))
            self.bg_photo = ImageTk.PhotoImage(self.blurred_image)
            
            # Create a label to display the background image
            self.bg_label = tk.Label(self, image=self.bg_photo)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)
            
        except Exception as e:
            print(f"Error loading image: {e}")
            # Use a light gray background if image fails to load
            self.configure(fg_color="#e8e8e8")
        
        # Create top header frame with transparent background
        self.header_frame = ctk.CTkFrame(self, fg_color="transparent", height=40, corner_radius=0)
        self.header_frame.pack(fill="x", pady=(0, 0))
        self.header_frame.pack_propagate(False)
        
        # Title on left
        self.title_label = ctk.CTkLabel(
            self.header_frame, 
            text="Hotel Booking and Management System", 
            font=ctk.CTkFont(size=14, weight="bold"),
            text_color="white"  # Text color white for visibility against the image
        )
        self.title_label.pack(side="left", padx=20, pady=10)
        
        # Sign-in button on right
        self.signin_button = ctk.CTkButton(
            self.header_frame, 
            text="Sign-in", 
            width=80,
            height=28,
            corner_radius=5
        )
        self.signin_button.pack(side="right", padx=20, pady=5)
        
        # Create center content frame with white background
        self.content_frame = ctk.CTkFrame(
            self, 
            fg_color="white", 
            corner_radius=10,
            width=850,
            height=260
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.content_frame.pack_propagate(False)
        
        # Add title to content frame
        self.system_title_label = ctk.CTkLabel(
            self.content_frame, 
            text="HOTEL BOOKING\nMANAGEMENT\nSYSTEM", 
            font=ctk.CTkFont(size=28, weight="bold"),
            text_color="black"
        )
        self.system_title_label.place(relx=0.5, rely=0.38, anchor="center")
        
        # Add get started button
        self.get_started_button = ctk.CTkButton(
            self.content_frame, 
            text="Get Started →", 
            font=ctk.CTkFont(size=14),
            fg_color="#333333",
            hover_color="#555555",
            corner_radius=5,
            width=120,
            height=35
        )
        self.get_started_button.place(relx=0.5, rely=0.75, anchor="center")

if __name__ == "__main__":
    app = HotelBookingSystem()
    app.mainloop()
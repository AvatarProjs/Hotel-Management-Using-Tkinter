import customtkinter as ctk
import tkinter as tk
from PIL import Image, ImageTk, ImageFilter
import os
from tkinter import Canvas


class HotelBookingSystem(ctk.CTkFrame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller
        self.parent = parent

        # Configure window
        self.configure(fg_color="#f0f8ff")

        # Setup background first (before other widgets)
        self.setup_background()

        # Create top header frame
        self.header_frame = ctk.CTkFrame(self, fg_color=("#ffffff", "#ffffff"), height=55, corner_radius=0)
        self.header_frame.configure(border_width=1, border_color="#e0e0e0")
        self.header_frame.pack(fill="x", pady=(0, 0))
        self.header_frame.pack_propagate(False)

        # Title label
        self.title_label = ctk.CTkLabel(
            self.header_frame,
            text="Hotel Booking and Management System",
            font=ctk.CTkFont(family="Helvetica", size=16, weight="bold"),
            text_color="#0a58ca"
        )
        self.title_label.pack(side="left", padx=20, pady=15)

        # Sign-in button
        self.signin_button = ctk.CTkButton(
            self.header_frame,
            text="Sign In",
            width=100,
            height=32,
            corner_radius=6,
            font=ctk.CTkFont(size=14),
            fg_color="#4682B4",
            hover_color="#3A6EA5",
            command=lambda: controller.show_frame("LoginApp")
        )
        self.signin_button.pack(side="right", padx=20, pady=10)

        # Create center content frame
        self.content_frame = ctk.CTkFrame(
            self,
            fg_color=("#ffffff", "#ffffff"),
            corner_radius=15,
            width=900,
            height=350,
            border_width=1,
            border_color="#e0e0e0"
        )
        self.content_frame.place(relx=0.5, rely=0.5, anchor="center")
        self.content_frame.pack_propagate(False)

        # Add decorative elements
        self.line_canvas = Canvas(self.content_frame, height=2, bg="white", highlightthickness=0)
        self.line_canvas.pack(fill="x", padx=40, pady=(40, 0))

        # Create gradient blue line
        for i in range(900):
            color_intensity = abs((i - 450) / 450)
            blue_value = int(200 - 100 * color_intensity)
            color = f"#{70 + int(40 * color_intensity):02x}{100 + int(40 * color_intensity):02x}{blue_value:02x}"
            self.line_canvas.create_line(i, 0, i, 2, fill=color)

        # Add title to content frame
        self.system_title_label = ctk.CTkLabel(
            self.content_frame,
            text="HOTEL BOOKING",
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#0a58ca"
        )
        self.system_title_label.place(relx=0.5, rely=0.28, anchor="center")

        self.system_subtitle_label = ctk.CTkLabel(
            self.content_frame,
            text="MANAGEMENT",
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#0a58ca"
        )
        self.system_subtitle_label.place(relx=0.5, rely=0.43, anchor="center")

        self.system_subtitle2_label = ctk.CTkLabel(
            self.content_frame,
            text="SYSTEM",
            font=ctk.CTkFont(family="Arial", size=36, weight="bold"),
            text_color="#0a58ca"
        )
        self.system_subtitle2_label.place(relx=0.5, rely=0.58, anchor="center")

        # Bottom decorative line
        self.line_canvas2 = Canvas(self.content_frame, height=2, bg="white", highlightthickness=0)
        self.line_canvas2.pack(fill="x", padx=40, pady=(260, 0))

        # Create another gradient blue line
        for i in range(900):
            color_intensity = abs((i - 450) / 450)
            blue_value = int(200 - 100 * color_intensity)
            color = f"#{70 + int(40 * color_intensity):02x}{100 + int(40 * color_intensity):02x}{blue_value:02x}"
            self.line_canvas2.create_line(i, 0, i, 2, fill=color)

        # Get started button
        self.get_started_button = ctk.CTkButton(
            self.content_frame,
            text="Get Started →",
            font=ctk.CTkFont(family="Helvetica", size=16),
            fg_color="#0a58ca",
            hover_color="#084298",
            corner_radius=8,
            width=180,
            height=45,
            command=lambda: controller.show_frame("RegistrationApp")
        )
        self.get_started_button.place(relx=0.5, rely=0.8, anchor="center")

        # Ensure proper layering
        self.update_layering()

        # Add subtle animation effect for the button
        self.animate_button()

    def update_layering(self):
        """Ensure proper widget layering"""
        if hasattr(self, 'bg_label'):
            self.bg_label.lower()
        if hasattr(self, 'content_frame'):
            self.content_frame.lift()
        if hasattr(self, 'header_frame'):
            self.header_frame.lift()

    def setup_background(self):
        """Handle background with multiple fallback options"""
        # First attempt: Try to load the hotel lobby image
        image_loaded = self.load_background_image()

        # If image loading fails, create a gradient background
        if not image_loaded:
            self.create_gradient_background()

    def load_background_image(self):
        """Attempt to load the hotel lobby background image"""
        try:
            current_dir = os.path.dirname(os.path.abspath(__file__))
            image_path = os.path.join(current_dir, "hotel_lobby.jpg")

            print(f"Attempting to load image from: {image_path}")

            if not os.path.exists(image_path):
                print("Image not found at:", image_path)
                return False

            # Load and prepare the image
            pil_image = Image.open(image_path)
            blurred_image = pil_image.filter(ImageFilter.GaussianBlur(radius=3))

            # Create CTkImage
            self.bg_image = ctk.CTkImage(
                light_image=blurred_image,
                dark_image=blurred_image,
                size=(self.winfo_screenwidth(), self.winfo_screenheight())
            )

            # Create background label
            self.bg_label = ctk.CTkLabel(self, text="", image=self.bg_image)
            self.bg_label.place(x=0, y=0, relwidth=1, relheight=1)

            print("Background image loaded successfully")
            return True

        except Exception as e:
            print(f"Error loading background image: {e}")
            return False

    def create_gradient_background(self):
        """Create a gradient background as fallback"""
        print("Creating gradient background fallback")

        # Create a canvas for the gradient
        self.bg_canvas = Canvas(self, highlightthickness=0)
        self.bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)

        # Create gradient from deep blue to light blue
        width, height = 2000, 1000
        start_color = (0, 40, 80)  # Deep blue
        end_color = (100, 180, 255)  # Light blue

        for y in range(0, height, 2):
            ratio = y / height
            r = int(start_color[0] * (1 - ratio) + end_color[0] * ratio)
            g = int(start_color[1] * (1 - ratio) + end_color[1] * ratio)
            b = int(start_color[2] * (1 - ratio) + end_color[2] * ratio)
            color = f"#{r:02x}{g:02x}{b:02x}"
            self.bg_canvas.create_line(0, y, width, y, fill=color)

        # Add decorative elements
        safe_stipples = ["gray25", "gray50", "gray75"]

        # Top left decorative circle
        for i in range(300, 0, -50):
            stipple = safe_stipples[i % len(safe_stipples)] if i < 250 else ""
            self.bg_canvas.create_oval(
                -100, -100, i * 2, i * 2,
                outline="#ffffff",
                width=1,
                stipple=stipple
            )

        # Bottom right decorative circle
        for i in range(250, 0, -50):
            stipple = safe_stipples[i % len(safe_stipples)] if i < 200 else ""
            self.bg_canvas.create_oval(
                width, height, width - i * 2, height - i * 2,
                outline="#ffffff",
                width=1,
                stipple=stipple
            )

        # Add subtle pattern overlay
        self.bg_canvas.create_rectangle(
            0, 0, width, height,
            fill="#ffffff",
            outline="",
            stipple="gray75"
        )

    def animate_button(self):
        """Create a subtle pulsing effect for the Get Started button"""
        original_color = self.get_started_button.cget("fg_color")
        hover_color = self.get_started_button.cget("hover_color")

        def pulse_animation(state=True):
            if state:
                self.get_started_button.configure(fg_color=hover_color)
                self.after(700, lambda: pulse_animation(False))
            else:
                self.get_started_button.configure(fg_color=original_color)
                self.after(1500, lambda: pulse_animation(True))

        # Start the animation after a delay
        self.after(3000, pulse_animation)
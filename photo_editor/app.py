import tkinter as tk
from tkinter import filedialog, simpledialog, messagebox
from PIL import Image, ImageTk, ImageFilter, ImageEnhance, ImageOps, ImageDraw, ImageFont
import os

class ImageEditor:
    def __init__(self, root):
        self.root = root
        self.root.title("Advanced Image Editor")
        self.root.geometry("1000x800")
        self.root.configure(bg="black")

        self.image_path = None
        self.original_image = None
        self.processed_image = None
        self.history = []
        self.history_index = -1

        # Create GUI components
        self.create_widgets()

    def create_widgets(self):
        # Upload Button
        self.upload_button = tk.Button(self.root, text="Upload Image", command=self.upload_image, bg="blue", fg="white", font=("Helvetica", 12, "bold"))
        self.upload_button.pack(pady=10)

        # Image Display
        self.image_label = tk.Label(self.root, bg="black")
        self.image_label.pack(pady=20)

        # Filter Frame
        self.filter_frame = tk.Frame(self.root, bg="black")
        self.filter_frame.pack(pady=10)

        # Filter Buttons
        self.filter_buttons = [
            ("Blur", self.apply_blur),
            ("Sharpen", self.apply_sharpen),
            ("Grayscale", self.apply_grayscale),
            ("Sepia", self.apply_sepia),
            ("Negative", self.apply_negative),
            ("Vivid", self.apply_vivid),
            ("Grainy", self.apply_grainy),
            ("Normal", self.apply_normal)
        ]

        for text, command in self.filter_buttons:
            button = tk.Button(self.filter_frame, text=text, command=command, bg="green", fg="white", font=("Helvetica", 10, "bold"))
            button.pack(side="left", padx=5)

        # Enhancement Sliders
        self.slider_frame = tk.Frame(self.root, bg="black")
        self.slider_frame.pack(pady=10)

        self.create_slider("Brightness", self.apply_brightness_enhance)
        self.create_slider("Contrast", self.apply_contrast_enhance)
        self.create_slider("Color", self.apply_color_enhance)
        self.create_slider("Sharpness", self.apply_sharpness_enhance)
        self.create_slider("Blur Amount", self.apply_blur_enhance)

        # Control Buttons
        self.control_frame = tk.Frame(self.root, bg="black")
        self.control_frame.pack(pady=10)

        self.undo_button = tk.Button(self.control_frame, text="Undo", command=self.undo, bg="yellow", fg="black", font=("Helvetica", 10, "bold"))
        self.undo_button.pack(side="left", padx=5)

        self.redo_button = tk.Button(self.control_frame, text="Redo", command=self.redo, bg="yellow", fg="black", font=("Helvetica", 10, "bold"))
        self.redo_button.pack(side="left", padx=5)

        self.save_button = tk.Button(self.control_frame, text="Save", command=self.save_image, bg="orange", fg="white", font=("Helvetica", 10, "bold"))
        self.save_button.pack(side="left", padx=5)

        self.download_button = tk.Button(self.control_frame, text="Download", command=self.download_image, bg="purple", fg="white", font=("Helvetica", 10, "bold"))
        self.download_button.pack(side="left", padx=5)

        # Before and After Button
        self.compare_button = tk.Button(self.root, text="Before and After", command=self.compare_images, bg="orange", fg="white", font=("Helvetica", 12, "bold"))
        self.compare_button.pack(pady=10)

        # Crop and Rotate Buttons
        self.crop_button = tk.Button(self.root, text="Crop", command=self.crop_image, bg="red", fg="white", font=("Helvetica", 12, "bold"))
        self.crop_button.pack(side="left", padx=5, pady=10)

        self.rotate_button = tk.Button(self.root, text="Rotate", command=self.rotate_image, bg="red", fg="white", font=("Helvetica", 12, "bold"))
        self.rotate_button.pack(side="left", padx=5, pady=10)

        # Add Text Button
        self.text_button = tk.Button(self.root, text="Add Text", command=self.add_text, bg="red", fg="white", font=("Helvetica", 12, "bold"))
        self.text_button.pack(side="left", padx=5, pady=10)

    def create_slider(self, text, command):
        label = tk.Label(self.slider_frame, text=text, bg="black", fg="white", font=("Helvetica", 10, "bold"))
        label.pack(side="left", padx=5)
        slider = tk.Scale(self.slider_frame, from_=0, to=100, orient="horizontal", command=command, bg="black", fg="white", font=("Helvetica", 10, "bold"))
        slider.set(50)
        slider.pack(side="left", padx=5)

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.jpg *.jpeg *.png")])
        if self.image_path:
            self.original_image = Image.open(self.image_path)
            self.processed_image = self.original_image.copy()
            self.add_to_history(self.processed_image)
            self.display_image(self.original_image)

    def display_image(self, image):
        image = image.resize((500, 400), Image.LANCZOS)
        img_tk = ImageTk.PhotoImage(image)
        self.image_label.config(image=img_tk)
        self.image_label.image = img_tk

    def apply_filter(self, filter_function, intensity=1.0):
        if self.original_image:
            self.processed_image = filter_function(self.processed_image, intensity)
            self.add_to_history(self.processed_image)
            self.display_image(self.processed_image)

    def apply_blur(self, intensity=1.0):
        self.apply_filter(lambda img, intensity: img.filter(ImageFilter.GaussianBlur(radius=intensity * 2)))

    def apply_sharpen(self, intensity=1.0):
        self.apply_filter(lambda img, intensity: img.filter(ImageFilter.UnsharpMask(radius=2, percent=150, threshold=intensity * 3)))

    def apply_grayscale(self, intensity=1.0):
        self.apply_filter(lambda img, intensity: ImageOps.grayscale(img))

    def apply_sepia(self, intensity=1.0):
        def sepia_filter(img, intensity):
            width, height = img.size
            pixels = img.load()
            for py in range(height):
                for px in range(width):
                    r, g, b = img.getpixel((px, py))
                    tr = int(0.393 * r + 0.769 * g + 0.189 * b)
                    tg = int(0.349 * r + 0.686 * g + 0.168 * b)
                    tb = int(0.272 * r + 0.534 * g + 0.131 * b)
                    tr = min(255, int(tr * intensity))
                    tg = min(255, int(tg * intensity))
                    tb = min(255, int(tb * intensity))
                    pixels[px, py] = (tr, tg, tb)
            return img
        self.apply_filter(sepia_filter, intensity)

    def apply_negative(self, intensity=1.0):
        self.apply_filter(lambda img, intensity: ImageOps.invert(img))

    def apply_vivid(self, intensity=1.0):
        def vivid_filter(img, intensity):
            enhancer = ImageEnhance.Color(img)
            return enhancer.enhance(intensity * 2)
        self.apply_filter(vivid_filter, intensity)

    def apply_grainy(self, intensity=1.0):
        def grainy_filter(img, intensity):
            width, height = img.size
            pixels = img.load()
            for py in range(height):
                for px in range(width):
                    if px % 2 == 0 and py % 2 == 0:
                        r, g, b = img.getpixel((px, py))
                        tr = int(r * intensity * 0.5)
                        tg = int(g * intensity * 0.5)
                        tb = int(b * intensity * 0.5)
                        pixels[px, py] = (tr, tg, tb)
            return img
        self.apply_filter(grainy_filter, intensity)

    def apply_normal(self, intensity=1.0):
        if self.original_image:
            self.processed_image = self.original_image.copy()
            self.add_to_history(self.processed_image)
            self.display_image(self.original_image)

    def apply_color_enhance(self, value):
        self.apply_enhance(ImageEnhance.Color, value)

    def apply_contrast_enhance(self, value):
        self.apply_enhance(ImageEnhance.Contrast, value)

    def apply_brightness_enhance(self, value):
        self.apply_enhance(ImageEnhance.Brightness, value)

    def apply_sharpness_enhance(self, value):
        self.apply_enhance(ImageEnhance.Sharpness, value)

    def apply_blur_enhance(self, value):
        self.apply_blur(value / 100)

    def apply_enhance(self, enhancer, value):
        if self.original_image:
            factor = value / 50  # Adjusting factor based on slider value
            enhancer_instance = enhancer(self.processed_image)
            self.processed_image = enhancer_instance.enhance(factor)
            self.add_to_history(self.processed_image)
            self.display_image(self.processed_image)

    def add_to_history(self, image):
        # Trim the history in case of undo
        self.history = self.history[:self.history_index + 1]
        self.history.append(image.copy())
        self.history_index += 1

    def undo(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.processed_image = self.history[self.history_index]
            self.display_image(self.processed_image)

    def redo(self):
        if self.history_index < len(self.history) - 1:
            self.history_index += 1
            self.processed_image = self.history[self.history_index]
            self.display_image(self.processed_image)

    def save_image(self):
        self.add_to_history(self.processed_image)
        self.display_image(self.processed_image)

    def download_image(self):
        if self.processed_image:
            file_path = filedialog.asksaveasfilename(defaultextension=".png", filetypes=[("PNG files", "*.png"), ("JPEG files", "*.jpg *.jpeg")])
            if file_path:
                self.processed_image.save(file_path)
                messagebox.showinfo("Image Saved", "Your image has been saved successfully!")

    def compare_images(self):
        if self.original_image and self.processed_image:
            compare_window = tk.Toplevel(self.root)
            compare_window.title("Before and After Comparison")
            compare_window.geometry("1200x600")
            compare_window.configure(bg="black")

            original_img = self.original_image.resize((500, 400), Image.LANCZOS)
            processed_img = self.processed_image.resize((500, 400), Image.LANCZOS)

            original_img_tk = ImageTk.PhotoImage(original_img)
            processed_img_tk = ImageTk.PhotoImage(processed_img)

            original_label = tk.Label(compare_window, image=original_img_tk, bg="black")
            original_label.image = original_img_tk
            original_label.pack(side="left", padx=10, pady=10)

            processed_label = tk.Label(compare_window, image=processed_img_tk, bg="black")
            processed_label.image = processed_img_tk
            processed_label.pack(side="right", padx=10, pady=10)

    def crop_image(self):
        if self.processed_image:
            crop_box = simpledialog.askstring("Crop", "Enter crop box coordinates (x1,y1,x2,y2):")
            if crop_box:
                coords = list(map(int, crop_box.split(',')))
                self.processed_image = self.processed_image.crop(coords)
                self.add_to_history(self.processed_image)
                self.display_image(self.processed_image)

    def rotate_image(self):
        if self.processed_image:
            angle = simpledialog.askfloat("Rotate", "Enter rotation angle:")
            if angle is not None:
                self.processed_image = self.processed_image.rotate(angle, expand=True)
                self.add_to_history(self.processed_image)
                self.display_image(self.processed_image)

    def add_text(self):
        if self.processed_image:
            text = simpledialog.askstring("Add Text", "Enter the text:")
            if text:
                font_size = simpledialog.askinteger("Font Size", "Enter font size:", minvalue=10, maxvalue=100)
                font_choice = simpledialog.askstring("Font Choice", "Enter font type (Helvetica, Arial, Times, etc.):")
                x_position = simpledialog.askinteger("X Position", "Enter X position:", minvalue=0, maxvalue=self.processed_image.width)
                y_position = simpledialog.askinteger("Y Position", "Enter Y position:", minvalue=0, maxvalue=self.processed_image.height)

                draw = ImageDraw.Draw(self.processed_image)
                font = ImageFont.truetype(f"{font_choice}.ttf", font_size)
                draw.text((x_position, y_position), text, fill="white", font=font)

                self.add_to_history(self.processed_image)
                self.display_image(self.processed_image)

# Initialize and run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = ImageEditor(root)
    root.mainloop()

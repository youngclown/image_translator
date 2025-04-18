"""
Image Text Translator GUI

This script provides a graphical user interface for extracting text from images
and translating it to Korean. It can process a single image or all images in a folder.

Requirements:
- Pillow (PIL): pip install pillow
- pytesseract: pip install pytesseract
- googletrans: pip install googletrans==4.0.0-rc1
- Tesseract OCR must be installed on your system:
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki
  - macOS: brew install tesseract
  - Linux: apt-get install tesseract-ocr

Usage:
python image_text_translator_gui.py
"""

import os
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox
from PIL import Image, ImageTk
import pytesseract
from googletrans import Translator

# Uncomment and modify the line below if Tesseract is not in your PATH (Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

class ImageTextTranslatorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Text Translator")
        self.root.geometry("800x700")
        self.root.resizable(True, True)

        self.image_path = None
        self.folder_path = None
        self.image_files = []
        self.current_image_index = 0
        self.setup_ui()

    def setup_ui(self):
        # Frame for image selection
        self.frame_top = tk.Frame(self.root)
        self.frame_top.pack(fill=tk.X, padx=10, pady=10)

        self.label_instruction = tk.Label(self.frame_top, text="Select an image or folder to extract and translate text:")
        self.label_instruction.pack(side=tk.LEFT, padx=5)

        self.btn_browse_image = tk.Button(self.frame_top, text="Browse Image", command=self.browse_image)
        self.btn_browse_image.pack(side=tk.LEFT, padx=5)

        self.btn_browse_folder = tk.Button(self.frame_top, text="Browse Folder", command=self.browse_folder)
        self.btn_browse_folder.pack(side=tk.LEFT, padx=5)

        self.btn_process = tk.Button(self.frame_top, text="Process", command=self.process_image)
        self.btn_process.pack(side=tk.LEFT, padx=5)

        self.btn_process_all = tk.Button(self.frame_top, text="Process All Images", command=self.process_all_images)
        self.btn_process_all.pack(side=tk.LEFT, padx=5)

        # Frame for image preview
        self.frame_image = tk.Frame(self.root, height=200)
        self.frame_image.pack(fill=tk.X, padx=10, pady=5)

        self.label_image = tk.Label(self.frame_image, text="Image preview will appear here")
        self.label_image.pack(fill=tk.BOTH, expand=True)

        # Frame for extracted text
        self.frame_extracted = tk.LabelFrame(self.root, text="Extracted Text")
        self.frame_extracted.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_extracted = scrolledtext.ScrolledText(self.frame_extracted, wrap=tk.WORD, height=10)
        self.text_extracted.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Frame for translated text
        self.frame_translated = tk.LabelFrame(self.root, text="Korean Translation")
        self.frame_translated.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        self.text_translated = scrolledtext.ScrolledText(self.frame_translated, wrap=tk.WORD, height=10)
        self.text_translated.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = tk.Label(self.root, textvariable=self.status_var, bd=1, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(side=tk.BOTTOM, fill=tk.X)

    def browse_image(self):
        filetypes = [
            ("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.gif"),
            ("All files", "*.*")
        ]
        self.image_path = filedialog.askopenfilename(
            title="Select Image",
            filetypes=filetypes
        )

        if self.image_path:
            self.folder_path = None  # Reset folder path when selecting a single image
            self.image_files = []
            self.current_image_index = 0
            self.status_var.set(f"Selected image: {os.path.basename(self.image_path)}")
            self.display_image_preview()

    def browse_folder(self):
        self.folder_path = filedialog.askdirectory(
            title="Select Folder Containing Images"
        )

        if self.folder_path:
            self.image_path = None  # Reset image path when selecting a folder
            self.image_files = self.get_image_files_from_folder(self.folder_path)
            self.current_image_index = 0

            if self.image_files:
                self.status_var.set(f"Selected folder: {os.path.basename(self.folder_path)} ({len(self.image_files)} images found)")
                # Display the first image as preview
                if len(self.image_files) > 0:
                    self.image_path = self.image_files[0]
                    self.display_image_preview()
            else:
                self.status_var.set(f"No image files found in the selected folder: {os.path.basename(self.folder_path)}")
                messagebox.showinfo("No Images", "No image files were found in the selected folder.")

    def get_image_files_from_folder(self, folder_path):
        """Get all image files from the specified folder."""
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
        image_files = []

        try:
            for file in os.listdir(folder_path):
                if file.lower().endswith(image_extensions):
                    full_path = os.path.join(folder_path, file)
                    image_files.append(full_path)

            return sorted(image_files)
        except Exception as e:
            messagebox.showerror("Error", f"Error reading folder: {e}")
            return []

    def display_image_preview(self):
        try:
            # Open and resize image for preview
            img = Image.open(self.image_path)

            # Calculate new dimensions while maintaining aspect ratio
            width, height = img.size
            max_width = 780
            max_height = 200

            # Resize if needed
            if width > max_width or height > max_height:
                ratio = min(max_width / width, max_height / height)
                new_width = int(width * ratio)
                new_height = int(height * ratio)
                img = img.resize((new_width, new_height), Image.LANCZOS)

            # Convert to PhotoImage for display
            photo = ImageTk.PhotoImage(img)

            # Update label
            self.label_image.config(image=photo, text="")
            self.label_image.image = photo  # Keep a reference to prevent garbage collection

        except Exception as e:
            messagebox.showerror("Error", f"Failed to display image preview: {e}")

    def process_image(self):
        if not self.image_path:
            messagebox.showwarning("Warning", "Please select an image first.")
            return

        self.status_var.set(f"Processing image: {os.path.basename(self.image_path)}...")
        self.root.update_idletasks()

        try:
            # Extract text
            extracted_text = self.extract_text_from_image(self.image_path)

            if not extracted_text:
                self.status_var.set("No text was extracted from the image.")
                return

            # Display extracted text
            self.text_extracted.delete(1.0, tk.END)
            self.text_extracted.insert(tk.END, extracted_text)

            # Translate text
            self.status_var.set("Translating text...")
            self.root.update_idletasks()

            translated_text = self.translate_text_to_korean(extracted_text)

            if not translated_text:
                self.status_var.set("Translation failed.")
                return

            # Display translated text
            self.text_translated.delete(1.0, tk.END)
            self.text_translated.insert(tk.END, translated_text)

            self.status_var.set("Processing completed successfully.")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}")
            self.status_var.set("Error during processing.")

    def process_all_images(self):
        if not self.folder_path or not self.image_files:
            messagebox.showwarning("Warning", "Please select a folder with images first.")
            return

        total_images = len(self.image_files)
        if total_images == 0:
            messagebox.showinfo("No Images", "No image files were found in the selected folder.")
            return

        # Create a new window to display results
        results_window = tk.Toplevel(self.root)
        results_window.title("Batch Processing Results")
        results_window.geometry("800x600")

        # Create a frame for the results
        results_frame = tk.Frame(results_window)
        results_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Create a scrolled text widget to display results
        results_text = scrolledtext.ScrolledText(results_frame, wrap=tk.WORD)
        results_text.pack(fill=tk.BOTH, expand=True)

        results_text.insert(tk.END, f"Processing {total_images} images from folder: {self.folder_path}\n\n")

        # Process each image
        for i, image_path in enumerate(self.image_files):
            try:
                # Update status
                self.status_var.set(f"Processing image {i+1}/{total_images}: {os.path.basename(image_path)}...")
                self.root.update_idletasks()

                # Display current image
                self.image_path = image_path
                self.display_image_preview()

                # Extract text
                extracted_text = self.extract_text_from_image(image_path)

                if not extracted_text or extracted_text.strip() == "":
                    results_text.insert(tk.END, f"Image {i+1}: {os.path.basename(image_path)}\n")
                    results_text.insert(tk.END, "No text was extracted from this image.\n\n")
                    continue

                # Translate text
                self.status_var.set(f"Translating text from image {i+1}/{total_images}...")
                self.root.update_idletasks()

                translated_text = self.translate_text_to_korean(extracted_text)

                if not translated_text:
                    results_text.insert(tk.END, f"Image {i+1}: {os.path.basename(image_path)}\n")
                    results_text.insert(tk.END, f"Extracted text: {extracted_text}\n")
                    results_text.insert(tk.END, "Translation failed.\n\n")
                    continue

                # Add results to the results window
                results_text.insert(tk.END, f"Image {i+1}: {os.path.basename(image_path)}\n")
                results_text.insert(tk.END, f"Extracted text: {extracted_text}\n")
                results_text.insert(tk.END, f"Korean translation: {translated_text}\n\n")

                # Also update the main window with the current image's results
                self.text_extracted.delete(1.0, tk.END)
                self.text_extracted.insert(tk.END, extracted_text)

                self.text_translated.delete(1.0, tk.END)
                self.text_translated.insert(tk.END, translated_text)

            except Exception as e:
                results_text.insert(tk.END, f"Image {i+1}: {os.path.basename(image_path)}\n")
                results_text.insert(tk.END, f"Error: {e}\n\n")

        self.status_var.set(f"Completed processing {total_images} images.")
        results_text.insert(tk.END, f"Batch processing completed. Processed {total_images} images.")

    def extract_text_from_image(self, image_path):
        """Extract text from an image using OCR."""
        try:
            img = Image.open(image_path)
            text = pytesseract.image_to_string(img)
            return text.strip()
        except Exception as e:
            messagebox.showerror("OCR Error", f"Error extracting text from image: {e}")
            return None

    def translate_text_to_korean(self, text):
        """Translate text to Korean."""
        try:
            translator = Translator()
            translation = translator.translate(text, dest='ko')
            return translation.text
        except Exception as e:
            messagebox.showerror("Translation Error", f"Error translating text: {e}")
            return None

def main():
    root = tk.Tk()
    app = ImageTextTranslatorApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()

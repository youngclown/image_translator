"""
Example Usage of Image Text Translator

This script demonstrates how to use the image text extraction and translation
functionality programmatically in your own Python applications.
It shows how to process a single image or all images in a folder.
"""

import os
from PIL import Image
import pytesseract
from googletrans import Translator

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

# Uncomment and modify the line below if Tesseract is not in your PATH (Windows)
# pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def extract_text_from_image(image_path):
    """
    Extract text from an image using OCR.

    Args:
        image_path (str): Path to the image file

    Returns:
        str: Extracted text from the image
    """
    try:
        # Open the image
        img = Image.open(image_path)

        # Extract text using pytesseract
        text = pytesseract.image_to_string(img)

        return text.strip()
    except Exception as e:
        print(f"Error extracting text from image: {e}")
        return None

def translate_text_to_korean(text):
    """
    Translate text to Korean.

    Args:
        text (str): Text to translate

    Returns:
        str: Translated text in Korean
    """
    try:
        # Initialize the translator
        translator = Translator()

        # Translate the text to Korean
        translation = translator.translate(text, dest='ko')

        return translation.text
    except Exception as e:
        print(f"Error translating text: {e}")
        return None

def get_image_files_from_folder(folder_path):
    """
    Get all image files from the specified folder.

    Args:
        folder_path (str): Path to the folder containing images

    Returns:
        list: List of full paths to image files
    """
    image_extensions = ('.png', '.jpg', '.jpeg', '.bmp', '.gif')
    image_files = []

    try:
        for file in os.listdir(folder_path):
            if file.lower().endswith(image_extensions):
                full_path = os.path.join(folder_path, file)
                image_files.append(full_path)

        return sorted(image_files)
    except Exception as e:
        print(f"Error reading folder: {e}")
        return []

def process_single_image(image_path):
    """
    Process a single image: extract text and translate it to Korean.

    Args:
        image_path (str): Path to the image file
    """
    print(f"Processing image: {image_path}")

    # Extract text from the image
    extracted_text = extract_text_from_image(image_path)

    if not extracted_text:
        print("No text was extracted from the image.")
        return

    print("\nExtracted Text:")
    print("-" * 50)
    print(extracted_text)
    print("-" * 50)

    # Translate the extracted text to Korean
    translated_text = translate_text_to_korean(extracted_text)

    if not translated_text:
        print("Translation failed.")
        return

    print("\nKorean Translation:")
    print("-" * 50)
    print(translated_text)
    print("-" * 50)

    return extracted_text, translated_text

def process_folder(folder_path):
    """
    Process all images in a folder: extract text and translate it to Korean.

    Args:
        folder_path (str): Path to the folder containing images
    """
    # Get all image files from the folder
    image_files = get_image_files_from_folder(folder_path)

    if not image_files:
        print(f"No image files found in folder: {folder_path}")
        return

    print(f"Found {len(image_files)} image(s) in folder: {folder_path}")

    # Process each image
    for i, image_path in enumerate(image_files):
        print(f"\n[{i+1}/{len(image_files)}] Processing: {os.path.basename(image_path)}")
        process_single_image(image_path)

def main():
    # Example 1: Process a single image
    print("Example 1: Processing a single image")
    print("=" * 70)

    image_path = "D:\\1234"  # Replace with your image path

    # Check if the file exists
    if os.path.exists(image_path):
        process_single_image(image_path)
    else:
        print(f"Warning: Example image file '{image_path}' does not exist.")
        print("Please replace with a valid image path to test.")

    # Example 2: Process all images in a folder
    print("\n\nExample 2: Processing all images in a folder")
    print("=" * 70)

    folder_path = "D:\\1234"  # Replace with your folder path

    # Check if the folder exists
    if os.path.exists(folder_path) and os.path.isdir(folder_path):
        process_folder(folder_path)
    else:
        print(f"Warning: Example folder '{folder_path}' does not exist or is not a directory.")
        print("Please replace with a valid folder path to test.")

    # Example of how to use in your own application
    print("\n\nExample of programmatic usage:")
    print("-" * 70)
    print("# Example 1: Process a single image")
    print("extracted_text, translated_text = process_single_image('path/to/your/image.jpg')")
    print("print(f'Translated text: {translated_text}')")
    print("\n# Example 2: Process all images in a folder")
    print("process_folder('path/to/your/folder')")
    print("-" * 70)

if __name__ == "__main__":
    main()

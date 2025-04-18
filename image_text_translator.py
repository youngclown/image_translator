"""
Image Text Translator

This script extracts text from images and translates it to Korean.
Requirements:
- Pillow (PIL): pip install pillow
- pytesseract: pip install pytesseract
- googletrans: pip install googletrans==4.0.0-rc1
- Tesseract OCR must be installed on your system:
  - Windows: https://github.com/UB-Mannheim/tesseract/wiki
  - macOS: brew install tesseract
  - Linux: apt-get install tesseract-ocr

Usage:
python image_text_translator.py <path_to_image>
"""

import sys
import os
from PIL import Image
import pytesseract
from googletrans import Translator

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

def main():
    # Check if image path is provided
    if len(sys.argv) < 2:
        print("Usage: python image_text_translator.py <path_to_image>")
        return

    image_path = sys.argv[1]

    # Check if the file exists
    if not os.path.exists(image_path):
        print(f"Error: File '{image_path}' does not exist.")
        return

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

if __name__ == "__main__":
    main()

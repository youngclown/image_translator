"""
Example Usage of Image Text Translator

This script demonstrates how to use the image text extraction and translation
functionality programmatically in your own Python applications.
"""

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

def main():
    # Example usage
    image_path = "D:\\1234\\다운로드 (1).png"  # Replace with your image path
    
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
    
    # Example of how to use in your own application
    print("\nExample of programmatic usage:")
    print("-" * 50)
    print("# Extract text from an image")
    print("text = extract_text_from_image('path/to/your/image.jpg')")
    print("# Translate text to Korean")
    print("korean_text = translate_text_to_korean(text)")
    print("# Use the translated text in your application")
    print("print(f'Translated text: {korean_text}')")
    print("-" * 50)

if __name__ == "__main__":
    main()
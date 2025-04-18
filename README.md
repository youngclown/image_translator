# Image Text Translator

This project provides tools to extract text from images using OCR (Optical Character Recognition) and translate the extracted text to Korean. It includes both a command-line interface and a graphical user interface.

## Features

- Load images in various formats (PNG, JPG, JPEG, BMP, GIF)
- Extract text from images using OCR
- Translate extracted text to Korean
- Simple and intuitive GUI interface
- Command-line interface for automation and scripting

## Requirements

- Python 3.6 or higher
- Tesseract OCR must be installed on your system (see installation instructions below)
- Required Python packages (see `requirements.txt`):
  - Pillow (PIL)
  - pytesseract
  - googletrans

## Installation

### 1. Clone or download this repository

```
git clone <repository-url>
```

### 2. Install Tesseract OCR

#### Windows
1. Download the installer from [UB Mannheim's GitHub repository](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer and follow the instructions
3. Make sure to note the installation path (default is `C:\Program Files\Tesseract-OCR`)
4. Add the Tesseract installation directory to your PATH environment variable

#### macOS
```
brew install tesseract
```

#### Linux (Ubuntu/Debian)
```
sudo apt-get install tesseract-ocr
```

### 3. Install required Python packages

```
pip install -r requirements.txt
```

## Usage

### Command-line Interface

```
python image_text_translator.py <path_to_image>
```

Example:
```
python image_text_translator.py sample_image.jpg
```

### Graphical User Interface

```
python image_text_translator_gui.py
```

Using the GUI:
1. Click the "Browse..." button to select an image file
2. Click the "Process Image" button to extract text and translate it
3. The extracted text will appear in the "Extracted Text" section
4. The Korean translation will appear in the "Korean Translation" section

### Programmatic Usage

For developers who want to integrate this functionality into their own applications, an example script is provided:

```
python example_usage.py
```

This script demonstrates how to use the text extraction and translation functions programmatically. You can import these functions into your own Python applications:

```python
from example_usage import extract_text_from_image, translate_text_to_korean

# Extract text from an image
text = extract_text_from_image('path/to/your/image.jpg')

# Translate text to Korean
korean_text = translate_text_to_korean(text)

# Use the translated text in your application
print(f'Translated text: {korean_text}')
```

## Troubleshooting

### Tesseract OCR not found

If you get an error like "TesseractNotFoundError", make sure:
1. Tesseract OCR is properly installed
2. The Tesseract executable is in your system PATH

For Windows users, you can also specify the Tesseract path in your code by adding:
```python
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
```
(Adjust the path according to your installation)

### Translation issues

If you encounter issues with the translation service:
1. Make sure you have a stable internet connection
2. Check if the googletrans API has changed (it's a third-party library that might be affected by changes in Google's services)
3. Try updating the googletrans package or check for alternative versions

## License

[MIT License](LICENSE)

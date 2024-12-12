import pytesseract
from PIL import Image, ImageFilter
import cv2
import numpy as np
import matplotlib.pyplot as plt
import re
from datetime import datetime

# Set the correct path to your Tesseract executable
pytesseract.pytesseract.tesseract_cmd = r"C:\Users\romai\AppData\Local\Programs\Tesseract-OCR\tesseract.exe"

def show_image(img, title="Image"):
    """Function to display the image using matplotlib."""
    plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    plt.title(title)
    plt.axis('off')
    plt.show()

def filter_black_color(img_filtered):
    """Filter the image so all colors are turned to white except black text."""
    if len(img_filtered.shape) == 3:
        gray = cv2.cvtColor(img_filtered, cv2.COLOR_BGR2GRAY)
    else:
        gray = img_filtered
    
    _, thresholded = cv2.threshold(gray, 125, 255, cv2.THRESH_BINARY_INV)
    thresholded_inv = cv2.bitwise_not(thresholded)
    img_filtered = cv2.cvtColor(thresholded_inv, cv2.COLOR_GRAY2BGR)
    return img_filtered

def preprocess_image(image):
    """Preprocess the image by applying filters and black-color filtering."""
    if isinstance(image, Image.Image):  # Convert PIL Image to NumPy array if needed
        image = np.array(image)

    img_filtered = filter_black_color(image)
    img_processed = Image.fromarray(cv2.cvtColor(img_filtered, cv2.COLOR_BGR2RGB))
    img_rotated = img_processed.rotate(270)

    show_image(np.array(img_rotated), "Processed Image")
    return img_rotated

def extract_ticket_info(image):
    """Extract the amount, date, and location from the ticket image."""
    img = preprocess_image(image)  # Process the image (image is passed as NumPy array)
    text = pytesseract.image_to_string(img)

    # Debugging: Print the OCR output for inspection
    print(f"OCR Text: {text}")

    # Regular expressions for extracting the amount, date, and location
    amount_pattern = r'(\d+,\d{2})\s*EUR'
    date_pattern = r'(\d{2}/\d{2}/\d{2})'
    location_pattern = r'([A-Z\s]+)\s*(?:MAG|MARCHE|STORE)'

    # Search for the amount, date, and location using the regular expressions
    amount_match = re.search(amount_pattern, text)
    date_match = re.search(date_pattern, text)
    location_match = re.search(location_pattern, text)

    ticket_info = {}
    if amount_match:
        ticket_info['amount'] = amount_match.group(1).replace(',', '.')
    if date_match:
        ticket_info['date'] = datetime.strptime(date_match.group(1), "%d/%m/%y").strftime("%Y-%m-%d")
    if location_match:
        ticket_info['location'] = location_match.group(1).strip()

    # Debugging: Print the extracted ticket info
    print(f"Extracted Info: {ticket_info}")

    # Return an empty dictionary if no data is found
    return ticket_info if ticket_info else None

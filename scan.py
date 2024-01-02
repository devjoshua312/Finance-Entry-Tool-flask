from PIL import Image
import pytesseract
import re
import json

with open('funds.json', 'r') as file:
    data = json.load(file)


def extract_text_from_image(image_path):
    try:
        img = Image.open(image_path)
        text = pytesseract.image_to_string(img, lang='eng')
        return text
    except Exception as e:
        return f"Error during text extraction: {e}"

def extract_transaction_id(text):
    transaction_id_patterns = [
        re.compile(r'TXN ID:\s*(\S+)', re.DOTALL),
        re.compile(r'Transaction ID\n\n(\S+)', re.DOTALL),
    ]

    for pattern in transaction_id_patterns:
        match = pattern.search(text)
        if match:
            return match.group(1).strip()

    return None

def scan(expected_name, transaction_id):
    extracted_text = extract_text_from_image(f"receipts/{expected_name}.jpeg")

    print(extracted_text)

    if transaction_id or expected_name in extracted_text:
        data[expected_name]['recStatus'] = "Verified"
    else:
        data[expected_name]['recStatus'] = "Not Verified"

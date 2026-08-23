import re
from pdf2image import convert_from_bytes
import pypdf
import pytesseract
import os

# Set executable paths for Windows local dev; Linux (Streamlit Cloud) uses system PATH automatically
if os.name == "nt":  # "nt" means Windows
    pytesseract.pytesseract.tesseract_cmd = (
        r"C:\Program Files\Tesseract-OCR\tesseract.exe"
    )
    # Update to match your working local path
    POPPLER_PATH = r"C:\Program Files\poppler\Library\bin"
else:  # Linux / Streamlit Cloud
    POPPLER_PATH = None

def extract_text_from_pdf(pdf_file):
    # 1. Store byte payload for potential OCR stream conversion
    if isinstance(pdf_file, str):
        with open(pdf_file, "rb") as f:
            pdf_bytes = f.read()
    else:
        pdf_bytes = pdf_file.read()
        pdf_file.seek(0)  # Reset pointer for pypdf reader

    # 2. Try fast digital text extraction first
    reader = pypdf.PdfReader(pdf_file)
    text = ""
    for page in reader.pages:
        extracted = page.extract_text()
        if extracted:
            text += extracted + "\n"

    # 3. Fallback to Tesseract OCR if PDF contains no digital text
    if not text.strip():
        try:
            # Pass poppler_path if on Windows, otherwise let it default to system PATH on Linux
            if POPPLER_PATH:
                images = convert_from_bytes(pdf_bytes, poppler_path=POPPLER_PATH)
            else:
                images = convert_from_bytes(pdf_bytes)
            text = ""
            for img in images:
                text += pytesseract.image_to_string(img) + "\n"
        except Exception as e:
            text = f"Extraction Error (OCR Failed): {str(e)}"

    return text


def parse_spec_data(raw_text):
    data = {
        "product_name": "Unknown",
        "abv": "Unknown",
        "net_volume": "Unknown",
        "french_label": "Unknown",
    }

    # Extract Product Name
    name_match = re.search(r"Product Name:\s*(.*)", raw_text)
    if name_match:
        data["product_name"] = name_match.group(1).strip()

    # Extract ABV %
    abv_match = re.search(r"Alcohol By Volume \(ABV\):\s*(.*)", raw_text)
    if abv_match:
        data["abv"] = abv_match.group(1).strip()

    # Extract Net Volume
    vol_match = re.search(r"Net Volume:\s*(.*)", raw_text)
    if vol_match:
        data["net_volume"] = vol_match.group(1).strip()

    # Extract French Label status
    french_match = re.search(r"French Label Text Included:\s*(.*)", raw_text)
    if french_match:
        data["french_label"] = french_match.group(1).strip()

    return data


def check_compliance(parsed_data):
    checklist = []

    # Rule 1: French Labeling Compliance
    french_text = parsed_data.get("french_label", "").lower()
    if "oui" in french_text or "yes" in french_text:
        checklist.append(
            {
                "rule": "Bilingual Packaging (French Text)",
                "status": "PASS",
                "details": "French label text present.",
            }
        )
    else:
        checklist.append(
            {
                "rule": "Bilingual Packaging (French Text)",
                "status": "FAIL",
                "details": "Missing required French translation.",
            }
        )

    # Rule 2: Maximum ABV Check (< 15% threshold for standard retail listing)
    abv_str = parsed_data.get("abv", "").replace("%", "").strip()
    try:
        abv_val = float(abv_str)
        if abv_val <= 15.0:
            checklist.append(
                {
                    "rule": "Standard Retail ABV Limit (<= 15%)",
                    "status": "PASS",
                    "details": f"ABV is {abv_val}%.",
                }
            )
        else:
            checklist.append(
                {
                    "rule": "Standard Retail ABV Limit (<= 15%)",
                    "status": "FAIL",
                    "details": f"ABV of {abv_val}% exceeds standard limit. Special permit required.",
                }
            )
    except ValueError:
        checklist.append(
            {
                "rule": "Standard Retail ABV Limit (<= 15%)",
                "status": "WARNING",
                "details": "Could not parse numerical ABV value.",
            }
        )

    # Rule 3: Net Volume Unit Standard (Must be mL or L format)
    vol_str = parsed_data.get("net_volume", "")
    if "mL" in vol_str or "L" in vol_str:
        checklist.append(
            {
                "rule": "Standard Packaging Volume Format",
                "status": "PASS",
                "details": f"Valid volume unit format ({vol_str}).",
            }
        )
    else:
        checklist.append(
            {
                "rule": "Standard Packaging Volume Format",
                "status": "FAIL",
                "details": "Non-standard volume units detected.",
            }
        )

    return checklist
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas


def create_pdf(filename, title, abv, net_vol, desc, french_label):
    c = canvas.Canvas(filename, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 730, f"VENDOR PRODUCT SPECIFICATION: {title}")

    c.setFont("Helvetica", 12)
    c.drawString(100, 690, f"Product Name: {title}")
    c.drawString(100, 670, f"Alcohol By Volume (ABV): {abv}")
    c.drawString(100, 650, f"Net Volume: {net_vol}")
    c.drawString(100, 630, f"Description: {desc}")
    c.drawString(100, 610, f"French Label Text Included: {french_label}")

    c.save()


# 1. Compliant Spec Sheet (ANBL Rules Pass)
create_pdf(
    "compliant_sample.pdf",
    "Fundy Bay Craft IPA",
    "6.5%",
    "473 mL",
    "Local craft IPA brewed in New Brunswick.",
    "Oui - Biere Artisanale",
)

# 2. Non-Compliant Spec Sheet (Missing French Label & Invalid Formatting)
create_pdf(
    "non_compliant_sample.pdf",
    "High Peak Imperial Stout",
    "16.5%",
    "0.5 L",
    "Strong dark stout.",
    "None",
)

print("Mock PDFs generated successfully!")
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import pdfplumber

def generate_certificate(output_path, customer_id, customer_name, energy_source, capacity_generated, powerhouse_id, powerhouse_name, date_of_claim, institute_logo_path):
    # Create a PDF document
    doc = SimpleDocTemplate(output_path, pagesize=letter)

    # Create a list to hold the elements of the PDF
    elements = []

    # Add institute logo and institute name
    if institute_logo_path:
        logo = Image(institute_logo_path, width=150, height=150)
        elements.append(logo)

    # Add institute details
    institute_style = ParagraphStyle(
        "InstituteStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=15,
        spaceAfter=10,
    )
    capacity_generated_divided = int(capacity_generated) / 1000
    institute_text = f"<b>Customer Details:</b><br/>\
                    Customer Name: <b>{customer_name}</b><br/>\
                    Customer ID: <b>{customer_id}</b><br/>\
                    Value of RECs:<b>{capacity_generated_divided}</b>"
    institute = Paragraph(institute_text, institute_style)
    elements.append(institute)
    elements.append(Spacer(1, 12))

    # Add header
    header_style = ParagraphStyle(
        "HeaderStyle",
        parent=getSampleStyleSheet()["Title"],
        fontName="Helvetica-Bold",
        fontSize=18,
        spaceAfter=20,
    )
    header_text = "<b>Renewable Energy Certificate</b>"
    header = Paragraph(header_text, header_style)
    elements.append(header)

    # Add hero section
    hero_style = ParagraphStyle(
        "HeroStyle",
        parent=getSampleStyleSheet()["BodyText"],
        fontSize=12,
        spaceAfter=12,
        leading=15,
    )
    hero_text = f"<div>This certificate acknowledges <b>{customer_name}</b>'s commitment to sustainable energy practices and their contribution to the utilization of <b>{energy_source}</b> as a renewable energy source.</div><br/><br/>\
          <div>With a generating capacity of <b>{capacity_generated}</b>, this certificate affirms <b>{customer_name}</b>'s role in promoting environmental responsibility and supporting clean energy initiatives.</div><br/><br/>\
            <div>Stored securely within <b>{powerhouse_name}</b>'s powerhouse, this certificate represents a significant milestone in the journey towards a greener and more sustainable future.<div><br/><br/><br/>\
        "

    hero = Paragraph(hero_text, hero_style)
    elements.append(hero)

    # Add footer
    footer_style = ParagraphStyle(
        "FooterStyle",
        parent=getSampleStyleSheet()["BodyText"],
        fontSize=10,
        spaceBefore=20,
        leading=15,
        alignment=1
    )
    footer_text = f"Verified - {date_of_claim}"
    footer = Paragraph(footer_text, footer_style)
    elements.append(footer)

    # Build the PDF document
    doc.build(elements)
    with open(output_path, "rb") as file:
        pdf_data = file.read()

    print(f"Certificate generated and saved at: {output_path}")
    return pdf_data

def extract_certificate(pdf_path):
    with pdfplumber.open(pdf_path) as pdf:
        # Extract text from each page
        text = ""
        for page in pdf.pages:
            text += page.extract_text()
        lines = text.splitlines()
        customer_name=lines[1][15:]
        org_name = lines[0]
        candidate_name = lines[3]
        customer_id = lines[5]
        energy_source = lines[-1]

        return (candidate_name)


from fpdf import FPDF

def generate_pdf(logs):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, txt="Certificate Renewal Report", ln=1, align="C")
    for entry in logs:
        line = f"{entry['timestamp']} - {entry['domain']} - {entry['status']}"
        pdf.cell(200, 10, txt=line, ln=1)
    path = "cert_report.pdf"
    pdf.output(path)
    return path

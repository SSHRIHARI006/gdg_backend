import io
import zipfile
import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Configure API
API_KEY = "AIzaSyAlNMExiThkT0dd3MrK9-dR_A4ZEtIC8EY"
genai.configure(api_key=API_KEY)
llm = genai.GenerativeModel("gemini-1.5-pro")

# Register Arial Unicode Font
pdfmetrics.registerFont(TTFont("ArialUnicode", "C:\\gdg website\\backend\\ezyZip\\arial-unicode-ms.ttf"))

# Load Default Styles
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="CustomTitle", fontName="ArialUnicode", fontSize=20, spaceAfter=14, alignment=1, bold=True))
styles.add(ParagraphStyle(name="CustomBody", fontName="ArialUnicode", fontSize=12, spaceAfter=8))
styles.add(ParagraphStyle(name="BulletPoint", fontName="ArialUnicode", fontSize=12, spaceAfter=6, leftIndent=20))

def generate_content(prompt):
    """Generates text content using Gemini AI."""
    response = llm.generate_content(prompt)
    return response.text if response else "No content generated."

def create_pdf(title, content):
    """Generates a PDF file in memory and returns it as a BytesIO object."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4)
    elements = [Paragraph(title, styles["CustomTitle"]), Spacer(1, 14)]

    content = content.replace("**", "")
    paragraphs = content.split("\n\n")

    for para in paragraphs:
        para = para.strip()
        if not para:
            continue

        if para.startswith(("•", "-", "*")):
            bullet_points = [ListItem(Paragraph(p.strip("•- "), styles["BulletPoint"])) for p in para.split("\n") if p]
            elements.append(ListFlowable(bullet_points, bulletType="bullet"))
        elif para[0].isdigit() and "." in para:
            numbered_items = [ListItem(Paragraph(p.strip(), styles["BulletPoint"])) for p in para.split("\n") if p]
            elements.append(ListFlowable(numbered_items, bulletType="1"))
        else:
            elements.append(Paragraph(para, styles["CustomBody"]))

        elements.append(Spacer(1, 8))

    doc.build(elements)
    buffer.seek(0)  # Move to the start of the buffer
    return buffer  # ✅ Return memory stream instead of saving as a file

def generate_study_material(topic):
    """Generates PDFs and returns them as a ZIP file."""
    # Generate Content
    notes = generate_content(f"Provide well-structured study notes on {topic}. Ensure clarity and bullet points.")
    assignment = generate_content(f"Generate 10 assignment questions for {topic}. Number them clearly.")
    test = generate_content(f"Create 10 multiple-choice test questions for {topic}. Clearly format them.")

    # Generate PDFs in memory
    pdf_files = {
        "Notes.pdf": create_pdf(f"{topic} - Study Notes", notes),
        "Assignment.pdf": create_pdf(f"{topic} - Assignment Questions", assignment),
        "Test.pdf": create_pdf(f"{topic} - Test Questions", test)
    }

    # Create a ZIP file in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, "w") as zipf:
        for filename, pdf_buffer in pdf_files.items():
            zipf.writestr(filename, pdf_buffer.getvalue())

    zip_buffer.seek(0)  # Move to the start of the buffer
    return zip_buffer  # ✅ Return ZIP file buffer

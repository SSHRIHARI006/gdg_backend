import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, ListFlowable, ListItem
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics

# Configure API
API_KEY = "AIzaSyCq3J2kgh-L_TCnZ2jbp681X7k0VGPPuC0"
genai.configure(api_key=API_KEY)
llm = genai.GenerativeModel("gemini-1.5-pro")

# Register Arial Unicode Font
pdfmetrics.registerFont(TTFont("ArialUnicode", "C:\\gdg website\\backend\\ezyZip\\arial-unicode-ms.ttf"))

# Load Default Stylesheet
styles = getSampleStyleSheet()

# Define Custom Styles
styles.add(ParagraphStyle(name="CustomTitle", fontName="ArialUnicode", fontSize=20, spaceAfter=14, alignment=1, bold=True))  # Centered Title
styles.add(ParagraphStyle(name="CustomHeading", fontName="ArialUnicode", fontSize=16, spaceAfter=10, bold=True))
styles.add(ParagraphStyle(name="CustomBody", fontName="ArialUnicode", fontSize=12, spaceAfter=8))
styles.add(ParagraphStyle(name="BulletPoint", fontName="ArialUnicode", fontSize=12, spaceAfter=6, leftIndent=20))

# Function to Generate Content from AI
def generate_content(prompt):
    response = llm.generate_content(prompt)
    return response.text if response else "No content generated."

# Function to Create Well-Formatted PDFs
def create_pdf(filename, title, content):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = [Paragraph(title, styles["CustomTitle"]), Spacer(1, 14)]

    # Split into Sections
    content = content.replace("**", "")
    paragraphs = content.split("\n\n")
    for para in paragraphs:
        if para == '':
            continue
        para = para.strip()
        
        if para.startswith("•") or para.startswith("-") or para.startswith("*"):
            # Handle bullet points
            bullet_points = [ListItem(Paragraph(p.strip("•- "), styles["BulletPoint"])) for p in para.split("\n") if p]
            elements.append(ListFlowable(bullet_points, bulletType="bullet"))
        elif para[0].isdigit() and "." in para:
            # Handle numbered lists
            numbered_items = [ListItem(Paragraph(p.strip(), styles["BulletPoint"])) for p in para.split("\n") if p]
            elements.append(ListFlowable(numbered_items, bulletType="1"))
        else:
            # Regular paragraph
            elements.append(Paragraph(para, styles["CustomBody"]))

        elements.append(Spacer(1, 8))

    doc.build(elements)
    print(f"{filename} generated successfully.")

# Main Function to Generate All PDFs
def generate_study_material(topic):
    # Generate Content
    notes = generate_content(f"Provide well-structured study notes on {topic}. Ensure clarity and bullet points.")
    assignment = generate_content(f"Generate 10 assignment questions for {topic}. Number them clearly.")
    test = generate_content(f"Create 10 multiple-choice test questions for {topic}. Clearly format them.")

    # Generate PDFs
    create_pdf("Notes.pdf", f"{topic} - Study Notes", notes)
    create_pdf("Assignment.pdf", f"{topic} - Assignment Questions", assignment)
    create_pdf("Test.pdf", f"{topic} - Test Questions", test)

# Run
topic = input("Enter the topic: ")
generate_study_material(topic)
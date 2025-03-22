import google.generativeai as genai
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfbase import pdfmetrics
import os
# Configure API
API_KEY = "AIzaSyCXFb8KyLG0DBz9dgcnVt__GFwrVxNJl48"
genai.configure(api_key=API_KEY)
llm = genai.GenerativeModel("gemini-1.5-pro")

font_path = "C:\\gdg website\\backend\\ezyZip\\arial-unicode-ms.ttf"

if os.path.exists(font_path):
    print("✅ Font file found at:", os.path.abspath(font_path))
else:
    print("❌ Font file NOT found! Check the filename and path.")

# Register Arial Unicode Font
pdfmetrics.registerFont(TTFont("ArialUnicode", font_path))

# Load Default Stylesheet
styles = getSampleStyleSheet()

# Define Custom Styles (Avoid Conflict with Existing Styles)
styles.add(ParagraphStyle(name="CustomTitle", fontName="ArialUnicode", fontSize=18, spaceAfter=12, bold=True))
styles.add(ParagraphStyle(name="CustomHeading", fontName="ArialUnicode", fontSize=14, spaceAfter=8, bold=True))
styles.add(ParagraphStyle(name="CustomBody", fontName="ArialUnicode", fontSize=12, spaceAfter=6))

# Function to Generate Content from AI
def generate_content(prompt):
    response = llm.generate_content(prompt)
    return response.text if response else "No content generated."

# Function to Create Well-Formatted PDFs
def create_pdf(filename, title, content):
    doc = SimpleDocTemplate(filename, pagesize=A4)
    elements = [Paragraph(title, styles["CustomTitle"]), Spacer(1, 12)]
    
    for paragraph in content.split("\n\n"):
        elements.append(Paragraph(paragraph.strip(), styles["CustomBody"]))
        elements.append(Spacer(1, 6))

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
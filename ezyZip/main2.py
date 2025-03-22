from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer
import google.generativeai as genai

# ✅ Configure Google Gemini API
genai.configure(api_key="AIzaSyDUVdHhRIX7Q6ctGUPjYrOL69C2WX97fzY")

# ✅ Function to generate AI-based content
def generate_content(topic, content_type):
    """Generates Notes, Assignments, and Tests using Gemini AI"""
    
    prompts = {
        "notes": f"""
        Generate well-structured notes on "{topic}". The notes should include:
        - Introduction: Briefly explain the topic.
        - Key Concepts: Define all important terms.
        - Formulas & Equations: Include necessary formulas.
        - Examples & Diagrams: Use ASCII diagrams where applicable.
        - Applications & Real-world Use: How is this concept used in real life?
        Keep explanations clear and concise.
        """,

        "assignments": f"""
        Generate 5 assignment questions on "{topic}". Ensure:
        - 2 Theory Questions (Explain concepts, derivations, or reasoning)
        - 2 Application-based Questions (Real-world problem-solving)
        - 1 Coding/Mathematical Problem (If applicable)
        Provide detailed, structured questions.
        """,

        "tests": f"""
        Generate a 5-question multiple-choice test (MCQ) for "{topic}". Each question should have:
        - 4 answer options (A, B, C, D)
        - The correct answer marked separately at the end.
        Ensure the questions cover both theory and application.
        """
    }
    
    model = genai.GenerativeModel("gemini-1.5-pro")
    response = model.generate_content(prompts[content_type])
    
    return response.text if response and response.text else "Error generating content."

# ✅ Function to save structured content into a PDF using ReportLab
def save_to_pdf(notes, assignments, tests, filename):
    doc = SimpleDocTemplate(filename, pagesize=letter)
    styles = getSampleStyleSheet()
    content = []

    # ✅ Add Notes
    content.append(Paragraph("<b>📌 Notes</b>", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(notes, styles['BodyText']))
    content.append(Spacer(1, 24))

    # ✅ Add Assignments
    content.append(Paragraph("<b>📌 Assignments</b>", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(assignments, styles['BodyText']))
    content.append(Spacer(1, 24))

    # ✅ Add Tests
    content.append(Paragraph("<b>📌 Tests</b>", styles['Title']))
    content.append(Spacer(1, 12))
    content.append(Paragraph(tests, styles['BodyText']))
    content.append(Spacer(1, 24))

    # ✅ Generate PDF
    doc.build(content)
    print(f"✅ PDF saved as {filename}")

# ✅ MAIN FUNCTION
if __name__ == "__main__":
    topic = input("Enter the topic: ")

    print("Generating AI-powered content... 🚀")
    notes = generate_content(topic, "notes")
    assignments = generate_content(topic, "assignments")
    tests = generate_content(topic, "tests")

    # ✅ Save everything into a single well-structured PDF
    save_to_pdf(notes, assignments, tests, f"{topic}_StudyMaterial.pdf")
    print("📄 PDF Generated Successfully!")

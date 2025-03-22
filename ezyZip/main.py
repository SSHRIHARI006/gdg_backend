import google.generativeai as genai
from fpdf import FPDF
import os

# 🔹 Configure Google Gemini API (Replace with your actual API key)
# api_key = "AIzaSyDUVdHhRIX7Q6ctGUPjYrOL69C2WX97fzY" 
api_key = "AIzaSyCq3J2kgh-L_TCnZ2jbp681X7k0VGPPuC0"
genai.configure(api_key=api_key)

# ✅ Custom PDF class with proper formatting (Using Arial Unicode)
class PDF(FPDF):
    def header(self):
        """Header for each page"""
        self.set_font("ArialUnicodeMS", "", 16)  # No bold font
        self.cell(0, 10, "AI-Generated Study Material", ln=True, align="C")
        self.ln(10)

    def chapter_title(self, title):
        """Formats chapter titles"""
        self.set_font("ArialUnicodeMS", "", 14)  # No bold font
        self.cell(0, 8, title, ln=True, align="L")
        self.ln(4)

    def chapter_body(self, body):
        """Handles paragraph text properly"""
        self.set_font("ArialUnicodeMS", "", 12)  # No bold font
        self.multi_cell(0, 7, body)
        self.ln(4)

    def add_code_block(self, code):
        """Formats code blocks"""
        self.set_font("Courier", size=10)
        self.set_fill_color(230, 230, 230)  # Light gray background
        self.multi_cell(0, 7, code, border=1, fill=True)
        self.ln(4)

# ✅ Function to save structured content into a properly formatted PDF
def save_to_pdf(notes, assignments, tests, filename):
    """Formats & Saves Notes, Assignments & Tests into a readable PDF"""
    
    pdf = PDF()
    
    font_path = "C:\\gdg website\\backend\\ezyZip\\arial-unicode-ms.ttf"  # Ensure this file is in the same directory

    # if not os.path.exists(font_path):
    #     raise FileNotFoundError(f"⚠️ Font file not found: {font_path}. Please add the file!")

    # ✅ Register Arial Unicode Font
    pdf.add_font(family="ArialUnicodeMS", fname = font_path, uni=True)
    pdf.set_font("ArialUnicodeMS", "", 12)

    pdf.add_page()


    # ✅ Properly handle headings, paragraphs & code blocks
    pdf.chapter_title("📌 Notes")
    format_content(pdf, notes)

    pdf.chapter_title("📌 Assignments")
    format_content(pdf, assignments)

    pdf.chapter_title("📌 Tests")
    format_content(pdf, tests)

    pdf.output(filename, "F")
    print(f"✅ Saved as {filename}")

# 🔹 Function to format content properly
def format_content(pdf, content):
    """Handles text formatting, headings & code blocks"""
    sections = content.split("\n\n")
    for section in sections:
        section = section.strip()
        if not section:
            continue

        # Title Handling
        if ":" in section and len(section.split()) < 10:
            title, body = section.split(":", 1)
            pdf.chapter_title(title.strip())
            pdf.chapter_body(body.strip())

        # Code Blocks Handling
        elif "```" in section:
            parts = section.split("```")
            for i in range(len(parts)):
                if i % 2 == 0:
                    pdf.chapter_body(parts[i].strip())
                else:
                    pdf.add_code_block(parts[i].strip())

        else:
            pdf.chapter_body(section)

# ✅ Function to generate AI-based content using Gemini API
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

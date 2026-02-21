Project name: RESUGLOW
Basic details:
Team name: Blackjacks
Team members:
Member 1:MInha A S - Muthoot Institute of Technology and Science
Member 2:Jithya Suresh - Muthoot Institute of Technology and Science

Hosted project link:
Project Description: 
   Resume AI is a web-based application that analyzes resumes using AI to provide insights and improve candidate evaluation.
   It extracts key information from PDF resumes and helps match skills with job requirements. The system enhances recruitment efficiency through automated resume screening and intelligent feedback.

The problem statement:
Job seekers often don’t know how effective their resumes are, and recruiters spend too much time reviewing them manually. 
Our solution uses AI to analyze resumes and provide feedback to improve screening and job readiness.

The Solution:
The system automates resume screening by extracting text from PDF resumes using pdfplumber and analyzing it with AI to identify key skills and qualifications.
It compares candidate data with job requirements to generate insights and improve hiring efficiency. This reduces manual effort and speeds up the recruitment process.

Technical Details:
Technology/components used:
For software:

Languages Used:
Python

Frameworks Used:
Streamlit
grok

Libraries Used:
pdfplumber
OpenAI (for AI analysis, if used)
re (Regular Expressions, if used for text processing)

Tools Used:
VS Code
Git & GitHub
Python (pip for package management)

Features:
Automated Resume Parsing – Extracts text and key details directly from PDF resumes.
AI-Based Skill Analysis – Identifies and evaluates candidate skills using intelligent analysis.
Job Matching System – Compares resume content with job descriptions for better fit assessment.
User-Friendly Web Interface – Simple and interactive interface for uploading and analyzing resumes.

IMPLEMENTATION

Installation :

pip install streamlit pdfplumber groq

Run:

streamlit run app.py

PROJECT DOCUMENTATION
for software

Screenshots:
![WhatsApp Image 2026-02-21 at 08 44 09](https://github.com/user-attachments/assets/993720d0-2c77-489b-8cba-d1fe8604a4f0)
![WhatsApp Image 2026-02-21 at 08 46 12](https://github.com/user-attachments/assets/ea530ec2-9265-4390-84b6-dc43cf064322)
![WhatsApp Image 2026-02-21 at 08 47 29](https://github.com/user-attachments/assets/b8b5880b-0a33-448e-956f-64650dab33e6)
![WhatsApp Image 2026-02-21 at 08 47 52](https://github.com/user-attachments/assets/85ce3960-3a74-4074-a2a6-2babefaf4fa2)
![WhatsApp Image 2026-02-21 at 08 48 49](https://github.com/user-attachments/assets/a3236ec4-5531-4d1b-a5fe-a5d6261f4f18)
![WhatsApp Image 2026-02-21 at 08 49 13](https://github.com/user-attachments/assets/d1477924-2bcf-462e-be66-2a36167bdabe)

SYSTEM ARCHITECTURE - EXPLANATION

Components:

Streamlit frontend (UI)
PDF parser (pdfplumber)
Groq API (LLM for analysis)
Processing logic
Output feedback display

Data Flow:

User uploads resume → Text extracted → Sent to AI → Analysis generated → Results shown

APPLICATION WORKFLOW - EXPLANATION

User uploads resume PDF
System extracts text
Sends content to AI model
AI evaluates skills, structure, gaps
Feedback displayed to user

ADDITIONAL DOCUMENTATION

API Documentation
http://localhost:8501/

Groq API (external service)

ENDPOINT 1 — Upload Resume & Analyze

POST /analyze

Description:
Uploads a resume PDF and analyzes it using AI to generate feedback, score, and suggestions.

Request:
Content-Type: multipart/form-data

File: resume.pdf

Response
{
  "status": "success",
  "score": 85,
  "feedback": "Strong technical skills but improve project descriptions.",
  "suggestions": [
    "Add quantified achievements",
    "Improve summary section",
    "Highlight key skills"
  ]
}

ENDPOINT 2 — Extract Resume Text

POST /extract-text

Description:
Extracts raw text from uploaded resume PDF.

Request:
Content-Type: multipart/form-data

File: resume.pdf

Response:
{
  "status": "success",
  "text": "Extracted resume content..."
}

ENDPOINT 3— Health Check

GET /health

Description
Checks whether the service is running.

Response
{
  "status": "running"
}

COMMAND REFERENCE (Adapted for Streamlit App)
🔹 Basic Usage

Run the application locally using:

streamlit run resumm.py

This starts the web interface where users can upload resumes and view AI-generated analysis.

🔹 Available Commands

streamlit run resumm.py — Launch the resume analysis web app

streamlit cache clear — Clear cached data if needed

pip install -r requirements.txt — Install dependencies

🔹 Options

--server.port — Specify custom port

--server.address — Bind to a specific IP address

--help — Show Streamlit help

Example:

streamlit run resumm.py --server.port 8501
🔹 Examples
Example 1 — Start App
streamlit run resumm.py

Output:

Local URL: http://localhost:8501
App ready to analyze resumes


Example 2 — Install Dependencies
pip install pdfplumber streamlit groq

Output:

Dependencies installed successfully


Project Demo
Video

(Add your demo video link here — YouTube / Drive)

What the video shows:

Uploading a resume
AI analysis process
Feedback and scoring
UI walkthrough

ADDITIONAL DEMOS:

GitHub repository: https://github.com/minhs-naj/resuglow

AI Tools Used
Tool Used

ChatGPT — debugging and documentation help
Groq API — AI resume analysis

Purpose

Assisted in code refinement
Generated feedback logic
Helped with documentation writing

Key Prompts Used:

“Analyze resume and give suggestions”
“Improve resume scoring logic”
“Explain Python errors”
“Generate documentation sections”

Human Contributions:

Project idea and design
Integration of resume parsing
UI decisions in Streamlit
Testing and debugging
Presentation preparation


HOSTING 
https://resuglow-xz9clxmsktfer6ybvn4p9z.streamlit.app/

# 🧠 Smart Tutor

Smart Tutor is an AI-powered learning platform built using **Flask**, **Python**, **HTML/CSS**, and **Hugging Face NLP models**. It helps students study smarter by generating quizzes, answering questions from paragraphs, chatting with PDFs, and tracking learning progress.

---

# 🚀 Features

## 📘 AI Question Answering

Paste any paragraph and ask questions instantly.

### Example

**Paragraph:**  
Machine Learning is a branch of AI that enables systems to learn from data.

**Question:**  
What is Machine Learning?

**Answer:**  
Machine Learning is a branch of AI.

---

## 📝 Instant Quiz Generator

Generate quiz questions automatically from any paragraph.

### Example Output

- What is Machine Learning?  
- How do systems learn?  
- Why is data important?  

---

## 📄 PDF Learning Assistant

Upload PDFs like:

- Notes  
- Chapters  
- Books  
- Assignments  
- Study Material  

Then interact with them using AI.

---

## 💬 PDF Chat

Ask questions from uploaded PDF files.

### Examples

- Summarize chapter 1  
- Explain thermodynamics  
- Give important MCQs  

---

## 📊 Dashboard

Track:

- Total questions asked  
- Quiz attempts  
- PDF uploads  
- Learning activity  

---

## 👤 User System

- Register Account  
- Login  
- Edit Profile  
- Personal Dashboard  

---

# 🛠️ Tech Stack

## Backend

- Python  
- Flask  
- SQLite Database  

## Frontend

- HTML5  
- CSS3  
- Jinja2 Templates  
- Font Awesome  

## AI / NLP

- Hugging Face Transformers  
- PyTorch  

## File Processing

- PyPDF2  

---

# 📁 Project Structure

```bash
smart_tutor/
│── app.py
│── database.db
│── requirements.txt
│── LICENSE
│── README.md
│
├── static/
│   └── style.css
│
├── templates/
│   ├── base.html
│   ├── index.html
│   ├── login.html
│   ├── register.html
│   ├── dashboard.html
│   ├── edit_profile.html
│   ├── quiz.html
│   ├── result.html
│   ├── upload_pdf.html
│   ├── pdf_chat.html
│   └── pdf_qa.html
│
├── uploads/
└── venv/
```

---

# ⚙️ Installation Guide

## 1️⃣ Clone Repository

```bash
git clone https://github.com/yourusername/smart_tutor.git
cd smart_tutor
```

## 2️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### Activate Environment

**Windows**

```bash
venv\Scripts\activate
```

**Linux / Mac**

```bash
source venv/bin/activate
```

## 3️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

## 4️⃣ Run Project

```bash
python app.py
```

## 5️⃣ Open Browser

```bash
http://127.0.0.1:5000
```

---

# 📦 requirements.txt

```txt
flask
transformers
torch
PyPDF2
werkzeug
```

---

# 🧠 AI Setup Example

```python
from transformers import pipeline

qa_model = pipeline("question-answering")
quiz_model = pipeline("text2text-generation")
```

---

# 🗄 Database

Uses SQLite database:

```bash
database.db
```

Stores:

- Users  
- Login Data  
- Quiz Scores  
- Progress Data  

---

# 🔐 Authentication

Includes:

- Login Page  
- Register Page  
- Session Management  
- Profile Editing  

---

# 📷 Pages Included

## Home

Main dashboard with all tools.

## Login

Secure user login page.

## Register

Create new account.

## Dashboard

View progress and stats.

## Quiz

Generate quiz instantly.

## Result

Quiz results page.

## Upload PDF

Upload documents.

## PDF Chat

Chat with uploaded file.

## Edit Profile

Update user details.

---

# 🌟 Use Cases

Perfect for:

- Engineering Students  
- UPSC Students  
- Teachers  
- School Students  
- Competitive Exams  
- Self Learners  

---

# 🔥 Future Upgrades

- JWT Authentication  
- Dark / Light Mode  
- Voice Tutor  
- Notes Summarizer  
- OCR Scanner  
- Flashcards Generator  
- AI Interview Prep  
- Study Planner  

---

# 🐛 Common Errors

## Transformers Slow Download

First run downloads model files.

## Torch Error

```bash
pip install torch --upgrade
```

## PDF Upload Error

Check:

- uploads folder exists  
- PDF extension allowed  
- Max file size limit  

---

# 🤝 Contribution

Contributions are welcome.

1. Fork repository  
2. Create new branch  
3. Commit changes  
4. Push branch  
5. Open Pull Request  

---

# 👨‍💻 Author

**Prakhar**  
Engineering Student | Python Developer | AI Builder

---

# 📜 License

MIT License

---

# ⭐ Support

If you like this project:

⭐ Star Repository  
🍴 Fork Project  
📢 Share With Friends  

---

# 💡 Tagline

**Smart Tutor – Your Personal AI Study Partner**
# ============================================================
# SMART TUTOR AI - FULL CLEAN app.py
# Login/Register + Dashboard + Quiz + PDF Upload + PDF QA
# ============================================================

from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_login import (
    LoginManager, UserMixin,
    login_user, login_required,
    logout_user, current_user
)
from werkzeug.security import generate_password_hash, check_password_hash
from transformers import pipeline
import sqlite3
import os
import fitz   # PyMuPDF

# ============================================================
# APP CONFIG
# ============================================================

app = Flask(__name__)
app.secret_key = "secret123"

DB = "database.db"
UPLOAD_FOLDER = "uploads"

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# ============================================================
# LOGIN MANAGER
# ============================================================

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

# ============================================================
# AI MODELS
# ============================================================

# Question Answering Model
qa = pipeline(
    "question-answering",
    model="deepset/roberta-base-squad2"
)

# Question Generation Model
qg = pipeline(
    "text2text-generation",
    model="valhalla/t5-small-qg-hl",
    use_fast=False
)

# ============================================================
# DATABASE INIT
# ============================================================

def init_db():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    # Users Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        fullname TEXT,
        username TEXT UNIQUE,
        email TEXT UNIQUE,
        password TEXT
    )
    """)

    # Quiz Scores Table
    cur.execute("""
    CREATE TABLE IF NOT EXISTS scores(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user_id INTEGER,
        score INTEGER,
        total INTEGER
    )
    """)

    con.commit()
    con.close()

# ============================================================
# USER CLASS
# ============================================================

class User(UserMixin):

    def __init__(self, id, username, fullname):
        self.id = id
        self.username = username
        self.fullname = fullname


@login_manager.user_loader
def load_user(user_id):

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT id, username, fullname FROM users WHERE id=?",
        (user_id,)
    )

    row = cur.fetchone()
    con.close()

    if row:
        return User(row[0], row[1], row[2])

    return None

# ============================================================
# HOME PAGE
# ============================================================

@app.route("/")
@login_required
def home():
    return render_template("index.html")

# ============================================================
# REGISTER
# ============================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        fullname = request.form["fullname"]
        username = request.form["username"]
        email = request.form["email"]
        password = request.form["password"]
        confirm = request.form["confirm_password"]

        # Password Match Check
        if password != confirm:
            flash("Passwords do not match")
            return redirect(url_for("register"))

        hashed = generate_password_hash(password)

        con = sqlite3.connect(DB)
        cur = con.cursor()

        try:
            cur.execute(
                """
                INSERT INTO users(fullname, username, email, password)
                VALUES(?,?,?,?)
                """,
                (fullname, username, email, hashed)
            )

            con.commit()
            flash("Registration successful")
            return redirect(url_for("login"))

        except:
            flash("Username or Email already exists")

        finally:
            con.close()

    return render_template("register.html")

# ============================================================
# LOGIN
# ============================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        user_input = request.form["username"]
        password = request.form["password"]

        con = sqlite3.connect(DB)
        cur = con.cursor()

        cur.execute(
            """
            SELECT id, username, fullname, password
            FROM users
            WHERE username=? OR email=?
            """,
            (user_input, user_input)
        )

        row = cur.fetchone()
        con.close()

        if row and check_password_hash(row[3], password):
            login_user(User(row[0], row[1], row[2]))
            return redirect(url_for("dashboard"))

        flash("Invalid credentials")

    return render_template("login.html")

# ============================================================
# LOGOUT
# ============================================================

@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for("login"))

# ============================================================
# DASHBOARD
# ============================================================

@app.route("/dashboard")
@login_required
def dashboard():

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT score,total FROM scores WHERE user_id=?",
        (current_user.id,)
    )

    rows = cur.fetchall()
    con.close()

    quizzes = len(rows)
    total = sum(r[1] for r in rows) if rows else 0
    score = sum(r[0] for r in rows) if rows else 0

    acc = round((score / total) * 100, 2) if total else 0

    return render_template(
        "dashboard.html",
        quizzes=quizzes,
        acc=acc
    )

# ============================================================
# EDIT PROFILE
# ============================================================

@app.route("/edit-profile", methods=["GET", "POST"])
@login_required
def edit_profile():

    if request.method == "POST":

        fullname = request.form["fullname"]
        email = request.form["email"]

        con = sqlite3.connect(DB)
        cur = con.cursor()

        cur.execute(
            """
            UPDATE users
            SET fullname=?, email=?
            WHERE id=?
            """,
            (fullname, email, current_user.id)
        )

        con.commit()
        con.close()

        flash("Profile Updated")
        return redirect(url_for("dashboard"))

    return render_template("edit_profile.html")

# ============================================================
# ASK QUESTION FROM PARAGRAPH
# ============================================================

@app.route("/ask", methods=["POST"])
@login_required
def ask():

    paragraph = request.form["paragraph"]
    question = request.form["question"]

    result = qa(
        question=question,
        context=paragraph
    )

    return render_template(
        "index.html",
        answer=result["answer"],
        paragraph=paragraph
    )

# ============================================================
# GENERATE QUIZ
# ============================================================

@app.route("/quiz", methods=["POST"])
@login_required
def quiz():

    paragraph = request.form["paragraph"]

    # Split paragraph into sentences
    sents = [
        s.strip()
        for s in paragraph.split(".")
        if s.strip()
    ][:5]

    questions = []

    for s in sents:

        try:
            q = qg(
                f"generate question: {s}",
                max_length=48
            )[0]["generated_text"]

        except:
            q = "What is stated in the paragraph?"

        questions.append((q, s))

    session["answers"] = [x[1] for x in questions]

    return render_template(
        "quiz.html",
        questions=questions
    )

# ============================================================
# SUBMIT QUIZ
# ============================================================

@app.route("/submit", methods=["POST"])
@login_required
def submit():

    answers = session.get("answers", [])

    score = 0
    feedback = []

    for i, ans in enumerate(answers):

        user = request.form.get(f"a{i}", "").lower().strip()

        ok = user in ans.lower()

        if ok:
            score += 1

        feedback.append({
            "user": user,
            "correct": ans,
            "status": ok
        })

    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        """
        INSERT INTO scores(user_id, score, total)
        VALUES(?,?,?)
        """,
        (current_user.id, score, len(answers))
    )

    con.commit()
    con.close()

    return render_template(
        "result.html",
        score=score,
        total=len(answers),
        feedback=feedback
    )

# ============================================================
# PDF UPLOAD
# ============================================================

@app.route("/upload-pdf", methods=["GET", "POST"])
@login_required
def upload_pdf():

    if request.method == "POST":

        file = request.files.get("pdf")

        if not file or file.filename == "":
            flash("Please select PDF file")
            return redirect(url_for("upload_pdf"))

        path = os.path.join(
            app.config["UPLOAD_FOLDER"],
            file.filename
        )

        file.save(path)

        # Read PDF Text
        doc = fitz.open(path)

        text = ""

        for page in doc:
            text += page.get_text()

        session["pdf_text"] = text

        flash("PDF uploaded successfully")
        return redirect(url_for("pdf_chat"))

    return render_template("upload_pdf.html")

# ============================================================
# PDF QUESTION ANSWERING
# ============================================================

@app.route("/pdf-chat", methods=["GET", "POST"])
@login_required
def pdf_chat():

    answer = ""

    if request.method == "POST":

        question = request.form["question"]
        context = session.get("pdf_text", "")

        if not context:
            flash("Please upload PDF first")
            return redirect(url_for("upload_pdf"))

        result = qa(
            question=question,
            context=context[:4000]
        )

        answer = result["answer"]

    return render_template(
        "pdf_chat.html",
        answer=answer
    )

# ============================================================
# RUN APP
# ============================================================

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
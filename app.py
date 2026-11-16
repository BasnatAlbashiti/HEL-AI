"""
app.py - Main Flask application for HEL AI Platform.
Controller: receives web requests and delegates work to the right module.
"""

from flask import Flask, render_template, request, jsonify
from chatbot import find_answer
from chatbot_advanced import ask_claude
from orchestrator import orchestrate
from orientation import get_orientation
from flask_mysqldb import MySQL
import os
from dotenv import load_dotenv
from flask import session, redirect, url_for
load_dotenv()


app = Flask(__name__)

app.secret_key = "hel2026secretkey"

# MySQL configuration
app.config['MYSQL_HOST'] = os.getenv('DB_HOST')
app.config['MYSQL_USER'] = os.getenv('DB_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('DB_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('DB_NAME')

mysql = MySQL(app)


# ===== HOME PAGE =====
@app.route("/")
def home():
    return render_template("index.html")


# ===== Niveau 1 — Assistant principal =====
@app.route("/chat")
def chat_page():
    return render_template("chat.html")

@app.route("/api/chat", methods=["POST"])
def api_chat():
    data = request.get_json()
    question = (data or {}).get("question", "").strip()

    if not question:
        return jsonify({"answer": "Veuillez poser une question.", "source": None, "confidence": "faible"}), 400

    result = find_answer(question)
    return jsonify(result)


# ===== Niveau 2 — Assistant IA (Groq) =====
@app.route("/chat-advanced")
def chat_advanced_page():
    return render_template("chat_advanced.html")

@app.route("/api/chat-advanced", methods=["POST"])
def api_chat_advanced():
    data = request.get_json()
    question = (data or {}).get("question", "").strip()

    if not question:
        return jsonify({"answer": "Veuillez poser une question."}), 400

    answer = ask_claude(question)
    return jsonify({"answer": answer})



# ===== Niveau 3 — Orchestrateur =====
@app.route("/chat-orchestrator")
def chat_orchestrator_page():
    return render_template("chat_orchestrator.html")

@app.route("/api/chat-orchestrator", methods=["POST"])
def api_chat_orchestrator():
    data = request.get_json()
    question = (data or {}).get("question", "").strip()

    if not question:
        return jsonify({"answer": "Veuillez poser une question."}), 400

    result = orchestrate(question)
    return jsonify(result)


# ===== Orientation IA =====
@app.route("/orientation")
def orientation_page():
    return render_template("chat_orientation.html")

@app.route("/api/orientation", methods=["POST"])
def api_orientation():
    data = request.get_json()
    interests = (data or {}).get("interests", "").strip()

    if not interests:
        return jsonify({"answer": "Veuillez décrire vos intérêts."}), 400

    answer = get_orientation(interests)
    return jsonify({"answer": answer})

# ===== Formulaire de satisfaction =====
@app.route("/formulaire")
def formulaire_page():
    return render_template("formulaire.html")

@app.route("/api/formulaire", methods=["POST"])
def api_formulaire():
    data = request.get_json()
    
    nom = (data or {}).get("nom", "").strip()
    email = (data or {}).get("email", "").strip()
    formation = (data or {}).get("formation", "").strip()
    note = (data or {}).get("note", 0)
    commentaire = (data or {}).get("commentaire", "").strip()

    if not nom or not email or not formation or not note:
        return jsonify({"success": False, "message": "Veuillez remplir tous les champs obligatoires."}), 400

    try:
        cur = mysql.connection.cursor()
        cur.execute("""
            INSERT INTO formulaires (nom, email, formation, note, commentaire)
            VALUES (%s, %s, %s, %s, %s)
        """, (nom, email, formation, note, commentaire))
        mysql.connection.commit()
        cur.close()
        return jsonify({"success": True, "message": "Merci pour votre retour !"})
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500
    

    # ===== Admin Login =====
ADMIN_USERNAME = "admin"
ADMIN_PASSWORD = "hel2026"

@app.route("/admin/login", methods=["GET", "POST"])
def admin_login():
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")
        if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
            session["admin"] = True
            return redirect(url_for("admin_dashboard"))
        else:
            return render_template("login.html", error="Identifiants incorrects.")
    return render_template("login.html", error=None)

@app.route("/admin/dashboard")
def admin_dashboard():
    if not session.get("admin"):
        return redirect(url_for("admin_login"))
    cur = mysql.connection.cursor()
    cur.execute("SELECT nom, email, formation, note, commentaire, date_soumission FROM formulaires ORDER BY date_soumission DESC")
    formulaires = cur.fetchall()
    cur.close()
    return render_template("admin.html", formulaires=formulaires)

@app.route("/admin/logout")
def admin_logout():
    session.clear()
    return redirect(url_for("home"))


if __name__ == "__main__":
    app.run(debug=True, port=5000)
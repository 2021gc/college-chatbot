from flask import Flask, render_template, request, redirect
import pandas as pd
from fuzzywuzzy import fuzz
import time

app = Flask(__name__)

# Load FAQ data
faq_data = pd.read_csv("faq.csv")
chat_history = []

# ---------- FAQ MATCH ----------
def get_faq_answer(user_input):
    best_score = 0
    best_answer = None

    for _, row in faq_data.iterrows():
        question = str(row["question"])
        answer = str(row["answer"])
        score = fuzz.ratio(user_input.lower(), question.lower())

        if score > best_score:
            best_score = score
            best_answer = answer

    if best_score >= 60:
        return best_answer
    return None


# ---------- AI FALLBACK ----------
def get_ai_answer(user_input):
    return "Sorry, I could not find this information in college data."


# ---------- ROUTES ----------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    global chat_history

    if request.method == "POST":

        # CLEAR CHAT
        if request.form.get("action") == "clear":
            chat_history.clear()
            return redirect("/chat")

        user_input = request.form.get("user_input")

        if not user_input:
            return redirect("/chat")

        user_msg = user_input.lower()

        # ---------- MAIN OPTIONS ----------
        if user_msg == "fees":
            answer = "💰 Fees details:\n• BSc IT Fees\n• BCom Fees\n• BA Fees"

        elif user_msg == "courses":
            answer = "🎓 Available courses:\n• BSc IT\n• BCom\n• BA"

        elif user_msg == "syllabus":
            answer = "📘 Select syllabus:\n• BSc IT Syllabus\n• BCom Syllabus\n• BA Syllabus"

        elif user_msg == "facilities":
            answer = "🏫 College Facilities:\n• Library\n• Hostel\n• Transport\n• Computer Lab\n• Sports Ground"

        # ---------- FEES ----------
        elif "bsc it fees" in user_msg:
            answer = "💰 BSc IT Fees: ₹25,000 per year (subject to change)."

        elif "bcom fees" in user_msg:
            answer = "💰 BCom Fees: ₹20,000 per year."

        elif "ba fees" in user_msg:
            answer = "💰 BA Fees: ₹15,000 per year."

        # ---------- SYLLABUS ----------
        elif "bsc it syllabus" in user_msg:
            answer = "📘 BSc IT syllabus includes Programming, DBMS, Networking, AI basics."

        elif "bcom syllabus" in user_msg:
            answer = "📘 BCom syllabus includes Accounting, Economics, Business Law."

        elif "ba syllabus" in user_msg:
            answer = "📘 BA syllabus includes History, Economics, Political Science."

        # ---------- FACILITIES ----------
        elif "library" in user_msg:
            answer = "📚 Our library has 10,000+ books, journals, and digital resources."

        elif "hostel" in user_msg:
            answer = "🏠 Hostel facility is available for boys and girls with food."

        elif "transport" in user_msg:
            answer = "🚌 College buses are available from major locations."

        elif "lab" in user_msg or "computer lab" in user_msg:
            answer = "💻 Well-equipped computer and science labs are available."

        elif "sports" in user_msg:
            answer = "🏏 Large sports ground available for cricket, football, and athletics."

        # ---------- FAQ + FALLBACK ----------
        else:
            answer = get_faq_answer(user_input)
            if not answer:
                answer = get_ai_answer(user_input)

        time.sleep(0.8)
        chat_history.append(("You", user_input))
        chat_history.append(("Bot", answer))

    return render_template("index.html", chat_history=chat_history)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

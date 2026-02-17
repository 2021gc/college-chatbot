from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
from fuzzywuzzy import fuzz
import time
import requests

app = Flask(__name__)

# ----------------- LOAD FAQ -----------------
faq_data = pd.read_csv("college_faq.csv")
chat_history = []

# ----------------- FAQ MATCH -----------------
def get_faq_answer(user_input):
    user_input = user_input.lower()

    best_score = 0
    best_answer = None

    for _, row in faq_data.iterrows():
        question = str(row["question"]).lower()
        answer = str(row["answer"])

        # ✅ 1. DIRECT KEYWORD MATCH (MOST IMPORTANT)
        if question in user_input:
            return answer

        # ✅ 2. FUZZY MATCH (BACKUP)
        score = fuzz.partial_ratio(user_input, question)
        if score > best_score:
            best_score = score
            best_answer = answer

    # ✅ LOWER THRESHOLD FOR BETTER MATCH
        if best_score >= 80:
           print("📘 FAQ MATCHED:", best_score)
           return best_answer

        print("🤖 USING OLLAMA")
        return None

# ----------------- CHATGPT FALLBACK -----------------
def get_ai_answer(user_input):
    try:
        response = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "phi",
                "prompt": f"Answer in 2 short sentences only.\nQuestion: {user_input}",
                "stream": False,
                "keep_alive": "30m",
                "options": {
                    "num_predict": 55,
                    "temperature": 0.3
                }
            }
        )

        return response.json()["response"]

    except Exception as e:
        print("Error:", e)
        return "AI not responding."



# ----------------- ROUTES -----------------
@app.route("/")
def home():
    return render_template("home.html")


@app.route("/chat", methods=["GET", "POST"])
def chat():
    global chat_history

    if request.method == "POST":

        if request.form.get("action") == "clear":
            chat_history.clear()
            return redirect("/chat")

        user_input = request.form.get("user_input")
        if not user_input:
            return redirect("/chat")

        msg = user_input.lower()

        # ----------------- RULE BASED (FIXED ORDER) -----------------

        # ---- SYLLABUS (SPECIFIC FIRST) ----
        if "bsc it syllabus" in msg:
            answer = (
                "BSc IT syllabus includes Programming, Data Structures, "
                "Database Management, Web Development, Networking and Project Work."
            )

        elif "bcom syllabus" in msg:
            answer = (
                "BCom syllabus includes Accounting, Business Economics, "
                "Banking, Taxation, Auditing and Financial Management."
            )

        elif "ba syllabus" in msg:
            answer = (
                "BA syllabus includes History, Economics, Political Science, "
                "Sociology and Elective subjects."
            )

        # ---- FEES ----
        elif msg == "fees":
            answer = "Fees details available for BSc IT, BCom and BA."

        elif "bsc it fees" in msg:
            answer = "BSc IT fees is ₹25,000 per year."

        elif "bcom fees" in msg:
            answer = "BCom fees is ₹20,000 per year."

        elif "ba fees" in msg:
            answer = "BA fees is ₹15,000 per year."

        # ---- COURSES ----
        elif msg == "courses":
            answer = "Available courses are BSc IT, BCom and BA."

        elif "bsc it" in msg:
            answer = (
                "BSc IT is a 3-year course with careers in software development, "
                "web development, data analysis and higher studies."
            )

        elif "bcom" in msg:
            answer = (
                "BCom is a 3-year course with careers in accounting, banking, finance and MBA."
            )

        elif "ba" in msg:
            answer = (
                "BA is a 3-year course with careers in civil services, teaching, journalism and MA."
            )

        # ---- FACILITIES ----
        elif msg == "facilities":
            answer = "Facilities include library, hostel, transport, labs and sports."

        elif "library" in msg:
            answer = "The college library has books, journals and digital resources."

        elif "hostel" in msg:
            answer = "Separate hostel facilities are available for boys and girls."

        elif "transport" in msg:
            answer = "College bus facilities are available from major areas."

        elif "wifi" in msg:
            answer = "The campus is fully Wi-Fi enabled."

        elif "medical" in msg:
            answer = "On-campus medical and first-aid facilities are available."

        # ---- FAQ + AI ----
        else:
            answer = get_faq_answer(user_input)
            if not answer:
                answer = get_ai_answer(user_input)

        

        chat_history.append(("You", user_input))
        chat_history.append(("Bot", answer))

    return render_template("index.html", chat_history=chat_history)


# ----------------- API FOR VOICE INPUT -----------------
@app.route("/voice", methods=["POST"])
def voice():
    data = request.json
    user_input = data.get("text")

    if not user_input:
        return jsonify({"reply": "I didn't hear anything."})

    msg = user_input.lower()

    if "bsc it syllabus" in msg:
        answer = "BSc IT syllabus includes Programming, DBMS, Web Development and Networking."
    else:
        answer = get_faq_answer(user_input)
        if not answer:
            answer = get_ai_answer(user_input)

    chat_history.append(("You", user_input))
    chat_history.append(("Bot", answer))

    return jsonify({"reply": answer})


# ----------------- RUN -----------------
if __name__ == "__main__":
   app.run(debug=False)

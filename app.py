from flask import Flask, render_template, request, redirect, jsonify
import pandas as pd
from fuzzywuzzy import fuzz
import time
from openai import OpenAI

app = Flask(__name__)


# ----------------- LOAD FAQ -----------------
faq_data = pd.read_csv("college_faq.csv")
chat_history = []

# ----------------- FAQ MATCH -----------------
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


# ----------------- CHATGPT FALLBACK -----------------
def get_ai_answer(user_input):
    try:
        response = client.responses.create(
            model="gpt-4.1-mini",
            input=f"You are a college AI assistant. Answer briefly.\nQuestion: {user_input}"
        )

        print("🔥 OpenAI API CALLED")  # debug proof
        return response.output_text.strip()

    except Exception as e:
        print("❌ OpenAI Error:", e)
        return "Sorry, AI service is not available right now."


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

        # ----------------- RULE BASED -----------------
        if msg == "fees":
            answer = "Fees details available for BSc IT, BCom and BA."

        elif msg == "courses":
            answer = "Available courses are BSc IT, BCom and BA."

        elif msg == "facilities":
            answer = "Facilities include library, hostel, transport, labs and sports."

        elif "bsc it fees" in msg:
            answer = "BSc IT fees is ₹25,000 per year."

        elif "bcom fees" in msg:
            answer = "BCom fees is ₹20,000 per year."

        elif "ba fees" in msg:
            answer = "BA fees is ₹15,000 per year."

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

        # ----------------- FAQ + AI -----------------
        else:
            answer = get_faq_answer(user_input)
            if not answer:
                answer = get_ai_answer(user_input)

        time.sleep(0.5)

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

    answer = get_faq_answer(user_input)
    if not answer:
        answer = get_ai_answer(user_input)

    chat_history.append(("You", user_input))
    chat_history.append(("Bot", answer))

    return jsonify({"reply": answer})


# ----------------- RUN -----------------
if __name__ == "__main__":
    app.run(debug=True)

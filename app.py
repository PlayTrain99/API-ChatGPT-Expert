from flask import Flask, render_template, request, jsonify, session
import os
import fitz  # PyMuPDF
from dotenv import load_dotenv
import spacy
from openai import OpenAI

app = Flask(__name__)
app.secret_key = os.urandom(24)

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

nlp = spacy.load("pl_core_news_sm")

# Globalna zmienna do przechowywania zawartości PDF
pdf_content = None

def load_pdf_content(pdf_path):
    try:
        doc = fitz.open(pdf_path)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text.lower()
    except Exception as e:
        print(f"Nie udało się załadować pliku PDF: {e}")
        return None

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/api", methods=["POST"])
def api():
    global pdf_content
    session.permanent = True

    user_message = request.json.get("message")
    if not user_message:
        return jsonify({"response": "Proszę podać wiadomość."}), 400

    if "conversation" not in session:
        session["conversation"] = []

    session["conversation"].append({"role": "user", "content": user_message})

    if pdf_content is None:
        pdf_path = "PDF/misjazgrzyby.pdf"
        pdf_content = load_pdf_content(pdf_path)
        if pdf_content is None:
            return jsonify({"response": "Błąd przy ładowaniu pliku PDF."}), 500

    # Logowanie treści PDF do konsoli dla celów debugowania
    print(f"PDF Content: {pdf_content[:10000]}")

    conversation_history = [{"role": "system", "content": pdf_content[:10000]}]
    conversation_history += [{"role": msg["role"], "content": msg["content"]} for msg in session["conversation"]]

    print(f"Sending to OpenAI: {conversation_history}")  # Logowanie wysyłanych danych

    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            temperature=0.4,
            messages=conversation_history
        )
        response_text = response.choices[0].message.content.strip()
        session["conversation"].append({"role": "system", "content": response_text})
        session.modified = True
    except Exception as e:
        response_text = f"Błąd serwera: {str(e)}"
        return jsonify({"response": response_text}), 500

    return jsonify({"response": response_text})

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
from chatbot import generate_response  # Import AI logic
import re
import os

app = Flask(__name__, static_folder="frontend/static", template_folder="frontend/templates")
CORS(app)

@app.route("/")
def home():
    return render_template("index.html")

def clean_markdown(text):
    """Converts AI Markdown to HTML-friendly formatting."""
    text = re.sub(r'\*\*(.*?)\*\*', r'<b>\1</b>', text)  # Bold
    text = re.sub(r'\*(.*?)\*', r'<i>\1</i>', text)  # Italic
    text = text.replace("\n", "<br>")  # Line breaks
    return text

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_message = data.get("message", "")

    if not user_message:
        return jsonify({"error": "No message provided"}), 400

    ai_response = generate_response(user_message)  # Get AI-generated response
    cleaned_response = clean_markdown(ai_response)  # Clean Markdown before sending

    return jsonify({"response": cleaned_response})

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))  # Get the port from Render
    app.run(host="0.0.0.0", port=port, debug=True)  # Set the correct host & port
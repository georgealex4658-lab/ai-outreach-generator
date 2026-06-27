from flask import Flask, render_template, request
import anthropic
import os 
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)
client = anthropic.Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods = ["POST"])
def generate():
    name = request.form["name"]
    business = request.form["business"]
    city = request.form["city"]

    response = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Generate 5 different personalized outreach messages for a Facebook ads agency called Phantom Digital reaching out to a roofing company. The messages should be short, direct and conversational like a real DM or cold email. No placeholders. Prospect name: {name}. Business: {business}. City: {city}. Make each message unique with a different angle. Number them 1-5."
            }
        ]
    )
    messages = response.content[0].text
    return render_template("index.html", messages=messages, name=name)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=False)
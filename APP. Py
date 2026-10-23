import os
from flask import Flask, request
app = Flask(__name__)

@app.route("/")
def home():
    return "Agente WhatsApp AI - Angola esta online!"

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    if request.method == "GET":
        return request.args.get("hub.challenge")
    # Aqui vai receber mensagens do WhatsApp
    print(request.json)
    return "OK", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 3000)))
    

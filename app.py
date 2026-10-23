
import os
from flask import Flask, request, jsonify
import requests
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# Configurações - vem do Render (Environment Variables)
META_API_KEY = os.getenv("META_API_KEY")
WHATSAPP_TOKEN = os.getenv("WHATSAPP_TOKEN")
VERIFY_TOKEN = os.getenv("VERIFY_TOKEN", "angola_verify_2026")
META_API_URL = "https://api.llama.meta.com/v1/chat/completions"

# Prompt profissional para mercado angolano
SYSTEM_PROMPT = """
Você é um assistente de vendas para PMEs angolanas.
Fala português angolano, informal, com gírias leves (mano, bwe, bué, ya).
Seja rápido, direto, focado em fechar venda.
Entende produtos de catálogo, preços em Kwanza, e negociação local.
Nunca diga que é IA, aja como funcionário da empresa.
"""

def call_llama4(user_message):
    """Chamada real para Llama 4 via Meta Model API"""
    if not META_API_KEY:
        return "Olá mano! Como posso te ajudar hoje? Ya?"

    headers = {
        "Authorization": f"Bearer {META_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "Llama-4-Maverick-17B-128E-Instruct",
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_message}
        ],
        "max_tokens": 500,
        "temperature": 0.7
    }
    try:
        r = requests.post(META_API_URL, json=payload, headers=headers, timeout=20)
        r.raise_for_status()
        return r.json()["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Erro Llama4: {e}")
        return "Mano, tive um problema rápido na conexão, pode repetir?"

@app.route("/", methods=["GET"])
def health():
    return jsonify({"status": "online", "agent": "WhatsApp AI Angola", "model": "Llama 4"}), 200

@app.route("/webhook", methods=["GET", "POST"])
def webhook():
    # Verificação do WhatsApp Business API
    if request.method == "GET":
        if request.args.get("hub.verify_token") == VERIFY_TOKEN:
            return request.args.get("hub.challenge")
        return "Token inválido", 403

    # Receber mensagem
    data = request.json
    try:
        message = data["entry"][0]["changes"][0]["value"]["messages"][0]["text"]["body"]
        sender = data["entry"][0]["changes"][0]["value"]["messages"][0]["from"]
        print(f"Mensagem de {sender}: {message}")
        
        resposta_ia = call_llama4(message)
        
        # Aqui você enviaria de volta via WhatsApp API
        # Por enquanto retorna no log
        print(f"Resposta Llama 4: {resposta_ia}")
        
        return jsonify({"status": "processed"}), 200
    except:
        return jsonify({"status": "ignored"}), 200

if __name__ == "__main__":
    port = int(os.getenv("PORT", 3000))
    app.run(host="0.0.0.0", port=port)

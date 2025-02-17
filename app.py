import openai
import os
from flask import Flask, request, jsonify

app = Flask(__name__)

openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")

@app.route("/chat", methods=["POST"])
def chat():
    user_message = request.json.get("message", "")

    if not user_message:
        return jsonify({"error": "Message cannot be empty"}), 400
    
    try:
        response = openai.ChatCompletion.create(
            model = "gpt-3.5-turbo",
             messages=[{"role": "user", "content": user_message}]
        )

        ai_response = response["choices"][0]["message"]["content"]
        return jsonify({"response": ai_response})
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
if __name__ == "__main__":
    port = int(os.environ.get("WEBSITES_PORT", 8000))
    app.run(host="0.0.0.0", port=port)
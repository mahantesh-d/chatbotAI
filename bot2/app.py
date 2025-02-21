import os
import asyncio
from flask import Flask, request, jsonify
from botbuilder.ai.luis import LuisApplication, LuisRecognizer

# Azure Credentials
LUIS_APP_ID = "<LUIS_APP_ID>"
LUIS_API_KEY = "<LUIS_API_KEY>"
LUIS_ENDPOINT = "https://northeurope.api.cognitive.microsoft.com/"
COSMOS_ENDPOINT = "https://jhanvi-restaurantchatbotdb.documents.azure.com:443/"
COSMOS_KEY = ""
DATABASE_NAME = "ChatbotDB"
CONTAINER_NAME = "chatbot-messages"

app = Flask(__name__)

# Set up LUIS Recognizer
luis_app = LuisApplication(LUIS_APP_ID, LUIS_API_KEY, LUIS_ENDPOINT)
luis_recognizer = LuisRecognizer(luis_app)

# Cosmos DB Client
# cosmos_client = CosmosClient(COSMOS_ENDPOINT, COSMOS_KEY)
# database = cosmos_client.get_database_client(DATABASE_NAME)
# container = database.get_container_client(CONTAINER_NAME)

# # Bot Adapter Settings
# bot_settings = BotFrameworkAdapterSettings(app_id=None, app_password=None)
# bot_adapter = BotFrameworkAdapter(bot_settings)


class RestaurantChatbot:
    async def process_message(self, message):
        # Analyze user message with LUIS
        result = await luis_recognizer.recognize(message)
        intent = result.intents[0].intent if result.intents else "None"

        if intent == "CheckMenu":
            return "Our menu includes Pizza, Pasta, and Burgers. Would you like to order?"
        elif intent == "BookTable":
            return "Sure! How many people and what time?"
        elif intent == "OperatingHours":
            return "We are open from 10 AM to 10 PM daily."
        else:
            return "I'm sorry, I didn't understand that. Could you rephrase?"

# Flask API Endpoint
@app.route("/api/messages", methods=["POST"])
def messages():
    payload = request.json  # Extract JSON request body
    user_message = payload.get("text", "")  # Get user input text

    chatbot = RestaurantChatbot()

    # FIX: Await the async function using asyncio.run()
    response = asyncio.run(chatbot.process_message(user_message))

    return jsonify({"response": response})  # Return chatbot's response

if __name__ == "__main__":
    app.run(port=3978)
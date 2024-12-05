from flask import Flask, request, jsonify,render_template
from chatbot.components.reterival_generation import generation  # Import your generation function
from chatbot.components.data_converter import DataConverter
from chatbot.components.data_ingestion import DataIngestion
from chatbot.logger.logging import logging
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os

app = Flask(__name__)

# Load environment variables
load_dotenv()
GOOGLE_GEMINI_API = os.getenv("GOOGLE_GEMINI_API")

@app.route("/")
def index():
    return render_template("index.html")

# Endpoint for chatbot interaction
@app.route('/chat', methods=['POST'])
def chat():
    try:
        user_message = request.json.get('message')  # Get user input from the frontend

        # Convert data into documents
        dataconverter = DataConverter()
        docs = dataconverter.convert_data_into_documents()

        # Create embeddings instance
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001", google_api_key=GOOGLE_GEMINI_API)

        # Data Ingestion
        data_ingestion = DataIngestion(docs=docs, embeddings=embeddings)
        vstore, inserted_ids = data_ingestion.ingestion_data(status=None)

        # Generate response using the chatbot generation function
        chain = generation(vstore)
        response = chain.invoke(user_message)  # Pass the user input message

        return jsonify({"response": response}), 200  # Return the response as JSON

    except Exception as e:
        logging.error(f"Error in chat endpoint: {e}")
        return jsonify({"error": "An error occurred"}), 500

if __name__ == '__main__':
    app.run(debug=True)

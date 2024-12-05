from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_google_genai import ChatGoogleGenerativeAI
from chatbot.components.data_converter import DataConverter
from chatbot.components.data_ingestion import DataIngestion
from chatbot.logger.logging import logging
from chatbot.exception.exception import aiChatbot
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from dotenv import load_dotenv
import os, sys

# Load environment variables
load_dotenv()

GOOGLE_GEMINI_API = os.getenv("GOOGLE_GEMINI_API")
print(GOOGLE_GEMINI_API)

def generation(vstore):
    try:
        retriever = vstore.as_retriever(search_kwargs={"k": 3})

        PRODUCT_BOT_TEMPLATE = """
        Your ecommercebot bot is an expert in product recommendations and customer queries.
        It analyzes product titles and reviews to provide accurate and helpful responses.
        Ensure your answers are relevant to the product context and refrain from straying off-topic.
        Your responses should be concise and informative.

        CONTEXT:
        {context}

        QUESTION: {question}

        YOUR ANSWER:
        """

        prompt = ChatPromptTemplate.from_template(PRODUCT_BOT_TEMPLATE)

        llm = ChatGoogleGenerativeAI(
        model="models/gemini-1.5-pro",
        google_api_key=GOOGLE_GEMINI_API
        )

        chain = (
            {"context": retriever, "question": RunnablePassthrough()}
            | prompt
            | llm
            | StrOutputParser()
        )

        return chain
    except Exception as e:
        logging.error(f"Error in generation function: {e}")
        raise aiChatbot(e, sys)

if __name__ == '__main__':
    try:
        logging.info("Starting the data ingestion process.")

        # Convert data into documents
        dataconverter = DataConverter()
        docs = dataconverter.convert_data_into_documents()
        logging.info("Converted data into %d documents.", len(docs))

        # Create the embeddings instance
        embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001",google_api_key=GOOGLE_GEMINI_API)

        # Create an instance of the DataIngestion class with embeddings
        data_ingestion = DataIngestion(docs=docs, embeddings=embeddings)

        # Call ingestdata with status=None to insert documents
        vstore, inserted_ids = data_ingestion.ingestion_data(status=None)
        logging.info("Inserted %d documents into the vector store.", len(inserted_ids))

        # Generate a response using the retrieved vector store
        chain = generation(vstore)
        response = chain.invoke("Can you tell me the best bluetooth buds?")
        logging.info("Response: %s", response)
        print(response)

    except Exception as e:
        logging.error(f"An error occurred: {e}")

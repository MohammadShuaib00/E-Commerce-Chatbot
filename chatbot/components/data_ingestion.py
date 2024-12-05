import os
import sys
from dotenv import load_dotenv
from chatbot.logger.logging import logging
from chatbot.exception.exception import aiChatbot
from chatbot.components.data_converter import DataConverter
from langchain_astradb import AstraDBVectorStore
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()

ASTRA_DB_API_ENDPOINT = os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN = os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE = os.getenv("ASTRA_DB_KEYSPACE")



class DataIngestion:
    def __init__(self, docs,embeddings):
        try:
            logging.info("Initializing DataIngestion with %d documents and embedding model.", len(docs))
            self.docs = docs
            self.embedding = embeddings
        except Exception as e:
            logging.error("Error initializing DataIngestion: %s", str(e))
            raise aiChatbot(e, sys)

    def embeddings(self, documents):
        embeddings_list = []
        logging.info("Generating embeddings for %d documents.", len(documents))
        
        for doc in documents:
            try:
                # Extract the 'page_content' and generate an embedding
                embedding = self.embedding.embed_query(doc["page_content"])
                embeddings_list.append(embedding)
            except Exception as e:
                logging.error("Error generating embedding for document: %s", str(e))
                
        logging.info("Generated embeddings for all documents.")
        return embeddings_list

    def ingestion_data(self, status=None):
        logging.info("Ingesting data into the vector store.")
        vstore = AstraDBVectorStore(
            embedding=self.embedding,
            collection_name="chatbotecomm",
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,
            namespace=ASTRA_DB_KEYSPACE,
        )

        try:
            if status is None:  # If no storage status is provided, ingest the data
                logging.info("Adding documents to the vector store.")
                inserted_ids = vstore.add_documents(self.docs)
                logging.info("%d documents added to the vector store.", len(inserted_ids))
                return vstore, inserted_ids
            else:  # If status is provided, just return the vector store
                logging.info("Returning vector store without ingesting data.")
                return vstore
        except Exception as e:
            logging.error("Error during data ingestion: %s", str(e))
            raise aiChatbot(e, sys)

import os
import sys
import pandas as pd
from langchain_core.documents import Document
from chatbot.exception.exception import aiChatbot
from chatbot.logger.logging import logging

class DataConverter:
    def __init__(self):
        """
        Initializes the DataConverter with the file path.
        """
        try:
            self.file_path = "data/flipkartproductreview.csv"
        except Exception as e:
            raise aiChatbot(e, sys)
    
    def read_data(self) -> pd.DataFrame:
        """
        Reads the CSV file into a DataFrame.
        """
        try:
            logging.info("Reading the data from the file.")
            data = pd.read_csv(self.file_path)
            logging.info("Successfully read the data.")
            return data
        except Exception as e:
            raise aiChatbot(e, sys)
    
    @staticmethod
    def extract_important_columns(data: pd.DataFrame) -> pd.DataFrame:
        """
        Extracts relevant columns from the DataFrame (product title and review).
        """
        try:
            data = data[['product_title', 'review']]
            return data
        except Exception as e:
            raise aiChatbot(e, sys)
    
    def process_data(self, data: pd.DataFrame) -> list:
        """
        Processes the data and converts it into a list of dictionaries with product title and review.
        """
        try:
            logging.info("Fetching important columns.")
            data = self.extract_important_columns(data)
            logging.info("Successfully fetched the columns.")
            
            product_list = []
            for index, row in data.iterrows():
                obj = {
                    'product_name': row['product_title'],
                    'review': row['review']
                }
                product_list.append(obj)
            return product_list
        except Exception as e:
            raise aiChatbot(e, sys)
    
    def convert_to_documents(self, product_list: list) -> list:
        """
        Converts the list of product information into Document objects.
        """
        try:
            docs = []
            for entry in product_list:
                metadata = {"product_name": entry['product_name']}
                doc = Document(page_content=entry['review'], metadata=metadata)
                docs.append(doc)
            return docs
        except Exception as e:
            raise aiChatbot(e, sys)
    
    def convert_data_into_documents(self):
        """
        Main method to convert data into documents.
        """
        try:
            # Step 1: Read data
            data = self.read_data()

            # Step 2: Process data
            product_list = self.process_data(data)

            # Step 3: Convert product list into documents
            docs = self.convert_to_documents(product_list)

            logging.info("Successfully converted data into documents.")
            return docs
        
        except Exception as e:
            raise aiChatbot(e, sys)



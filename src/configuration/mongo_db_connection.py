# src/configuration/mongo_db_connection.py

import os
import sys
import pymongo
import certifi
from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME, MONGO_URL_KEY

# Load certificate for MongoDB Atlas TLS
ca = certifi.where()

class MongoDBClient:
    """
    MongoDBClient is responsible for establishing a connection to the MongoDB database.
    """
    client = None  # Shared MongoClient instance (singleton pattern)

    def __init__(self, database_name: str = DATABASE_NAME) -> None:
        """
        Initializes a connection to MongoDB. Reuses existing connection if available.
        """
        try:
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGO_URL_KEY)
                if mongo_db_url is None:
                    raise Exception(f"Environment variable '{MONGO_URL_KEY}' not set!")

                MongoDBClient.client = pymongo.MongoClient(
                    mongo_db_url,
                    tlsCAFile=ca
                )
                logging.info("New MongoDB connection created.")

            # Assign the shared client to this instance
            self.client = MongoDBClient.client
            self.database = self.client[database_name]      # ← NOW THIS RUNS!
            self.database_name = database_name

            logging.info(f"MongoDB connected → Database: {database_name}")

        except Exception as e:
            logging.error("Failed to connect to MongoDB")
            raise MyException(e, sys)
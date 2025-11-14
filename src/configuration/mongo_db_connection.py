import os
import sys
import pymongo
import certifi

from src.exception import MyException
from src.logger import logging
from src.constants import DATABASE_NAME,MONGO_URL_KEY

#Load the cerfificate authority file to avoid timeout erroe when connecting to mongoDB
ca = certifi.where()

class MongoDBClient:
    '''
    MongoDBClient is responsible for establishing a connection to the MongoDB database.
    Attributes:
    ------
    client: MongoClient
        A shared MongoClient instance for the class.
    database: Database
        The specific database instance that MongoDBClient connects to.

    Methods:
    -----
    __init__(database_name:str)-->None
        Initializes the MongoDB connection using the given database name.
    '''

    client = None # shared Mongoclient instance across all MongoBD client instances

    def __init__(self,database_name: str = DATABASE_NAME)->None:
        '''
        Initializes a connection to the MongoDB databse. if no existing connection is found, it establish a new one
        Parameters:
        --------\
        MyException
            if there is an issue connecting to mongoBD or if the environment variable for the MongoDB URL is not set

        '''
        try:
            #check if a MOngoDB client connection has already been established; if nor create a new one
            if MongoDBClient.client is None:
                mongo_db_url = os.getenv(MONGO_URL_KEY) #Retrive MongoDB URL from environment variables
                if mongo_db_url is None:
                    raise Exception(f"Environment variable'{MONGO_URL_KEY}' is not set")
                    
                MongoDBClient.client = pymongo.MongoClient(mongo_db_url)

                
                #Establish a new MongoDB client for this instance
                self.client = MongoDBClient.client
                self.database = self.client[database_name]
                self.database_name = database_name
                logging.info('MongoDB connection sucess!')

        except Exception as e:
            #raise a custom exception with traceback details if connection fails
            raise MyException(e,sys)
        
        
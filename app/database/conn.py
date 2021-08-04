from fastapi import FastAPI
from pymongo import MongoClient
import logging

class MongoDB:
    def __init__(self, app: FastAPI = None, **kwargs):
        self.db_url = None
        self.client = None
        self.db = None
    
    def init_app(self, app:FastAPI, **kwargs):
        self.db_url = kwargs.get("DB_URL")
        self.client = MongoClient(self.db_url)
        self.db = self.client.get_database(kwargs.get("DB_NAME"))
    
    def get_db(self):
        return self.db

mongo = MongoDB()
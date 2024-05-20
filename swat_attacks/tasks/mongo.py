from pymongo import MongoClient
from django.conf import settings

client = MongoClient(settings.MONGO_CONNECTION_STRING)
db = client[settings.MONGO_DATABASE_NAME]

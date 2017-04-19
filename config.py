from pymongo import MongoClient
from pymongo import ReturnDocument

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Secret'
DB_NAME = 'multitenants'

DATABASE = MongoClient()[DB_NAME]
PROJECTS_COLLECTION = DATABASE.projects
USERS_COLLECTION = DATABASE.users
COUNTER_COLLECTION = DATABASE.counter
DEBUG = True

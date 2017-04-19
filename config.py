from pymongo import MongoClient

WTF_CSRF_ENABLED = True
SECRET_KEY = 'Secret'
DB_NAME = 'multitenants'

DATABASE = MongoClient()[DB_NAME]
PROJECTS_COLLECTION = DATABASE.projects
USERS_COLLECTION = DATABASE.users

DEBUG = True

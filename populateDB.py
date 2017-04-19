#!/usr/bin/python

from werkzeug.security import generate_password_hash
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError


def main():
    # Connect to the DB
    collection = MongoClient()["multitenants"]["users"]

    # Ask for data to store
    user = raw_input("Enter username: ")
    name = raw_input("Enter name")
    email = raw_input("Enter your email: ")
    password = raw_input("Enter your password: ")
    role = raw_input("Enter user role (admin/user/manager): ")
    pass_hash = generate_password_hash(password, method='pbkdf2:sha256')

    # Insert the user in the DB
    try:
        collection.insert({"_id": user, "name": name, "email": email, "password": pass_hash, "role": role, "projects": []})
        print "User created."
    except DuplicateKeyError:
        print "User already present in DB."


if __name__ == '__main__':
    main()

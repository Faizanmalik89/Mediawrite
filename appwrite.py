import os
import logging
import requests
import json

# Initialize local authentication
def initialize_appwrite():
    logging.info("Using local authentication instead of Appwrite")
    return None, None, None, None

# Register a new user
def register_user(email, password, name):
    try:
        # For demonstration purposes, we'll use the Flask database instead
        # of Appwrite. The actual user registration will be handled
        # in the routes.py file.
        logging.info(f"Local user registration attempt for: {email}")
        return {"email": email, "name": name}
    except Exception as e:
        logging.error(f"Local registration error: {str(e)}")
        raise Exception(f"Failed to register user: {str(e)}")

# Login a user
def login_user_appwrite(email, password):
    try:
        # For demonstration purposes, we'll use the Flask database
        # instead of Appwrite. The actual login will be handled
        # in the routes.py file.
        logging.info(f"Local login attempt for: {email}")
        return {"email": email}
    except Exception as e:
        logging.error(f"Local login error: {str(e)}")
        raise Exception(f"Failed to login: {str(e)}")

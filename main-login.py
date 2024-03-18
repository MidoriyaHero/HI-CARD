from utils import functions
import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import json
from google.oauth2.service_account import Credentials

def main():
    container = st.container(border=True)
    email = container.text_input('Email Address')
    password = container.text_input('Password',type='password')
    # Add a dropdown to choose between Login and Signup
    _, col2 = st.columns([5, 1])
    login_or_signup = col2.selectbox("Login or Signup", ["Login", "Signup"])
    if login_or_signup == "Login":
        if container.button('Login'):
            functions.user_sign_in(email,password)
    elif login_or_signup == "Signup":
        username = container.text_input("Enter  your username")
        if container.button('Create my account'):
            functions.create_user(email = email, password = password,username=username)

if __name__ == "__main__":
    st.set_page_config(page_title="HI-card", layout="centered")
    st.title("Welcome to HI card 🪪")
    key_dict = json.loads(st.secrets["textkey"])
    creds = credentials.Certificate(key_dict)

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(creds)
    main()
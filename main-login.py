from utils import functions
import firebase_admin
import streamlit as st
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth
import json
from google.oauth2.service_account import Credentials

def main():
    col1, col2 = st.columns([5, 1])
    login_or_signup = col2.selectbox("Login or Signup", ["Login", "Signup"])
    email = st.text_input('Email Address')
    password = st.text_input('Password',type='password')
    # Add a dropdown to choose between Login and Signup
    if login_or_signup == "Login":
        if col1.button('Login'):
            functions.user_sign_in(email,password)
        else:
            st.warning('Invalid user! Try again!!!')

    elif login_or_signup == "Signup":
        username = st.text_input("Enter  your username")
        if st.button('Create my account'):
            functions.create_user(email = email, password = password,username=username)

if __name__ == "__main__":
    st.set_page_config(page_title="HI-card", layout="centered", initial_sidebar_state="collapsed")
    st.title("Welcome to HI card 🪪")
    key_dict = json.loads(st.secrets["textkey"])
    creds = credentials.Certificate(key_dict)

    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(creds)
    main()
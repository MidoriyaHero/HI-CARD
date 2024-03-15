import streamlit as st
import firebase_admin
from firebase_admin import auth
from firebase_admin import credentials
import json
from google.oauth2.service_account import Credentials

key_dict = json.loads(st.secrets["textkey"])

def create_hos(email, password,username):
    user = auth.create_user(email = email, password = password,uid="hos-"+email,display_name = username)
    st.success('Account created successfully!')
    st.markdown('Please Login using your email and password')
    st.balloons()

def main():
    email = st.text_input('Email Address')
    password = st.text_input('Password',type='password')
    username = st.text_input("Enter  your username")
    if st.button('Create my account'):
        create_hos(email = email, password = password,username=username)

if __name__ == '__main__':
    st.set_page_config(page_title="HI-card", layout="centered", initial_sidebar_state="collapsed")
    st.title("Welcome to HI card 🪪")
    creds = Credentials.from_service_account_info(key_dict)
    try:
        firebase_admin.get_app()
    except ValueError:
        firebase_admin.initialize_app(creds)
    main()
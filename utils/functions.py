import streamlit as st
import firebase_admin
from firebase_admin import auth
import requests
import json
from time import sleep
from streamlit.runtime.scriptrunner import get_script_run_ctx
from streamlit.source_util import get_pages




def create_user(email, password,username):
    user = auth.create_user(email = email, password = password,uid="user-"+email,display_name = username)
    st.success('Account created successfully!')
    st.markdown('Please Login using your email and password')
    st.balloons()

def user_sign_in(email, password, return_secure_token=True):
    payload = json.dumps({"email":email, "password":password, "return_secure_token":return_secure_token})
    #change API KEY to your API key
    FIREBASE_WEB_API_KEY = 'AIzaSyD66lk98aE-aFsIhyRSJikEiWInlE8Blmc' 
    rest_api_url = "https://identitytoolkit.googleapis.com/v1/accounts:signInWithPassword"

    r = requests.post(rest_api_url,
                  params={"key": FIREBASE_WEB_API_KEY},
                  data=payload)
    r = r.json()
    if 'registered' in r:
        st.session_state["logged_in"] = True
        st.session_state['user_info'] = r
        st.success("Logged in!")
        if r['localId'].split('-')[0] == 'user':
            st.switch_page("pages/User-display.py")
        elif r['localId'].split('-')[0] == 'hos':
            st.switch_page("pages/hos-display.py")
    else:
        st.warning("Invalid email or password try again!")

def get_current_page_name():
    ctx = get_script_run_ctx()
    if ctx is None:
        raise RuntimeError("Couldn't get script context")

    pages = get_pages("")

    return pages[ctx.page_script_hash]["page_name"]

def make_sidebar():
    with st.sidebar:
        st.title("Profile setting")
        st.write("")
        st.write("")
        
        if st.session_state.get("logged_in", False):
            st.page_link("pages/User-display.py", label="Setting", icon="⚙️")
            st.page_link("pages/QR_code.py", label="Generate QR code", icon="🔁")
            st.write("")
            st.write("")

            if st.button("Log out"):
                logout()

        elif get_current_page_name() != "main-login":
            st.switch_page("main-login.py")

def logout():
    st.session_state.logged_in = False
    st.session_state.user_infor = ""
    st.info("Logged out successfully!")
    sleep(0.5)
    st.switch_page("main-login.py")
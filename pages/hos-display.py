from utils import functions
import streamlit as st
from firebase_admin import firestore
import json
from google.oauth2.service_account import Credentials

key_dict = json.loads(st.secrets["textkey"])
creds = Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

def load_user():
    doc_ref = db.collection("Hospital").document(user_info['localId'])
    doc = doc_ref.get()
    dic = doc.to_dict()
    if dic is not None:
        name = dic.get('Name')
        phone = dic.get('Phone')
        location = dic.get('Location')
        return name,phone,location
    else:
        return None, None, None
    

def save_user_data(name,phone,location):
    db = firestore.client()
    doc_ref = db.collection("Hospital").document(user_info['localId'])
    doc_ref.set({
		"Location": location,
        "Name": name,
        "Phone": phone,
	})
    st.success("Profile updated successfully!")
    st.balloons()


def display_profile():
    name,phone,location = load_user()
    name = st.text_input("Name:",name)
    phone = st.text_input("Phone:", phone)
    location = st.text_input("Location:",location)
    return name ,phone, location



def main():
    st.title("Hospital Profile")
    # Create the form
    with st.form("user_profile_form"):
        name, phone, location = display_profile()
        submitted = st.form_submit_button("Save Profile")

        if submitted:
            save_user_data(name, phone, location)
    with st.sidebar:
        if st.button("Log out"):
            functions.logout()



if __name__ == "__main__":
    
    user_info = st.session_state.user_info
    st.header(f"Hi, {user_info['displayName']}")
    st.markdown('this page is used to register and update your information')
    main()

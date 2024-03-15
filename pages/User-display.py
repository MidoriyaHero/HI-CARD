from utils import functions
import streamlit as st
from firebase_admin import firestore
import json
from google.oauth2.service_account import Credentials

key_dict = json.loads(st.secrets["textkey"])
creds = Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)


def load_user():
    doc_ref = db.collection("Users").document(user_info['localId'])
    doc = doc_ref.get()
    dic = doc.to_dict()
    if dic is not None:
        age = dic.get('Age')
        name = dic.get('Name')
        phone = dic.get('Phone')
        anamnesis = dic.get('Anamnesis')
        return age,name,phone,anamnesis
    else:
        return None,None,None,None

def save_user_data(age,name,phone,anamnesis):
    db = firestore.client()
    doc_ref = db.collection("Users").document(user_info['localId'])
    doc_ref.set({
		"Age": age,
		"Anamnesis":anamnesis,
        "Name": name,
        "Phone": phone,
	}, merge=True)
    st.success("Profile updated successfully!")
    st.balloons()

def display_profile():
    age,name,phone,anamnesis = load_user()
    name = st.text_input("Name:",name)
    age = st.text_input("Age:",age)
    phone = st.text_input("phone:", phone)
    anamnesis = st.text_area("Anamnesis:",anamnesis)
    return age,name, phone, anamnesis

def main():
    st.title("User Profile")
    # Create the form
    with st.form("user_profile_form"):
        age,name, phone, anamnesis = display_profile()
        submitted = st.form_submit_button("Save Profile")

        if submitted:
            save_user_data(age,name, phone, anamnesis)

if __name__ == "__main__":
    functions.make_sidebar()
    user_info = st.session_state.user_info
    #st.write(user_info)
    st.header(f"Hi, {user_info['displayName']}")
    st.markdown('this page is used to register and update your information')
    main()

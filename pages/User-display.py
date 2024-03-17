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

def check_profile(age, name, phone,anamnesis):
    if age == None or name == None or phone == None or age == '' or name == '' or phone == '' or anamnesis == None or anamnesis =='':
        st.session_state["incomplete_info"] = True
    else:  
        st.session_state["incomplete_info"] = False

def display_profile():
    age,name,phone,anamnesis = load_user()
    name = st.text_input("Name: *",name)
    age = st.text_input("Age: *",age)
    phone = st.text_input("Phone: *", phone)
    anamnesis = st.text_area("Anamnesis: *",anamnesis)
    return age,name, phone, anamnesis

def main():
    st.title("User Profile")
    # Create the form
    
    with st.form("user_profile_form"):
        age,name, phone, anamnesis = display_profile()
        check_profile(age,name, phone,anamnesis)
        submitted = st.form_submit_button("Save Profile")
        if submitted:
            check_profile(age, name, phone,anamnesis)
            if st.session_state.incomplete_info == False:
                save_user_data(age,name, phone, anamnesis)
            else:
                st.warning('Please complete your profile')
if __name__ == "__main__":
    st.set_page_config(page_title="HI-card", layout="centered", initial_sidebar_state="auto", menu_items=None)
    user_info = st.session_state.user_info
    #st.write(user_info)
    st.header(f"Hi, {user_info['displayName']}")
    st.markdown('this page is used to register and update your information')
    col1, col2 = st.columns([5, 1])
    with col1:
        main()
    with col2:
        functions.make_sidebar()
    info = st.session_state.incomplete_info

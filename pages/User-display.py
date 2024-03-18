from utils import functions
import streamlit as st
from firebase_admin import firestore
import json
from google.oauth2.service_account import Credentials
import io
import base64
import numpy as np
from PIL import Image


key_dict = json.loads(st.secrets["textkey"])
creds = Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

css = '''
<style>
    [data-testid='stImage'] {
        width: 200px;
        height: 200px;
        border-radius: 50%;
        overflow: hidden;
    }
    }

    [data-testid='stFileUploader'] {
        width: max-content;
    }
    [data-testid='stFileUploader'] section {
        padding: 0;
        float: left;
    }
    [data-testid='stFileUploader'] section > input + div {
        display: none;
    }
    [data-testid='stFileUploader'] section + div {
        float: right;
        padding-top: 0;
    }

</style>
'''

st.markdown(css, unsafe_allow_html=True)


def upload_and_convert_image(user_info):
  uploaded_file = st.file_uploader("Choose your avatar", type=["jpg", "png", "jpeg"],help ='gregrg')
  if uploaded_file is not None:
    # Read the image data
    image_bytes = uploaded_file.read()
    image = Image.open(io.BytesIO(image_bytes))
    image = functions.resize_image(image, 600)
    image1 = io.BytesIO(image_bytes)
    buffer = io.BytesIO()
    image.save(buffer, format=image.format)  # Use original format
    image = buffer.getvalue()

    db = firestore.client()
    doc_ref = db.collection("Users").document(user_info['localId'])
    doc_ref.set({'Image': image}, merge=True)
    
def load_stored_image():
    """
    Loads the stored image data from Firestore and converts it back to a NumPy array.
    """
    # Reference to Firestore database (assuming collection exists)
    db = firestore.client()
    doc_ref = db.collection("Users").document(user_info['localId'])

    # Get the image data (Base64 string)
    doc = doc_ref.get()
    image_data = doc.to_dict().get('Image')

    if image_data is None:
        return None
    
    return st.image(image_data, width=200, use_column_width ='auto') # Or return the PIL Image object

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
    user_info = st.session_state.user_info
    #st.write(user_info)
    col1, col2 = st.columns([2, 3])
    with col1:
        load_stored_image()
        
    with col2:
        st.header(f"Hi, {user_info['displayName']}")
        upload_and_convert_image(user_info)
    col1, col2 = st.columns([5, 1])
    with col1:
        main()
    with col2:
        functions.make_sidebar()
    info = st.session_state.incomplete_info
    
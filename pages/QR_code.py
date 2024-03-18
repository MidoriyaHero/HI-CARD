import streamlit as st
import qrcode
import io
from utils import functions
from firebase_admin import firestore
import json
from google.oauth2.service_account import Credentials
from PIL import Image

key_dict = json.loads(st.secrets["textkey"])
creds = Credentials.from_service_account_info(key_dict)
db = firestore.Client(credentials=creds)

# Function to generate QR code and return image bytes
def generate_qr_code_bytes(data):
    qr = qrcode.QRCode(version=1, box_size=10, border=4)
    qr.add_data(data)
    qr.make(fit=True)
    img_buffer = io.BytesIO()
    qr.make_image(fill_color="black", back_color="white").save(img_buffer, format="PNG")

    db = firestore.client()
    doc_ref = db.collection("Users").document(user_info['localId'])
    doc_ref.set({'QR':img_buffer.getvalue()}, merge=True)
    st.success("Profile updated successfully!")
    return img_buffer.getvalue()

def download_and_display_qr_code(data):
    # Offer download button
    st.download_button(
        label="Download QR Code",
        data=data,
        file_name= user_info['displayName']+".png",
        mime="image/png",)
        # Display the QR code image
    st.image(data, width=200)

def main():
    # Main app
    st.title("QR Code Generator")
    #change path here when deploy
    data_to_encode = 'https://show-info.streamlit.app/?uid=' + user_info['localId']
    doc_ref = db.collection("Users").document(user_info['localId'])
    doc = doc_ref.get()
    dic = doc.to_dict()
    if info == True:
        st.warning('Please complete your profile')
    elif 'QR' not in dic.keys():
        if st.button("Generate QR Code", type="primary"):
            qr_code_bytes = generate_qr_code_bytes(data_to_encode)
            download_and_display_qr_code(qr_code_bytes)
    else:
        col1,col2,col3 = st.columns([4,2,5])
        with col1:
            download_and_display_qr_code(dic.get('QR'))
        with col2:
            st.write('OR')
        with col3:
            if st.button("Regenerate QR Code"):
                qr_code_bytes = generate_qr_code_bytes(data_to_encode)


if __name__ == "__main__":
    user_info = st.session_state.user_info
    info = st.session_state.incomplete_info
    
    col1, col2 = st.columns([5, 1])
    with col1:
        main()
    with col2:
        functions.make_sidebar()
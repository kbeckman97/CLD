import streamlit as st
import boto3
from PIL import Image
import os

# localhost (Programm starten) aufrufen im terminal mit streamlit run main.py
# Programm stoppen mit strg +c
# neues package installieren pip install package name
s3 = boto3.resource(
    service_name='s3',
    region_name='eu-central-1',
    aws_access_key_id=st.secrets["AccesskeyID"],
    aws_secret_access_key=st.secrets["Secretaccesskey"]
)

def load_image(img):
    im = Image.open(img)
    #image = np.array(im)
    return im


def main():
    uploadFile = st.file_uploader(label="Upload files here", type=['jpg', 'png'])
    if uploadFile is not None:
        # Perform your Manupilations (In my Case applying Filters)
        img = load_image(uploadFile)
        st.image(img)
        st.write("Image Uploaded Successfully")
        if st.button("Save and upload"):
            img.save('Testbild.png')
            s3.Bucket('mybucket-tes-3').upload_file(Filename='Testbild.png', Key='Test_Webseite/Testbild.png')
            #os.remove('CloudComputing/Testbild.png')
    else:
        st.write("Make sure you image is in JPG/PNG Format.")
    if st.button("Click me download"):
        s3.Bucket('mybucket-tes-3').download_file(Key='Test_Webseite/Testbild.png', Filename='Testbild_download.png')
        img = Image.open('Testbild_download.png')
        st.image(img)


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


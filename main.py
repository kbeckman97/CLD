import botocore.exceptions
import streamlit as st
import boto3
from PIL import Image
from datetime import datetime
import time
import os

currentTime = None


# localhost (Programm starten) aufrufen im terminal mit streamlit run main.py
# Programm stoppen mit strg +c
# neues package installieren pip install package name
s3 = boto3.resource(
    service_name='s3',
    region_name='eu-central-1',
    aws_access_key_id="AccesskeyID",
    aws_secret_access_key="Secretaccesskey"
)

def load_image(img):
    im = Image.open(img)
    #image = np.array(im)
    return im


def main():
    global currentTime
    uploadFile = st.file_uploader(label="Upload files here", type=[ 'png'])
    if uploadFile is not None:
        # Perform your Manupilations (In my Case applying Filters)
        img = load_image(uploadFile)
        st.image(img)
        st.write("Image Uploaded Successfully")
        if st.button("Save and upload"):

            now = datetime.now()
            currentTime = now.strftime("%d-%m-%Y-%H-%M-%S")
            imageNameAWS_upload = "Test_Webseite/" + currentTime + ".PNG"
            imageNameStre_upload = currentTime + ".PNG"

            img.save(imageNameStre_upload)
            s3.Bucket('mybucket-tes-3').upload_file(Filename=imageNameStre_upload, Key=imageNameAWS_upload)
            os.remove(imageNameStre_upload)
            with st.spinner("Waiting"):
                time.sleep(45)
            imageNameStre_download = currentTime + "Download.PNG"
            imageNameAWS_download = "processed_images/" + currentTime + ".PNG"
            try:
                s3.Bucket('mybucket-tes-3').download_file(Key=imageNameAWS_download, Filename=imageNameStre_download)
            except botocore.exceptions.ClientError:
                s3.Bucket('mybucket-tes-3').download_file(Key=imageNameAWS_download, Filename=imageNameStre_download)

            img = Image.open(imageNameStre_download)
            st.image(img)

            print("Download Sucessfull")
            with open(imageNameStre_download, "rb") as file:
                btn = st.download_button(
                label = "Download image with bounding boxes",
                data = file,
                file_name = "Strahlen.png",
                mime = "image/png"
                )
    else:
        st.write("Make sure you image is in PNG Format.")

    convertImage = st.file_uploader(label="convert images", type=['png'])
    if convertImage is not None:
        imgConvert = load_image(convertImage)
        st.image(imgConvert)
        st.write("Image Uploaded Successfully")
        if st.button("Convert to grayscale"):
            imgGray = imgConvert.convert('1')
            imgGray.save('test_gray.png')
            st.image(imgGray)

            with open("test_gray.png", "rb") as file:
                btn = st.download_button(
                label = "Download grayscale image",
                data = file,
                file_name = "test_gray.png",
                mime = "image/png"
                )


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()

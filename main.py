import botocore.exceptions
import numpy as np
import skimage.measure
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
    aws_access_key_id=st.secrets["AccesskeyID"],
    aws_secret_access_key=st.secrets["Secretaccesskey"]
)


def load_image(img):
    im = Image.open(img)
    return im


def main():

    for file in os.listdir("images"):
        os.remove("images/" + file)

    uploadFile = st.file_uploader(label="Upload files here", type=[ 'png'])
    if uploadFile is not None:
        # Perform your Manupilations (In my Case applying Filters)
        img_upload = load_image(uploadFile)
        st.image(img_upload)
        st.write("Image Uploaded Successfully")
        if st.button("Save and upload"):

            now = datetime.now()
            currentTime = now.strftime("%d-%m-%Y-%H-%M-%S")
            imageNameAWS_upload = "Test_Webseite/" + currentTime + ".PNG"
            imageNameStre_upload = "images/" + currentTime + ".PNG"

            img_upload.save(imageNameStre_upload)
            s3.Bucket('mybucket-tes-3').upload_file(Filename=imageNameStre_upload, Key=imageNameAWS_upload)

            with st.spinner("Waiting"):
                time.sleep(45)
            imageNameStre_download = "images/" + currentTime + "Download.PNG"
            imageNameAWS_download = "processed_images/" + currentTime + ".PNG"
            try:
                s3.Bucket('mybucket-tes-3').download_file(Key=imageNameAWS_download, Filename=imageNameStre_download)
            except botocore.exceptions.ClientError:
                s3.Bucket('mybucket-tes-3').download_file(Key=imageNameAWS_download, Filename=imageNameStre_download)

            print("Download Sucessfull")
            with open(imageNameStre_download, "rb") as file:
                btn = st.download_button(
                label = "Download image with bounding boxes",
                data = file,
                file_name = "images/" + "Strahlen.png",
                mime = "image/png"
                )

    else:
        st.write("Make sure you image is in PNG Format.")

    convertImage = st.file_uploader(label="convert images", type=['png'])
    if convertImage is not None:
        imgConvert = load_image(convertImage)
        st.image(imgConvert)
        st.write("Image Uploaded Successfully")

        now = datetime.now()
        currentTime = now.strftime("%d-%m-%Y-%H-%M-%S")
        imageNameGray = "images/" + currentTime + ".png"
        if st.button("Convert to grayscale"):
            imgGray = imgConvert.convert('L')
            #size = [1280, 720]
            #imgGray = imgGray.resize(size)
            imgGray = np.array(imgGray)
            imgGray = skimage.measure.block_reduce(imgGray, (3,3), np.max)
            imgGray = Image.fromarray(imgGray)
            imgGray.save(imageNameGray)
            st.image(imgGray)

            with open(imageNameGray, "rb") as file:
                btn = st.download_button(
                label = "Download grayscale image",
                data = file,
                file_name = currentTime + ".png",
                mime = "image/png"
                )



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



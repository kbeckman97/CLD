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


    st.title('Nebelspurenanalyse von Strahlen')
    "Bitte laden Sie in den Drag and Drop File Uploader ein Bild hoch, auf dem die Strahlen analysiert werden sollen. Ein Programm analysiert das Bild und markiert die vorhandenen Strahlen. Dieses Bild kann dann anschließend heruntergeladen werden."

    uploadFile = st.file_uploader(label="Bitte fügen Sie hier ihr zu analysierendes Bild ein:", type=[ 'png', 'jpg'])
    if uploadFile is not None:
        # Perform your Manupilations (In my Case applying Filters)
        img_upload = load_image(uploadFile)
        st.image(img_upload)
        st.success("Image Uploaded Successfully")
        if st.button("Save and upload"):
            with st.spinner("Bitte warten, Ihr Bild wird hochgeladen."):
                now = datetime.now()
                currentTime = now.strftime("%d-%m-%Y-%H-%M-%S-%f")
                imageNameAWS_upload = "Test_Webseite/" + currentTime + ".PNG"
                imageNameStre_upload = "images/" + currentTime + ".PNG"
                imageNameStre_download = "images/" + currentTime + "Download.PNG"
                imageNameAWS_download = "processed_images/" + currentTime + ".PNG"

                img_upload.save(imageNameStre_upload)
                s3.Bucket('mybucket-tes-3').upload_file(Filename=imageNameStre_upload, Key=imageNameAWS_upload)

            has_downloaded = False
            for i in range(0,20):
                with st.spinner("Bitte warten, Ihr Bild wird analysiert."):
                    time.sleep(3)
                try:
                    s3.Bucket('mybucket-tes-3').download_file(Key=imageNameAWS_download, Filename=imageNameStre_download)
                    has_downloaded = True
                    break
                except botocore.exceptions.ClientError:
                    continue
            if has_downloaded:
                st.success("Download Sucessfull")
                img_download = load_image(imageNameStre_download)
                st.image(img_download)
                with open(imageNameStre_download, "rb") as file:
                    btn = st.download_button(
                    label = "Download image with bounding boxes",
                    data = file,
                    file_name = "images/" + "Strahlen.png",
                    mime = "image/png"
                    )
                s3.Object('mybucket-tes-3', imageNameAWS_download).delete()


            else:
                st.error("Es ist ein Fehler aufgetreten. Bitte wenden Sie sich an den Systemadministrator!")

    else:
        st.write("Sie haben noch kein Bild hochladen oder ihr Bild ist nicht im .png oder .jpg Format.")

    Kammer__Erklaerung, Kammer_bild = st.columns(2)
    with Kammer_bild:
        img_Kammer = load_image('Nebelspurenkammer.jpg')
        st.image(img_Kammer, width=300)
    with Kammer__Erklaerung:
        "In dieser Nebelkammer wird die sonst unsichtbare inonisierende Strahlung mit Hilfe von Alkoholnebel sichtbar gemacht. Die unterschiedlichen Strahlenarten sind hierbei nicht so einfach voneinander zu unterscheiden."
        "Daher gibt es hier einen kurzen Einblick in die Unterschiede zwischen Alpha-, Betastrahlung und Myonen. Ein typischer Alpha-Strahler ist Uran."

    st.subheader('Alpha Strahlung')
    alpha_bild, Alpha_Erklaerung = st.columns(2)
    with alpha_bild:
        alpha = load_image('alpha.jpg')
        st.image(alpha)
    with Alpha_Erklaerung:
        "Alpha-Strahlung ist eine stark ionisierende Strahlung, die bei radioaktiven Zerfall freigesetzt wird. Sie besteht aus zwei Protonen und zwei Neutronen."
        "Von einem Alpha-Strahler gehen ungefähr gleichlange Spuren aus. Die Länge der Spuren liegt im Bereich von 1-1,6 cm"
    st.subheader('Beta Strahlung')
    beta_bild, Beta_Erklaerung = st.columns(2)
    with beta_bild:
        alpha = load_image('beta.jpg')
        st.image(alpha)
    with Beta_Erklaerung:
        "Bei der Beta-Strahlung gibt es sowohl die Beta(+)- als auch die Beta(-)-Strahlung. Bei der Beta(+)-Strahlung wird ein Elektron freigesetzt. Bei der Beta(-)-Strahlung wird ein Positron freigesetzt."
        "Beta-Strahlung lässt sich nur schwer erkennen, da sie oft im Hintergrundnebel untergehen. Diese Strahlung ist hauptsächlich durch Kurven zu erkennen. Die schnelleren Strahlen bleiben größtenteils geradlining"
    st.subheader('Myonen')
    Myonen_bild, Myonen_Erklaerung = st.columns(2)
    with Myonen_bild:
        myonen = load_image('Myonen.jpg')
        st.image(myonen)
    with Myonen_Erklaerung:
        "Myonen sind kosmische Strahlen. Sie taucht nur sehr selten auf und ist erkennbar durch sehr große und dichte Spuren."

    # st.header('Farbbilder konvertieren')
    # "Hier können Sie Farbbilder in 8-Bit Grauwertbilder konvertieren. Bitte laden Sie ein Bild hoch:"
    # convertImage = st.file_uploader(label="convert images", type=['png'])
    # if convertImage is not None:
    #     imgConvert = load_image(convertImage)
    #     st.image(imgConvert)
    #     st.write("Image Uploaded Successfully")
    #
    #     now = datetime.now()
    #     currentTime = now.strftime("%d-%m-%Y-%H-%M-%S")
    #     imageNameGray = "images/" + currentTime + ".png"
    #     if st.button("Convert to grayscale"):
    #         imgGray = imgConvert.convert('L')
    #         #size = [1280, 720]
    #         #imgGray = imgGray.resize(size)
    #         imgGray = np.array(imgGray)
    #         #imgGray = skimage.measure.block_reduce(imgGray, (3,3), np.max)
    #         M, N = imgGray.shape
    #         K = 3
    #         L = 3
    #
    #         MK = M // K
    #         NL = N // L
    #         imgGray = imgGray[:MK * K, :NL * L].reshape(MK, K, NL, L).max(axis=(1, 3))
    #         imgGray = Image.fromarray(imgGray)
    #         imgGray.save(imageNameGray)
    #         st.image(imgGray)
    #
    #         with open(imageNameGray, "rb") as file:
    #             btn = st.download_button(
    #             label = "Download grayscale image",
    #             data = file,
    #             file_name = currentTime + ".png",
    #             mime = "image/png"
    #             )



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()



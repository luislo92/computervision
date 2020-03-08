from google.cloud import vision
from google.oauth2 import service_account
import io
import re
import string
import pandas as pd

def load_image(path):
    #'/Users/luislosada/Downloads/IMG_3065.JPG'
    path = path

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    return content

#GCP
def set_up():
    credentials = service_account.Credentials.from_service_account_file(
        '/Users/luislosada/Downloads/Hack NYU 2020-ede401beb252.json')

    client = vision.ImageAnnotatorClient(credentials=credentials)

    return client


#Vision
image = vision.types.Image(content=load_image('/Users/luislosada/Downloads/IMG_3065.JPG'))

response = set_up().text_detection(image=image)
texts = response.text_annotations

def clean_response(texts):
    # Vision

    if response.error.message:
        raise Exception(
            '{}\nFor more info on error messages, check: '
            'https://cloud.google.com/apis/design/errors'.format(
                response.error.message))
    else:

        word = []
        lines = texts[0].description.split('\n')
        for text in lines:
            #Eliminating long words or payments

            if len(text) < 100 \
                and len(text) > 2 \
                and "$" not in text:

            #Eliminating Numbers
                try:
                    if (len("".join(re.findall(r'[0-9]+',text))) / len(text)) < 0.3:
                        stringIn = text
                        stringOut = stringIn.translate(str.maketrans('', '', string.punctuation))
                        word.append(stringOut.lower())

                except IndexError:
                    stringIn = text
                    stringOut = stringIn.translate(str.maketrans('', '', string.punctuation))
                    word.append(stringOut.lower())

    return word

resp = clean_response(texts)

resp
df = pd.read_csv('/Users/luislosada/PycharmProjects/computervision/nutrition_scrappe.csv',index_col=0)

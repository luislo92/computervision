from google.cloud import vision
from google.oauth2 import service_account
import io
import re
import string
import pandas as pd

credentials = service_account.Credentials.from_service_account_file(
    '/Users/luislosada/Downloads/Hack NYU 2020-ede401beb252.json')

client = vision.ImageAnnotatorClient(credentials=credentials)
path = '/Users/luislosada/Downloads/IMG_3065.JPG'
with io.open(path, 'rb') as image_file:
    content = image_file.read()

image = vision.types.Image(content=content)

response = client.text_detection(image=image)
texts = response.text_annotations

def clean_response(texts):

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

df = pd.read_csv('/Users/luislosada/PycharmProjects/computervision/nutrition_scrappe.csv',index_col=0)

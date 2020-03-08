from google.cloud import vision
from google.oauth2 import service_account
import io
import re
import string

"""
There are three necessary inputs for this script to run:
1) Query DB for the Foods Table
2) Input of the DB on the bert_sim_model function
3) Input of the path of the image uploaded by the client

Finally declare the output of the variable to a desired location the output is a data frame like this:

|Item| Accuracy Score | Calories |
##################################
|____|________________|__________|
"""

#load image
def load_image(path):

    path = path

    with io.open(path, 'rb') as image_file:
        content = image_file.read()

    return content

# GCP
def set_up():
    credentials = service_account.Credentials.from_service_account_file(
        '/Users/luislosada/Downloads/Hack NYU 2020-ede401beb252.json')

    client = vision.ImageAnnotatorClient(credentials=credentials)

    return client


#1 Vision

def clean_response(image_path):
    # Vision

    image = vision.types.Image(content=load_image(image_path))

    response = set_up().text_detection(image=image)
    texts = response.text_annotations

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


#################################################
#---------------------------------------------------#

#Getting the data data from the DB

#Query from the db.execute('SELECT DISTINCT restaurant FROM foods;')

def select_rest(db_path,image_path):

    resp = clean_response(image_path)
    df = db_path
    rest_comp = " ".join(resp)
    for rest in list(set(df.restaurant)):
        if rest.replace("-", " ") in rest_comp:
            ind = rest
            resp = [line for line in resp if rest not in line]
            break
    return [ind,resp]


#query the entire DB db.execute('SELECT * FROM foods;')

def bert_sim_model(db_path,image_path):
    """
    Loads the Bert Similarity pre-trained model to analyze the fuzzy words
    """

    from semantic_text_similarity.models import WebBertSimilarity
    import pandas as pd

    #Building the Model
    model = WebBertSimilarity(device='cpu', batch_size=10)
    df = db_path
    rest_s = select_rest(db_path, image_path)
    ind,fixed_rep = rest_s[0],rest_s[1]

    #Comparisons
    to_compare = df[df.restaurant == ind]
    m = []
    for res in fixed_rep:
        for food in to_compare.food_name:
            pred = float(model.predict([(res, food)]))
            if pred > 2:
                m.append([res, pred, to_compare.mean_value[to_compare.food_name == food]])


    df_final = pd.DataFrame(columns=['item','pred','calories'])

    for row in m:
        df = pd.DataFrame({'item': row[0],
                           'pred': row[1],
                           'calories':row[2]})
        df_final = pd.concat([df_final,df])
    idx = df_final.groupby(['item'])['pred'].transform(max) == df_final['pred']

    return df_final[idx].reset_index(drop=True)



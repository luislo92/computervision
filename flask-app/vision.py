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

#################################################
#---------------------------------------------------#

def select_db(path):

    import pandas as pd

    df = pd.read_csv(path, index_col=0)
    return df

def select_rest(db_path,resp):
    df = select_db(db_path)
    rest_comp = " ".join(resp)
    for rest in list(set(df.restaurant)):
        if rest.replace("-", " ") in rest_comp:
            ind = rest
            resp = [line for line in resp if rest not in line]
            break
    return [ind,resp]

def bert_sim_model(db_path,resp):
    """
    Loads the Bert Similarity pre-trained model to analyze the fuzzy words
    """

    from semantic_text_similarity.models import WebBertSimilarity
    import pandas as pd

    #Building the Model
    model = WebBertSimilarity(device='cpu', batch_size=10)
    df = pd.read_csv(db_path)
    ind,fixed_rep = select_rest(db_path,resp)[0],select_rest(db_path,resp)[1]

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

dd = bert_sim_model('/Users/luislosada/PycharmProjects/computervision/flask-app/nutrition_scrappe.csv',resp=resp)

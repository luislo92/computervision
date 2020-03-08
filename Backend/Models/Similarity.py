from semantic_text_similarity.models import WebBertSimilarity
import pandas as pd

def select_db(path):
    df = pd.read_csv(path, index_col=0)
    return df

def select_rest(db_path,resp):
    df = select_db(db_path)
    rest_comp = " ".join(resp)
    for rest in list(set(df.restaurant)):
        if rest.replace("-", " ") in rest_comp:
            ind = rest
            break
    return ind


def Bert_Sim_Model(db_path,path,resp):
    """
    Loads the Bert Similarity pre-trained model to analyze the fuzzy words
    """
    model = WebBertSimilarity(device='cpu', batch_size=10)
    df = select_db(db_path)
    ind = select_rest(path,resp)

    to_compare = df[df.restaurant == ind]
    m = []
    for res in resp:
        for food in to_compare.name:
            pred = float(model.predict([(res, food)]))
            if pred > 2:
                m.append([res, to_compare.mean_value[to_compare.name == food]])

    df_final = pd.DataFrame(columns=['item','calories'])
    for row in m:
        df = pd.DataFrame(row)
        df_final = pd.concat([df_final,df])

    return df_final
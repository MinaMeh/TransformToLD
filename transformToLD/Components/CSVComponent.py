import pandas as pd
from transformToLD.Helpers.explore import get_vocab
from transformToLD.Helpers.preprocess import translate_word,get_combinaisons

def trait_csv(csv_file, vocabs_list):
    file= pd.read_csv(csv_file,delimiter=",")
    #file= csv.reader(csv_file   ,delimiter=",")
    headers= file.columns
    terms=[]
    for col in headers:
        term={}
        data= get_vocab(col,vocabs_list,'property')
        term["property"] = col
        term["result"] = data
        terms.append(term)
    return terms

def read_csv(csv_file):
    file = pd.read_csv(csv_file)
    cols = file.columns
    headers=[]
    for col in cols:
        header = dict()
        header["name"]=col
        translated = translate_word(col)
        header['translated']= translated
        combinaison = get_combinaisons(translated)
        header['combinaison'] = combinaison
        headers.append(header)
    content = file.values.tolist()
    lines=file.shape[0]
    columns= file.shape[1]
    return {"headers": headers, 'content':content, 'columns': columns, "lines":lines}
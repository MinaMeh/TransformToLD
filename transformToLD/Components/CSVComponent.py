import pandas as pd
from transformToLD.Helpers.explore import get_vocab
from transformToLD.Helpers.preprocess import translate_word, get_combinaisons
import toolz


def trait_csv(csv_file, vocabs_list):
    file = pd.read_csv(csv_file, delimiter=",")
    # file= csv.reader(csv_file   ,delimiter=",")
    headers = file.columns
    terms = []
    for col in headers:
        term = {}
        data = get_vocab(col, vocabs_list, 'property')
        term["property"] = col
        term["result"] = data
        terms.append(term)
    return terms


def explore_csv(columns, vocabs_list):
    '''
    Map csv columns to LOV terms
    '''
    terms = []
    for col in columns:
        terms.append(explore_column(col, vocabs_list))

    return terms


def explore_column(column, vocabs_list):
    """
    Get column terms in the LOV cloud
    """
    transated = translate_word(column)
    combinaisons = get_combinaisons(transated)
    term = {}
    term["property"] = column
    term["result"] = []
    for comb in combinaisons:
        data = get_vocab(comb, vocabs_list, 'property')
        term["result"] += data
    term['result'].sort(key=lambda term: term.get('score'), reverse=True)
    return term


def read_csv(csv_file):
    file = pd.read_csv(csv_file)
    cols = file.columns
    headers = []
    for col in cols:
        header = dict()
        header["name"] = col
        translated = translate_word(col)
        header['translated'] = translated
        combinaison = get_combinaisons(translated)
        header['combinaison'] = combinaison
        headers.append(header)
   # content = file.values.tolist()
    lines = file.shape[0]
    columns = file.shape[1]
    return {"headers": headers, 'columns': columns, "lines": lines}

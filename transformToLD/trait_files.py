import pandas as pd
import csv
from .searchTerms import *
def trait_csv(csv_file):
    file= pd.read_csv(csv_file,delimiter=",")
    #file= csv.reader(csv_file   ,delimiter=",")
    line=0
    headers= file.columns
    terms=dict()
    for col in headers:
        data= getVocab(col,"property")
        terms[col]=data
    return terms

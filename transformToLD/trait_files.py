import pandas as pd
import csv
from .searchTerms import getVocab
import lxml.html as lh
def trait_csv(csv_file):
    file= pd.read_csv(csv_file,delimiter=",")
    #file= csv.reader(csv_file   ,delimiter=",")
    headers= file.columns
    terms=dict()
    for col in headers:
        data= getVocab(col,"property")
        terms[col]=data
    return terms

def trait_html(html_file):
    file= open (html_file).read()
    data= lh.fromstring(file)
    tr_elements= data.xpath('//tr')
    headers=[]
    terms=dict()

    #For each row, store each first element (header) and an empty list
    for t in tr_elements[0]:
        name=t.text_content()
        headers.append(name)
        data= getVocab(name,"property")
        terms[name]=data

    return terms
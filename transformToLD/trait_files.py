import pandas as pd
import csv
from .searchTerms import getVocab
import lxml.html as lh
from bs4 import BeautifulSoup as bs
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
    soup= bs(file,'lxml')
    tables= soup.find_all("table")
    tables_content=dict()
    for i in range (len(tables)):
        data= lh.fromstring(str(tables[i]))
        tr_elements= data.xpath('//tr')
        headers=[]
        tables_content[str(i)]={}
        terms=dict()
        for header in tr_elements[0]:
            name=header.text_content()
            headers.append(name)
            terms[name]=getVocab(name,"property")
        tables_content[str(i)]['headers']=headers
        tables_content[str(i)]['terms']=terms
        tables_content[str(i)]["elements"]=[]
        for row in tr_elements[1:]:
            line=[]
            for cell in row:
                line.append(cell.text_content())
            tables_content[str(i)]["elements"].append(line)

    return tables_content
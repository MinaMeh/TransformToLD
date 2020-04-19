from transformToLD.Helpers.explore import get_vocab
import lxml.html as lh
from bs4 import BeautifulSoup as bs
from transformToLD.Components.TexteComponent import explore_text
from transformToLD.Helpers.preprocess import translate_word, get_combinaisons
def trait_html(html_file,vocabs_list):
    file= open (html_file).read()
    soup= bs(file,'lxml')
    tables = soup.find_all("table")
    tables_results =explore_tables(tables,vocabs_list)
    paragraphs = [par.text for par in soup.find_all("p")]
    paragraph_results = explore_text(paragraphs, vocabs_list)
    num_tables = len(tables_results)
    num_paragraphs= len(paragraph_results)
    results= {"tables": tables_results, "num_tables":num_tables,"paragraphs": paragraph_results, "num_paragraphs": num_paragraphs}
    return results

def read_html(html_file):
    file = open(html_file).read()
    soup = bs(file, 'lxml')
    paras = [par.text for par in soup.find_all("p")]
    paragraphs= explore_text(paras)
    tables_html = soup.find_all("table")
    tables=get_tables_content(tables_html)
    num_tables = len(tables)
    num_paragraphs= len(paragraphs)
    results = {"tables": tables, "num_tables": num_tables, "paragraphs": paragraphs, "num_paragraphs": num_paragraphs}
    return results

def get_tables_content(tables):
    tables_results = []
    for i in range(len(tables)):
        tables_content = dict()
        data= lh.fromstring(str(tables[i]))
        tr_elements= data.xpath('//tr')
        headers=[]
        tables_content["id"]=i
        for header in tr_elements[0]:
            head=dict()
            name = header.text_content()
            head['name'] = name
            head['translated'] = translate_word(name)
            head['combinaison']= get_combinaisons(name)
            headers.append(head)
        tables_content['headers'] = headers
        tables_content['columns']=len(headers)
        tables_content["elements"]=[]
        for row in tr_elements[1:]:
            line=[]
            for cell in row:
                line.append(cell.text_content())
            tables_content["elements"].append(line)
        tables_content["lines"]= len(tables_content["elements"])
        tables_results.append(tables_content)
    return tables_results


def explore_tables(tables, vocabs_list):
    '''
    explores the tables of HTML page and returns mapping of columns names to LOV properties
    '''
    tables_results = []
    for i in range(len(tables)):
        tables_content = dict()
        data= lh.fromstring(str(tables[i]))
        tr_elements= data.xpath('//tr')
        headers=[]
        tables_content["id"]=i
        terms=[]
        for header in tr_elements[0]:
            term=dict()
            name=header.text_content()
            headers.append(name)
            term["property"]=name
            term["result"] = get_vocab(name, vocabs_list, "property")
            terms.append(term)
        tables_content['headers']=headers
        tables_content['terms']=terms
        tables_content["elements"]=[]
        for row in tr_elements[1:]:
            line=[]
            for cell in row:
                line.append(cell.text_content())
            tables_content["elements"].append(line)
        tables_results.append(tables_content)
    return tables_results



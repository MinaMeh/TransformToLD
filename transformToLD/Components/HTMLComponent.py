from transformToLD.Helpers.explore import get_entities, get_vocab
import lxml.html as lh
from bs4 import BeautifulSoup as bs

def trait_html(html_file,vocabs_list):
    file= open (html_file).read()
    soup= bs(file,'lxml')
    tables = soup.find_all("table")
    tables_results =explore_tables(tables,vocabs_list)
    paragraphs = [par.text for par in soup.find_all("p")]
    paragraph_results= explore_text(paragraphs,vocabs_list)
    results= {"tables": tables_results, "paragraphs": paragraph_results}
    return results


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


def explore_text(paragraphs, vocabs_list):
    '''
    explores paragraphs and returns mapping between entities and LOV classes
    '''
    paragraph_results=[]
    for paragraph in paragraphs:
        paragraph_entities = {}
        paragraph_entities['paragraph']=paragraph
        paragraph_entities['entities'] = get_entities(paragraph,vocabs_list)
        paragraph_results.append(paragraph_entities)
    return paragraph_results

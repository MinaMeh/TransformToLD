import lxml.html as lh
from bs4 import BeautifulSoup as bs
import spacy
import pandas as pd


def extract_text_data(file):
    ''' Extracts the sentences of a text file '''
    results = dict()
    with open(file, "r") as f:
        content = f.read()
        results['paragraph'] = content
        results['sentences'] = get_sentences(content)
        return results


def extract_csv_data(csv_file, separator=";"):
    ''' Extracts Data of csv file 
        Returns: headers, number of lines , number of columns
        stores the content in the database
    '''
    file = pd.read_csv(csv_file, delimiter=separator)
    headers = file.columns
    lines = file.shape[0]
    columns = file.shape[1]
    return {"headers": headers, 'columns': columns, "lines": lines}


def extract_html_data(file, extract_tables=False, extract_paragraphs=False):
    '''
    Extract HTML file data
    if tables==true, it extracts tables
    if paragraphs==true it extracts paragraphs
    '''
    file_content = open(file).read()
    soup = bs(file_content, 'lxml')
    tables = []
    num_tables = 0
    paragraph_results = []
    num_paragraphs = 0
    if (extract_tables):
        tables_html = soup.find_all("table")
        tables = get_tables_content(tables_html)
        num_tables = len(tables)
    if (extract_paragraphs):
        paragraphs = [par.text for par in soup.find_all("p")]
        paragraph_results = get_paragraphs_sentences(paragraphs)
        num_paragraphs = len(paragraph_results)
    results = {"tables": tables, "num_tables": num_tables,
               "paragraphs": paragraph_results, "num_paragraphs": num_paragraphs}
    return results


def get_tables_content(tables):
    '''
    Extract data from HTML Tables
    Returns: headers, number of columns, number of lines
    Stores the content in a database
    '''
    tables_results = []
    for i in range(len(tables)):
        tables_content = dict()
        data = lh.fromstring(str(tables[i]))
        tr_elements = data.xpath('//tr')
        headers = []
        tables_content["id"] = i
        tables_content["selected"] = False

        for header in tr_elements[0]:
            head = dict()
            name = header.text_content()
            head = {"name": name, "selected": False}
            headers.append(head)
        tables_content['headers'] = headers
        tables_content['columns'] = len(headers)
        #tables_content["elements"] = []
        content = []
        for row in tr_elements[1:]:
            line = []
            for cell in row:
                line.append(cell.text_content())
            content.append(line)
            # tables_content["elements"].append(line)
        tables_content["lines"] = len(content)
        tables_results.append(tables_content)
    return tables_results


def get_paragraphs_sentences(paragraphs):
    '''
    Extracts the sentences of all paragraphs
    Returns the paragraph and its sentences
    '''
    paragraph_results = []
    i = 0
    for paragraph in paragraphs:
        result = dict()
        result['paragraph'] = paragraph
        result['id'] = i
        i += 1
        result['sentences'] = get_sentences(paragraph)
        paragraph_results.append(result)
    return paragraph_results


def get_sentences(paragraph, model="en_core_web_sm"):
    '''
    Extracts the sentences of a given paragraph
    '''
    sentences = []
    nlp = spacy.load(model)
    doc = nlp(paragraph)
    for sent in doc.sents:
        sentences.append(sent.text)
    return sentences

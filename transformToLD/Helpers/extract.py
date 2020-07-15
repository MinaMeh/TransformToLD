import lxml.html as lh
from bs4 import BeautifulSoup as bs
import spacy
import pandas as pd
import textrazor


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
    cols = file.columns
    headers = []
    for col in cols:
        head = {}
        head['name'] = col
        head['selected'] = False
        headers.append(head)
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
        tables = get_tables_content(tables_html, file)
        num_tables = len(tables)
    if (extract_paragraphs):
        paragraphs = [par.text for par in soup.find_all("p")]
        paragraph_results = get_paragraphs_sentences(paragraphs)
        num_paragraphs = len(paragraph_results)
    results = {"tables": tables, "num_tables": num_tables,
               "paragraphs": paragraph_results, "num_paragraphs": num_paragraphs}
    return results


def get_tables_content(tables, file):
    '''
    Extract data from HTML Tables
    Returns: headers, number of columns, number of lines
    Stores the content in a database
    '''
    tables_results = []

    for i in range(len(tables)):
        filename = "{}_{}.html".format(
            "".join(file.split(".")[:-1]), str(i), "html")
        with open(filename, "w") as f:
            f.write(str(tables[i]))
        # html_file = pd.read_html(filename)
        tables_content = dict()
        # data = lh.fromstring(str(tables[i]))
        # tr_elements = data.xpath('//tr')
        file_content = pd.read_html(filename)[0]
        headers = []
        tables_content["id"] = i
        tables_content["selected"] = False
        tables_content["filename"] = filename
        for header in file_content.columns:
            head = dict()
            name = header
            head = {"name": name, "selected": False}
            headers.append(head)
        tables_content['headers'] = headers
        tables_content['columns'] = len(headers)
        tables_content["lines"] = file_content.shape[0]
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
        result['selected'] = True

        i += 1
        result['sentences'] = get_sentences(paragraph)
        paragraph_results.append(result)
    return paragraph_results


def get_sentences(paragraph, model="en_core_web_sm"):
    '''
    Extracts the sentences of a given paragraph
    '''
    sentences = []
    textrazor.api_key = "4599791ae63e2fb4f39d911a2145db56469b306ba8fbd6eda53e65ce"

    client = textrazor.TextRazor(extractors=['entities', 'relations'])
    response = client.analyze(paragraph)
    for sent in response.sentences():
        sentence = dict()
        sentence['text'] = concatenate(sent.words)
        sentences.append(sentence)
    return sentences


def concatenate(word_list):
    term = ""
    for word in word_list:
        term += " " + word.token
    return term

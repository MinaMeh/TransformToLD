from transformToLD.Helpers.preprocess import get_entities


def read_text(file_uploaded):
    results={}
    with open(file_uploaded, "r") as f:
        content= f.read()
        results['text']= content
        results['entities'] = get_entities(content)
        return results


def explore_text(paragraphs):
    '''
    explores paragraphs and returns mapping between entities and LOV classes
    '''
    paragraph_results=[]
    for paragraph in paragraphs:
        paragraph_entities = {}
        paragraph_entities['paragraph']=paragraph
        paragraph_entities['entities'] = get_entities(paragraph)
        paragraph_results.append(paragraph_entities)
    return paragraph_results



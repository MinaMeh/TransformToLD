from transformToLD.Helpers.preprocess import get_entities, get_sentences, tagging_sentence


def read_text(file_uploaded):
    results = []
    with open(file_uploaded, "r") as f:
        content = f.read()
        results = explore_paragraph(content)
        return results


def explore_text(paragraphs):
    '''
    explores paragraphs and returns mapping between entities and LOV classes
    '''
    tags = []
    results = []
    paragraph_results = []
    for paragraph in paragraphs:
        result = explore_paragraph(paragraph)
        paragraph_results.append(result)
    return paragraph_results


def explore_paragraph(paragraph):
    """
    explore a paragraph and returns list of words with their tags
    """
    results = []
    sentences = get_sentences(paragraph)
    for sentence in sentences:
        result = dict()
        result["sentence"] = sentence
        result['tags'] = tagging_sentence(sentence)
        results.append(result)
    return results

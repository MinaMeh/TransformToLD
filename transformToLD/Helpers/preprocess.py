from googletrans import Translator
from transformToLD.Classes.classes import Tag
import spacy
import inflection
TYPE_MAPPING = {
    "PER": "person",
    "LOC": "location",
    "ORG": "organisation",
    "MISC": "misc"
}


def translate_word(word):
    '''
    translates a word to english
    '''
    translator = Translator()
    return translator.translate(word).text


def get_combinaisons(word):
    '''
    get all possible combinaisons of a compound word for example get_combinaisons("First Name") should return ["first name","firstName", "first_name", "firstname)] (separated,camel case,
    underscore, attached)
    '''
    words_list = word.split(" ")
    if len(words_list) > 1:  # word is separated
        separated = " ".join(words_list)
        underscore = "_".join(words_list)
        camel_case = ''.join(x.capitalize() for x in words_list)
        attached = ''.join(words_list)
        words_list = [separated, underscore, camel_case, attached]
    else:  # one word
        word = words_list[0]
        if "_" in words_list[0]:  # the word is with underscore
            word = word.split("_")
            attached = ''.join(word)
            separated = ' '.join(word)
            camelcase = ''.join(x.capitalize() for x in word)
            words_list.extend([attached, camelcase, separated])
        else:  #
            if is_camel_case(words_list[0]):  # word is camel case
                underscore = inflection.underscore(word)
                attached = "".join(underscore.split('_'))
                separated = " ".join(underscore.split('_'))
                words_list.extend([underscore, attached, separated])
            else:
                pass
    return list(set(words_list))


def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s


def get_class(entity):
    '''
    get_class return all possible classes URIS of the entity "entity" in the vocabularies "list_vocabs"
    '''
    return TYPE_MAPPING[entity]


def get_entities(paragraph, model='xx_ent_wiki_sm'):
    '''
    extract the entities of the paragraph "paragraph" using the model "model" and map it to classes of the vocabularies 
    present in the list "vocabs_list"
    '''
    nlp = spacy.load(model)
    doc = nlp(paragraph)
    entities = [Tag(X.text, get_class(X.label_)).to_dict()
                for X in doc.ents]
    return entities


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


def tagging_sentence(sentence, model="en_core_web_sm"):
    '''
    tags a sentence grammaticaly
    '''
    tags = get_entities(sentence)
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    for token in doc:
        if (token.pos_ == "VERB"):
            tags.append(Tag(token.text, token.pos_).to_dict())
    return tags
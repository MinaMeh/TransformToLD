import spacy


class Tag(object):
    def __init__(self, word, tag):
        self.word = word
        self.tag = tag

    def to_dict(self):
        return {
            "word": self.word,
            "tag": self.tag
        }


def tagging_sentence(sentence, model="en_core_web_sm"):
    '''
    tags a sentence grammaticaly
    '''
    tags = []
    nlp = spacy.load("en_core_web_sm")
    doc = nlp(sentence)

    for token in doc:
        tags.append(Tag(token.text, token.pos_).to_dict())
    return tags


sentence = "Bill Gates works at Microsoft Corporation"
print(tagging_sentence(sentence))

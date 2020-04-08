from googletrans import Translator
import inflection
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
    if len(words_list) > 1:  #word is separated
        separated = " ".join(words_list)
        underscore = "_".join(words_list)
        camel_case = ''.join(x.capitalize() for x in words_list)
        attached= ''.join(words_list)
        words_list=[separated,underscore, camel_case,attached]
    else:  #one word
        word = words_list[0]
        if "_" in words_list[0]:  #the word is with underscore
            word = word.split("_")
            attached = ''.join(word)
            separated= ' '.join(word)
            camelcase = ''.join(x.capitalize() for x in word)
            words_list.extend([attached, camelcase,separated])
        else:  #
            if is_camel_case(words_list[0]): #word is camel case
                underscore = inflection.underscore(word)
                attached = "".join(underscore.split('_'))
                separated = " ".join(underscore.split('_'))
                words_list.extend([underscore, attached, separated])
            else:
                pass
    return words_list
                
def is_camel_case(s):
    return s != s.lower() and s != s.upper() and "_" not in s

import textrazor


def concatenate(word_list):
    term = ""
    for word in word_list:
        term += " " + word.token
    return term


textrazor.api_key = "4599791ae63e2fb4f39d911a2145db56469b306ba8fbd6eda53e65ce"
client = textrazor.TextRazor(extractors=['entities', 'relations'])
client.set_entity_freebase_type_filters(["/organization/organization"])
client.set_entity_dbpedia_type_filters(["Company"])

response = client.analyze(
    "Spain's stricken Bankia expects to sell off its vast portfolio of industrial holdings that includes a stake in parent company of British Airways and Iberia.")

for relation in response.relations():
    print("relation")
    print("predicate_words {}".format(concatenate(relation.predicate_words)))
    for param in relation.params:
        print("param words {}".format(concatenate(param.param_words)))
        print("param reation {}".format(param.relation))

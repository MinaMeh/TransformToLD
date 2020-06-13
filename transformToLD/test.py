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

relations = []
for relation in response.relations():
    rel = dict()
    rel['predicate'] = concatenate(relation.predicate_words)
    i = 0
    rel["param"] = []

    for param in relation.params:
        params = dict()
        params['param'] = concatenate(param.param_words)
        params['param relation'] = param.relation
        rel["param"].append(params)
    relations.append(rel)
print(rel)

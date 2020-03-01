import argparse
import requests
vocab_list = []
term="first_name"
term_type=""
URL = "https://lov.linkeddata.es/dataset/lov/api/v2/term/suggest?q="+term
r = requests.get(URL)
data = r.json()
for element in data["suggestions"]:
    print (element)
import tabula
import pdftotext
import io
import pandas as pd
import re
file = "/home/mina/Downloads/Document.pdf"
Datatypes = {
    "int64": "xsd:int",
    "float64": "xsd:float",
    "object": "xsd:string",
    "bool": "xsd:boolean",
    "datetime64": "xsd:date",
    "category": "xsd:string",
}


# tables = tabula.read_pdf(file, pages="all", multiple_tables=True)
# # # output just the first table in the PDF to a CSV
# print(tables)
# tables[0].to_csv("test_csv.csv", index=False)
pdf_file = open(file, 'rb').read()
with open(file, "rb") as f:
    pdf = pdftotext.PDF(f)
for page in pdf:
    print(page)
    s = re.sub(r'.*[\s]{2,}.*', '', page)
    print("\s" in s)
    print(s)

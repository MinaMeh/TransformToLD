def trait_csv(csv_file):
    file= pd.read_csv("test.csv",delimiter=",")
    headers= file.columns
    terms=dict()
    for col in columns:
        data= getVocab(col,"propery")
        terms[col]=data
    return terms

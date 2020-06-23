import pandas as pd
import lxml.html as lh
from bs4 import BeautifulSoup as bs

file = pd.read_html("media/test_ywVSrPg_0.html")
print(file[0].columns)

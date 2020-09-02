import lxml.html as lh
from bs4 import BeautifulSoup as bs
import pandas as pd
import textrazor
import tabula
import cv2
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import csv
import numpy as np
try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract
import pdftotext
import re
Datatypes = {
    "int64": "xsd:int",
    "float64": "xsd:float",
    "object": "xsd:string",
    "bool": "xsd:boolean",
    "datetime64": "xsd:date",
    "category": "xsd:string",
}


def extract_text_data(file):
    ''' Extracts the sentences of a text file '''
    results = dict()
    with open(file, "r") as f:
        content = f.read()
        results['paragraph'] = content
        results['sentences'] = get_sentences(content)
        return results


def extract_csv_data(csv_file, separator=";"):
    ''' Extracts Data of csv file
        Returns: headers, number of lines , number of columns
        stores the content in the database
    '''
    file = pd.read_csv(csv_file, delimiter=separator)
    cols = file.columns
    headers = []
    for col in cols:
        head = {}
        head['name'] = col
        head["type"] = Datatypes[str(file.dtypes[col])]
        head['selected'] = True
        headers.append(head)
    lines = file.shape[0]
    columns = file.shape[1]
    return {"headers": headers, 'columns': columns, "lines": lines}


def extract_html_data(file, extract_tables=False, extract_paragraphs=False):
    '''
    Extract HTML file data
    if tables==true, it extracts tables
    if paragraphs==true it extracts paragraphs
    '''
    file_content = open(file).read()
    soup = bs(file_content, 'lxml')
    tables = []
    num_tables = 0
    paragraph_results = []
    num_paragraphs = 0
    if (extract_tables):
        tables_html = soup.find_all("table")
        tables = get_tables_content(tables_html, file)
        num_tables = len(tables)
    if (extract_paragraphs):
        paragraphs = [par.text for par in soup.find_all("p")]
        paragraph_results = get_paragraphs_sentences(paragraphs)
        num_paragraphs = len(paragraph_results)
    results = {"tables": tables, "num_tables": num_tables,
               "paragraphs": paragraph_results, "num_paragraphs": num_paragraphs}
    return results


def extract_pdf_data(file, extract_tables=False, extract_paragraphs=False):
    '''
    Extract PDF file data
    if tables==true, it extracts tables
    if paragraphs==true it extracts paragraphs
    '''
    if (extract_tables):
        tables_pdf = get_pdf_table(file)
        num_tables = len(tables_pdf)
    if (extract_paragraphs):
        paragraphs = get_pdf_text(file)
        paragraph_results = get_paragraphs_sentences(paragraphs)
        num_paragraphs = len(paragraph_results)
    results = {"tables": tables_pdf, "num_tables": num_tables,
               "paragraphs": paragraph_results, "num_paragraphs": num_paragraphs}
    return results


def extract_image_data(file, extract_tables=False, extract_paragraphs=False):
    '''
    Extract image file data
    if tables==true, it extracts tables
    if paragraphs==true it extracts paragraphs
    '''
    img_data = get_image_tables(file)
    if (extract_tables):
        tables_pdf = img_data[0]
        num_tables = len(tables_pdf)
    if (extract_paragraphs):
        paragraphs = get_image_text(img_data[1])
        paragraph_results = get_paragraphs_sentences(paragraphs)
        num_paragraphs = len(paragraph_results)
    results = {"tables": tables_pdf, "num_tables": num_tables,
               "paragraphs": paragraph_results, "num_paragraphs": num_paragraphs}
    return results


def get_tables_content(tables, file):
    '''
    Extract data from HTML Tables
    Returns: headers, number of columns, number of lines
    Stores the content in a database
    '''
    tables_results = []

    for i in range(len(tables)):
        filename = "{}_{}.html".format(
            "".join(file.split(".")[:-1]), str(i), "html")
        with open(filename, "w") as f:
            f.write(str(tables[i]))
        # html_file = pd.read_html(filename)
        tables_content = dict()
        # data = lh.fromstring(str(tables[i]))
        # tr_elements = data.xpath('//tr')
        file_content = pd.read_html(filename)[0]
        headers = []
        tables_content["id"] = i
        tables_content["selected"] = True
        tables_content["filename"] = filename
        for header in file_content.columns:
            head = dict()
            name = header
            h_type = Datatypes[str(file_content.dtypes[header])]
            head = {"name": name, "selected": True, "type": h_type}
            headers.append(head)
        tables_content['headers'] = headers
        tables_content['columns'] = len(headers)
        tables_content["lines"] = file_content.shape[0]
        tables_results.append(tables_content)
    return tables_results


def get_paragraphs_sentences(paragraphs):
    '''
    Extracts the sentences of all paragraphs
    Returns the paragraph and its sentences
    '''
    paragraph_results = []
    i = 0
    for paragraph in paragraphs:
        result = dict()
        result['paragraph'] = paragraph
        result['id'] = i
        result['selected'] = True

        i += 1
        result['sentences'] = get_sentences(paragraph)
        paragraph_results.append(result)
    return paragraph_results


def get_sentences(paragraph, model="en_core_web_sm"):
    '''
    Extracts the sentences of a given paragraph
    '''
    sentences = []
    textrazor.api_key = "4599791ae63e2fb4f39d911a2145db56469b306ba8fbd6eda53e65ce"

    client = textrazor.TextRazor(extractors=['entities', 'relations'])
    response = client.analyze(paragraph)
    for sent in response.sentences():
        sentence = dict()
        sentence['text'] = concatenate(sent.words)
        sentences.append(sentence)
    return sentences


def concatenate(word_list):
    term = ""
    for word in word_list:
        term += " " + word.token
    return term


def get_pdf_table(file):
    tables = tabula.read_pdf(file, pages="all", multiple_tables=True)
    tables_results = []
    for i in range(len(tables)):
        filename = "{}_{}.csv".format(
            "".join(file.split(".")[:-1]), str(i), "csv")
        with open(filename, "w") as f:
            tables[i].to_csv(filename, index=False)
        tables_content = dict()
        file_content = pd.read_csv(filename)
        headers = []
        tables_content["id"] = i
        tables_content["selected"] = True
        tables_content["filename"] = filename
        for header in file_content.columns:
            head = dict()
            name = header
            h_type = Datatypes[str(file_content.dtypes[header])]
            head = {"name": name, "selected": True, "type": h_type}
            headers.append(head)
        tables_content['headers'] = headers
        tables_content['columns'] = len(headers)
        tables_content["lines"] = file_content.shape[0]
        tables_results.append(tables_content)
    return tables_results


def get_pdf_text(file):
    content = []
    pdf_file = open(file, 'rb').read()
    with open(file, "rb") as f:
        pdf = pdftotext.PDF(f)
    for page in pdf:
        s = re.sub(r'.*[\s]{2,}.*', '', page)
        content.append(s)
    return content


def get_image_tables(file):
    img = cv2.imread(file, 0)

    # thresholding the image to a binary image
    thresh, img_bin = cv2.threshold(
        img, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    # inverting the image
    img_bin = 255-img_bin
    cv2.imwrite('/Users/YOURPATH/cv_inverted.png', img_bin)
    # Plotting the image to see the output
    plotting = plt.imshow(img_bin, cmap='gray')
    # Length(width) of kernel as 100th of total width
    kernel_len = np.array(img).shape[1]//100
    # Defining a vertical kernel to detect all vertical lines of image
    ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
    # Defining a horizontal kernel to detect all horizontal lines of image
    hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
    # A kernel of 2x2
    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))

    # Use vertical kernel to detect and save the vertical lines in a jpg
    image_1 = cv2.erode(img_bin, ver_kernel, iterations=3)
    vertical_lines = cv2.dilate(image_1, ver_kernel, iterations=3)
    cv2.imwrite("/Users/YOURPATH/vertical.jpg", vertical_lines)
    # Plot the generated image
    plotting = plt.imshow(image_1, cmap='gray')

    # Use horizontal kernel to detect and save the horizontal lines in a jpg
    image_2 = cv2.erode(img_bin, hor_kernel, iterations=3)
    horizontal_lines = cv2.dilate(image_2, hor_kernel, iterations=3)
    cv2.imwrite("/Users/YOURPATH/horizontal.jpg", horizontal_lines)
    # Plot the generated image
    plotting = plt.imshow(image_2, cmap='gray')
    # Combine horizontal and vertical lines in a new third image, with both having same weight.
    img_vh = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
    # Eroding and thesholding the image
    img_vh = cv2.erode(~img_vh, kernel, iterations=2)
    thresh, img_vh = cv2.threshold(
        img_vh, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
    cv2.imwrite("/Users/YOURPATH/img_vh.jpg", img_vh)
    bitxor = cv2.bitwise_xor(img, img_vh)
    bitnot = cv2.bitwise_not(bitxor)
    # Plotting the generated image
    plotting = plt.imshow(bitnot, cmap='gray')
    # Detect contours for following box detection
    contours, hierarchy = cv2.findContours(
        img_vh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    def sort_contours(cnts, method="left-to-right"):
        # initialize the reverse flag and sort index
        reverse = False
        i = 0
        # handle if we need to sort in reverse
        if method == "right-to-left" or method == "bottom-to-top":
            reverse = True
        # handle if we are sorting against the y-coordinate rather than
        # the x-coordinate of the bounding box
        if method == "top-to-bottom" or method == "bottom-to-top":
            i = 1
            # construct the list of bounding boxes and sort them from top to
            # bottom
            boundingBoxes = [cv2.boundingRect(c) for c in cnts]
            (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                                                key=lambda b: b[1][i], reverse=reverse))
            # return the list of sorted contours and bounding boxes
        return (cnts, boundingBoxes)

    # Sort all the contours by top to bottom.
    contours, boundingBoxes = sort_contours(contours, method="top-to-bottom")
    # Creating a list of heights for all detected boxes
    heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
    # Get mean of heights
    mean = np.mean(heights)
    # Create list box to store all boxes in
    box = []
    # Get position (x,y), width and height for every contour and show the contour on image
    for c in contours:
        x, y, w, h = cv2.boundingRect(c)
        if (w < 1000 and h < 500):
            image = cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            box.append([x, y, w, h])
    plotting = plt.imshow(image, cmap='gray')
    # Creating two lists to define row and column in which cell is located
    row = []
    column = []
    j = 0
    # Sorting the boxes to their respective row and column
    for i in range(len(box)):
        if(i == 0):
            column.append(box[i])
            previous = box[i]
        else:
            if(box[i][1] <= previous[1]+mean/2):
                column.append(box[i])
                previous = box[i]
                if(i == len(box)-1):
                    row.append(column)
            else:
                row.append(column)
                column = []
                previous = box[i]
                column.append(box[i])

    # calculating maximum number of cells
    countcol = 0
    for i in range(len(row)):
        countcol = len(row[i])
        if countcol > countcol:
            countcol = countcol

    # Retrieving the center of each column
    center = [int(row[i][j][0]+row[i][j][2]/2)
              for j in range(len(row[i])) if row[0]]
    center = np.array(center)
    center.sort()

    # Regarding the distance to the columns center, the boxes are arranged in respective order
    finalboxes = []
    for i in range(len(row)):
        lis = []
        for k in range(countcol):
            lis.append([])
        for j in range(len(row[i])):
            diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
            minimum = min(diff)
            indexing = list(diff).index(minimum)
            lis[indexing].append(row[i][j])
        finalboxes.append(lis)

    # from every single image-based cell/box the strings are extracted via pytesseract and stored in a list
    outer = []
    for i in range(len(finalboxes)):
        for j in range(len(finalboxes[i])):
            inner = ''
            if (len(finalboxes[i][j]) == 0):
                outer.append(' ')
            else:
                for k in range(len(finalboxes[i][j])):
                    y, x, w, h = finalboxes[i][j][k][0], finalboxes[i][j][k][1], finalboxes[i][j][k][2], finalboxes[i][j][k][3]
                    finalimg = bitnot[x:x+h, y:y+w]
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                    border = cv2.copyMakeBorder(
                        finalimg, 2, 2, 2, 2,   cv2.BORDER_CONSTANT, value=[255, 255])
                    resizing = cv2.resize(border, None, fx=2,
                                          fy=2, interpolation=cv2.INTER_CUBIC)
                    dilation = cv2.dilate(resizing, kernel, iterations=1)
                    erosion = cv2.erode(dilation, kernel, iterations=1)

                    out = pytesseract.image_to_string(erosion)
                    if (len(out) == 0):
                        out = pytesseract.image_to_string(
                            erosion, config='--psm 3')

                    inner = (inner + " " + out).strip()
                outer.append(out.strip())
    # Creating a dataframe of the generated OCR list
    arr = np.array(outer)
    dataframe = pd.DataFrame(arr.reshape(len(row), countcol))
    data = dataframe.style.set_properties(align="left")
    filename = 'test.csv'
    dataframe.to_csv('test.csv', index=False, header=False)
    table = pd.read_csv("test.csv", index_col=None)
    tables_results = []
    tables_content = dict()
    file_content = pd.read_csv(filename)
    headers = []
    tables_content["id"] = 0
    tables_content["selected"] = True
    tables_content["filename"] = filename
    for header in file_content.columns:
        head = dict()
        name = header
        h_type = Datatypes[str(file_content.dtypes[header])]
        head = {"name": name, "selected": True, "type": h_type}
        headers.append(head)
    tables_content['headers'] = headers
    tables_content['columns'] = len(headers)
    tables_content["lines"] = file_content.shape[0]
    tables_results.append(tables_content)
    return tables_results, img


def get_image_text(img):
    return [pytesseract.image_to_string(img)]

import os
from csv import DictWriter
from django.conf import settings
from transformToLD.Automatic.autmatic_convert import auto_convert_csv, auto_convert_text, auto_convert_html


def test_csv(settings, DictWriter):
    path = settings.MEDIA_URL+"tests/"
    report_file = open(settings.MEDIA_URL+'report_test.csv', 'w')
    writer = DictWriter(report_file, fieldnames=[
                        "filename", 'size', "exec_time", 'nb_rows', 'nb_cols', 'extract', 'preprocess', 'map', 'convert', 'sum', 'nb_triplets'])
    writer.writeheader()
    for i, csv_file in enumerate(os.listdir(path)):
        record = {}
        file_path = os.path.join(path, csv_file)
        if (os.path.isfile(file_path)):
            size = os.path.getsize(file_path)
            record["filename"] = csv_file
            record['size'] = size
            print("file {}  size= {}".format(file_path, size))
            record = auto_convert_csv(file_path, str(i))
            record.update({
                'filename': csv_file,
                'size': size,
            })
            writer.writerow(record)
    report_file.close()


path = settings.MEDIA_URL+"tests/text/"
report_file = open(settings.MEDIA_URL+'report_test_text.csv', 'w')
writer = DictWriter(report_file, fieldnames=[
    "filename", 'nb_sentences', 'size', "exec_time", 'extract', 'preprocess', 'map', 'convert', 'nb_triplets'])
writer.writeheader()
for i, csv_file in enumerate(os.listdir(path)):
    record = {}
    file_path = os.path.join(path, csv_file)
    if (os.path.isfile(file_path)):
        size = os.path.getsize(file_path)
        record["filename"] = csv_file
        record['size'] = size
        print("file {}  size= {}".format(file_path, size))
        record = auto_convert_text(file_path, "text"+str(i))
        record.update({
            'filename': csv_file,
            'size': size,
        })
        print(record)
        writer.writerow(record)
report_file.close()


def test_html():
    path = settings.MEDIA_URL+"tests/html/"
    report_file = open(settings.MEDIA_URL+'report_test_html.csv', 'w')
    writer = DictWriter(report_file, fieldnames=[
        "filename", 'size', 'extract', 'nb_tables', 'nb_paragraphs'])
    writer.writeheader()
    for i, csv_file in enumerate(os.listdir(path)):
        record = {}
        file_path = os.path.join(path, csv_file)
        if (os.path.isfile(file_path)):
            size = os.path.getsize(file_path)
            record["filename"] = csv_file
            record['size'] = size
            print("file {}  size= {}".format(file_path, size))
            record = auto_convert_html(file_path, "html"+str(i))
            record.update({
                'filename': csv_file,
                'size': size,
            })
            print(record)
            writer.writerow(record)
    report_file.close()

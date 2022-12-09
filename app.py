import os
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage
from io import StringIO

from PyPDF2 import PdfFileReader
import fitz
import time

import pandas as pd


def save_file(path, content):
    with open(path, 'wb') as f:
        f.write(content)


def timeit(func):
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        diff = end - start
        print('Function: {0} run time: {1} seconds'.format(
            func.__name__, diff))
        return res
    return wrapper


@timeit
def PDF2TextCustom(path):
    # convert pdf to text
    rsrcmgr = PDFResourceManager()
    retstr = StringIO()
    codec = 'utf-8'
    laparams = LAParams()
    device = TextConverter(rsrcmgr, retstr, codec=codec, laparams=laparams)
    fp = open(path, 'rb')
    interpreter = PDFPageInterpreter(rsrcmgr, device)
    password = ""
    maxpages = 0
    caching = True
    pagenos = set()

    for page in PDFPage.get_pages(fp, pagenos, maxpages=maxpages, password=password, caching=caching, check_extractable=True):
        interpreter.process_page(page)

    text = retstr.getvalue()

    fp.close()
    device.close()
    retstr.close()
    return text


@timeit
def PDF2TextPyPDF2(path):
    # convert pdf to text with pypdf2
    with open(path, 'rb') as f:
        pdf = PdfFileReader(f)
        info = pdf.getDocumentInfo()
        number_of_pages = pdf.getNumPages()

        text = ''
        for i in range(number_of_pages):
            page = pdf.getPage(i)
            text += page.extractText()
    return text


@timeit
def PDF2TextPyMuPDF(path):
    text = ''
    with fitz.open(path) as doc:
        for page in doc:
            text += page.get_text()
    return text


def main():
    # load pdf file
    path = 'sample.pdf'
    # convert pdf to text
    text = PDF2TextCustom(path)
    # save text file
    save_file('custom.txt', text.encode('utf-8'))

    text1 = PDF2TextPyPDF2(path)
    save_file('pypdf2.txt', text1.encode('utf-8'))

    text2 = PDF2TextPyMuPDF(path)
    save_file('pymupdf.txt', text2.encode('utf-8'))

    
main()

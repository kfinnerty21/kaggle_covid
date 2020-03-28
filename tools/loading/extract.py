import re


def clean(txt):
    """
    Basic string loading code.

    :param txt:
    :return:
    """
    txt = re.sub(' +', ' ', txt)
    txt = re.sub(',', ' ', txt)
    txt = re.sub(r'\([^()]*\)', '', txt)
    txt = re.sub(r'https?:\S+\sdoi', '', txt)
    txt = re.sub(r'\n+', '.', txt)  # replace multiple newlines with period
    txt = re.sub(r'\[\d+\]', ' ', txt)  # remove reference numbers
    return txt.lower()


def pub_extract(data):
    """
    Extracting data from publications.

    :param data:
    :return:
    """
    abstract = ''
    for section in data['abstract']:
        abstract = abstract + '  ' + section['text']
    abstract = clean(abstract)

    text = ''
    for section in data['body_text']:
        text = text + '  ' + section['text']
    text = clean(text)
    ID = data['paper_id']
    title = data['metadata']['title']
    return ID, title, abstract, text

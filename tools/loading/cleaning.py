import re


def clean(txt):
    """
    Basic string loading code.

    :param txt:
    :return:
    """
    txt = re.sub(r'.\n+', '. ', txt)  # replace multiple newlines with period
    txt = re.sub(r'\n+', '', txt)  # replace multiple newlines with period
    txt = re.sub(r'\[\d+\]', ' ', txt)  # remove reference numbers
    txt = re.sub(' +', ' ', txt)
    txt = re.sub(',', ' ', txt)
    txt = re.sub(r'\([^()]*\)', '', txt)
    txt = re.sub(r'https?:\S+\sdoi', '', txt)
    txt = re.sub(r'biorxiv', '', txt)
    txt = re.sub(r'preprint', '', txt)
    txt = re.sub(r':', ' ', txt)
    return txt.lower()
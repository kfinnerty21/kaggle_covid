import unittest
import pytest
import json
from loading.document import document

@pytest.fixture()
def data_file(tmpdir_factory):
    data =  {'paper_id': '00000001',
            'metadata': {'title': 'Test Text'},
            'abstract': [{'text': "Abstract sentence 1 is high quality."},
                         {'text': "Abstract sentence 2 is of lesser quality."},
                         {'text': "Abstract sentence 3 is bad."}],
            'body_text': [{'text': "Body text sentence 1 gives an overview of the paper."},
                          {'text': "Body sentence 2 provide context for the research."},
                          {'text': "Best sentence 3 provides the results."}]
            }
    fn = tmpdir_factory.mktemp('data').join('pub.json')
    with open(fn, 'w') as json_file:
        json.dump(data, json_file)
    return fn




def test_pub_extract(data_file):
    pub = document(data_file)

    assert pub.paper_id == '00000001'
    assert pub.title == 'Test Text'
    assert pub.abstract == "\nAbstract sentence 1 is high quality.\nAbstract sentence 2 is of lesser quality.\nAbstract sentence 3 is bad."
    assert pub.text == "\nBody text sentence 1 gives an overview of the paper.\nBody sentence 2 provide context for the research.\nBest sentence 3 provides the results."



def test_pub_clean(data_file):
    pub = document(data_file)
    pub.clean_text()
    assert pub.paper_id == '00000001'
    assert pub.title == 'Test Text'
    assert pub.abstract == "\nabstract sentence 1 is high quality.\nabstract sentence 2 is of lesser quality.\nabstract sentence 3 is bad."
    assert pub.text == "\nbody text sentence 1 gives an overview of the paper.\nbody sentence 2 provide context for the research.\nbest sentence 3 provides the results."

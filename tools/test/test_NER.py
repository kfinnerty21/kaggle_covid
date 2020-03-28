import unittest
import pytest
import json
from NER.tripple_extract import entity_pairs, get_sent_list, get_entities_pairs


@pytest.fixture()
def ner_data():

    text_1_pair = "Tom has a brown cat named Tim."
    text_1_5_pair = "Tom has a borwn cat and a big dog."
    text_2_pair = "Tom has a brown cat, he also has a big dog."

    text_list = [text_1_pair, text_1_5_pair, text_2_pair]
    return "\n".join(text_list)


def test_ner_basic(ner_data):
    sents = get_sent_list(ner_data)
    pairs = list(map(get_entities_pairs, sents))
    print(ner_data)
    print(pairs)
    assert False
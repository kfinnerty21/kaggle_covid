import unittest
import pytest
import json
from NER.tripple_extract import get_entity_pairs


@pytest.fixture()
def ner_data():

    text_1_pair = """Tim has a too much iron in his red blood cells."""
    text_1_5_pair = """The subject contracted Covid-SARS"""
    text_2_pair = "the cell"

    text_list = [text_1_pair, text_1_5_pair, text_2_pair]
    return "\n".join(text_list)


def test_ner_basic(ner_data):
    pairs, ents = get_entity_pairs(ner_data)
    print(ner_data)
    print(ents)
    print(pairs)
    assert False
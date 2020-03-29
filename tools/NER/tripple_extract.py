import spacy
import pandas as pd
from loading.cleaning import clean

from scispacy.abbreviation import AbbreviationDetector

nlp = spacy.load("en_core_web_lg")

# Add the abbreviation pipe to the spacy pipeline.
abbreviation_pipe = AbbreviationDetector(nlp)
nlp.add_pipe(abbreviation_pipe)

SUBJECTS = ["nsubj", "nsubjpass", "csubj", "csubjpass", "agent", "expl"]
OBJECTS = ["dobj", "dative", "attr", "oprd"]


def filter_spans(spans):
    """Filter a sequence of spans and remove duplicates or overlaps. Useful for
    creating named entities (where one token can only be part of one entity) or
    when merging spans with `Retokenizer.merge`. When spans overlap, the (first)
    longest span is preferred over shorter spans.
    spans (iterable): The spans to filter.
    RETURNS (list): The filtered spans.
    """
    get_sort_key = lambda span: (span.end - span.start, span.start)
    sorted_spans = sorted(spans, key=get_sort_key, reverse=True)
    result = []
    seen_tokens = set()
    for span in sorted_spans:
        # Check for end - 1 here because boundaries are inclusive
        if span.start not in seen_tokens and span.end - 1 not in seen_tokens:
            result.append(span)
        seen_tokens.update(range(span.start, span.end))
    result = sorted(result, key=lambda span: span.start)
    return result


def refine_ent(ent, sent):
    """
    Filter any unwanted entity types

    :param ent: spacy entity object
    :param sent: spacy sentence object
    :return: entity, entity type
    """
    unwanted_tokens = (
        'PRON',  # pronouns
        'PART',  # particle
        'DET',  # determiner
        'SCONJ',  # subordinating conjunction
        'PUNCT',  # punctuation
        'SYM',  # symbol
        'X',  # other
    )
    ent_type = ent.ent_type_  # get entity type
    if ent_type == '':
        ent_type = 'NOUN_CHUNK'
        ent = ' '.join(str(t.text) for t in
                       nlp(str(ent)) if t.pos_
                       not in unwanted_tokens and t.is_stop == False)
    elif ent_type in ('ENTITY', 'NOMINAL', 'CARDINAL', 'ORDINAL') and str(ent).find(' ') == -1:
        t = ''
        for i in range(len(sent) - ent.i):
            if ent.nbor(i).pos_ not in ('VERB', 'PUNCT'):
                t += ' ' + str(ent.nbor(i))
            else:
                ent = t.strip()
                break
    return ent, ent_type


def get_sent_list(text):
    """
    Perform spacy processing and break document into sentences
    :param text: document text
    :return: list of sentences
    """
    text = clean(text)
    text = nlp(text)
    spans = list(text.ents) + list(text.noun_chunks)  # collect nodes
    spans = filter_spans(spans)
    with text.retokenize() as retokenizer:
        [retokenizer.merge(span) for span in spans]

    sentences = [sent for sent in text.sents]  # split text into sentences

    return sentences


def get_sent_entity_pairs(sent):
    """
    Extract entity pairs from sentences
    :param sent: spacy sentenace object
    :return: entity pair list of lists
    """
    ent_pairs = []
    dep = [token.dep_ for token in sent]
    try:
        if sum([dep.count(object) for object in OBJECTS]) == 1 \
                and sum([dep.count(object) for object in SUBJECTS]) == 1:
            for token in sent:
                if token.dep_ in ('obj', 'dobj'):  # identify object nodes
                    subject = [w for w in token.head.lefts if w.dep_
                               in ('subj', 'nsubj')]  # identify subject nodes
                    if subject:
                        subject = subject[0]
                        # identify relationship by root dependency
                        relation = [w for w in token.ancestors if w.dep_ == 'ROOT']
                        if relation:
                            relation = relation[0]
                            # add adposition or particle to relationship
                            if relation.nbor(1).pos_ in ('ADP', 'PART'):
                                relation = ' '.join((str(relation),
                                                     str(relation.nbor(1))))
                        else:
                            relation = 'unknown'
                        subject, subject_type = refine_ent(subject, sent)
                        token, object_type = refine_ent(token, sent)
                        ent_pairs.append([str(subject), str(relation), str(token),
                                          str(subject_type), str(object_type)])
    except:
        pass

    return ent_pairs


def entity_extract(sent):
    """
    Extract entity and entity type from sentence tokens
    :param sent: spacy sentence object
    :return: entity, entity type dictionary
    """
    ent_types = {}
    for token in sent:
        if token.ent_type_ is not '':
            ent_types[token.text] = token.ent_type_

    return ent_types


def get_entity_pairs(text):
    """
    process document and get entity paris and entities within the document.
    :param text: document
    :return: enitiy pairs datframe and dictionary of entities
    """
    sents = get_sent_list(text)
    pairs = list(map(get_sent_entity_pairs, sents))
    ents = list(map(entity_extract, sents))
    flatten_pairs = [item for pair in pairs for item in pair]
    pairs = pd.DataFrame(flatten_pairs, columns=['subject',
                                                 'relation', 'object', 'subject_type',
                                                 'object_type'])
    entities = {}
    for l in ents:
        entities.update(l)

    return pairs, entities

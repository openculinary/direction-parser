from collections import defaultdict

from hashedindex import HashedIndex, textparser
from stop_words import get_stop_words

stopwords = get_stop_words('en')


def build_search_index(docs):
    index = HashedIndex()
    for doc_id, doc in enumerate(docs):
        for ngrams in [1, 2]:
            for term in textparser.word_tokenize(doc, stopwords, ngrams):
                index.add_term_occurrence(term, doc_id)
    return index


def build_query_terms(docs):
    for doc in docs:
        for ngrams in [2, 1]:
            for term in textparser.word_tokenize(doc, stopwords, ngrams):
                yield term
                break


def execute_queries(index, queries):
    hits = defaultdict(set)
    for query_term in build_query_terms(queries):
        try:
            for doc_id in index.get_documents(query_term):
                hits[doc_id].add(' '.join(query_term))
        except IndexError:
            continue
    return hits


def load_queries(filename):
    with open(filename) as f:
        return f.readlines()

import pytest

from web.search import (
    build_search_index,
    execute_queries,
)


@pytest.fixture
def example_docs():
    return [
        'example content',
        'extra content',
        'unrelated item',
        'unrelated extra item content',
    ]


def test_exact_term_query(example_docs):
    index = build_search_index(example_docs)
    results = execute_queries(index, ['example'])
    assert len(results) == 1


def test_multiple_term_query(example_docs):
    index = build_search_index(example_docs)
    results = execute_queries(index, ['content'])
    assert len(results) == 3


def test_negative_term_query(example_docs):
    index = build_search_index(example_docs)
    results = execute_queries(index, ['nonexistent'])
    assert len(results) == 0


def test_positive_phrase_query(example_docs):
    doc_id = example_docs.index('extra content')
    index = build_search_index(example_docs)
    results = execute_queries(index, ['extra content'])
    assert len(results) == 1
    assert 'extra content' in results[doc_id]

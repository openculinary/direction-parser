from collections import defaultdict
from flask import Flask, abort, jsonify, request
from hashedixsearch import (
   build_search_index,
   execute_queries,
   tokenize,
)
from stop_words import get_stop_words as get_stopwords


def load_queries(filename):
    with open(filename) as f:
        return [line.strip().lower() for line in f.readlines()]


app = Flask(__name__)

stopwords = get_stopwords('en')

appliance_queries = load_queries('web/data/appliances.txt')
utensil_queries = load_queries('web/data/utensils.txt')
vessel_queries = load_queries('web/data/vessels.txt')


@app.route('/queries')
def queries():
    queries_by_type = {
        'appliances': appliance_queries,
        'utensils': utensil_queries,
        'vessels': vessel_queries,
    }
    query_type = request.args.get('type')
    queries = queries_by_type.get(query_type)
    if not queries:
        return abort(404)
    return jsonify(queries)


def equipment_by_document(index, queries):
    results_by_document = defaultdict(lambda: set())
    equipment_hits = execute_queries(index, queries)
    for equipment, hits in equipment_hits:
        for hit in hits:
            results_by_document[hit['doc_id']].add(equipment)
    return results_by_document


@app.route('/', methods=['POST'])
def root():
    descriptions = request.form.getlist('descriptions[]')

    index = build_search_index()
    for doc_id, doc in enumerate(descriptions):
        for ngrams in [1, 2]:
            for term in tokenize(doc, stopwords=stopwords, ngrams=ngrams):
                index.add_term_occurrence(term, doc_id)

    appliances_by_doc = equipment_by_document(index, appliance_queries)
    utensils_by_doc = equipment_by_document(index, utensil_queries)
    vessels_by_doc = equipment_by_document(index, vessel_queries)

    results = []
    for doc_id, description in enumerate(descriptions):
        results.append({
            'index': doc_id,
            'description': description,
            'appliances': list(appliances_by_doc[doc_id]),
            'utensils': list(utensils_by_doc[doc_id]),
            'vessels': list(vessels_by_doc[doc_id]),
        })
    return jsonify(results)

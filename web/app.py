from collections import defaultdict
from flask import Flask, jsonify, request
from hashedixsearch import (
   build_search_index,
   execute_queries,
   highlight,
   tokenize,
   NullStemmer,
)
from snowballstemmer import stemmer
from stop_words import get_stop_words as get_stopwords


def load_queries(filename):
    with open(filename) as f:
        return [line.strip().lower() for line in f.readlines()]


class EquipmentStemmer(NullStemmer):

    stemmer_en = stemmer('english')

    def stem(self, x):
        return self.stemmer_en.stemWord(x)


app = Flask(__name__)

stopwords = get_stopwords('en')

appliance_queries = load_queries('web/data/appliances.txt')
utensil_queries = load_queries('web/data/utensils.txt')
vessel_queries = load_queries('web/data/vessels.txt')


def equipment_by_document(index, queries):
    results_by_document = defaultdict(lambda: set())
    stemmer = EquipmentStemmer()
    equipment_hits = execute_queries(
        index=index,
        queries=queries,
        stemmer=stemmer,
        stopwords=stopwords
    )
    for equipment, hits in equipment_hits:
        for hit in hits:
            results_by_document[hit['doc_id']].add(equipment)
    return results_by_document


@app.route('/', methods=['POST'])
def root():
    descriptions = request.form.getlist('descriptions[]')

    stemmer = EquipmentStemmer()
    index = build_search_index()
    for doc_id, doc in enumerate(descriptions):
        for ngrams in [1, 2]:
            for term in tokenize(doc,
                                 stopwords=stopwords,
                                 ngrams=ngrams,
                                 stemmer=stemmer):
                index.add_term_occurrence(term, doc_id)

    appliances_by_doc = equipment_by_document(index, appliance_queries)
    utensils_by_doc = equipment_by_document(index, utensil_queries)
    vessels_by_doc = equipment_by_document(index, vessel_queries)

    markup_by_doc = {}
    for doc_id, description in enumerate(descriptions):
        equipment = (
            appliances_by_doc[doc_id]
            | utensils_by_doc[doc_id]
            | vessels_by_doc[doc_id]
        )
        terms = []
        for equipment in equipment:
            terms.append(next(tokenize(equipment, stemmer=stemmer)))
        markup_by_doc[doc_id] = highlight(
            query=description,
            terms=terms,
            stemmer=stemmer,
            case_sensitive=False
        )

    results = []
    for doc_id, description in enumerate(descriptions):
        results.append({
            'index': doc_id,
            'description': description,
            'markup': markup_by_doc.get(doc_id),
            'appliances': [
                {'appliance': appliance}
                for appliance in appliances_by_doc[doc_id]
            ],
            'utensils': [
                {'utensil': utensil}
                for utensil in utensils_by_doc[doc_id]
            ],
            'vessels': [
                {'vessel': vessel}
                for vessel in vessels_by_doc[doc_id]
            ],
        })
    return jsonify(results)

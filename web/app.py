from flask import Flask, jsonify, request

from web.search import (
   build_search_index,
   execute_queries,
   load_queries,
)


app = Flask(__name__)

appliance_queries = load_queries('web/data/appliances.txt')
utensil_queries = load_queries('web/data/utensils.txt')


@app.route('/', methods=['POST'])
def root():
    descriptions = request.form.getlist('descriptions[]')

    index = build_search_index(descriptions)
    appliance_hits = execute_queries(index, appliance_queries)
    utensil_hits = execute_queries(index, utensil_queries)

    results = []
    for doc_id, description in enumerate(descriptions):
        results.append({
            'index': doc_id,
            'description': description,
            'appliances': list(appliance_hits[doc_id]),
            'utensils': list(utensil_hits[doc_id]),
        })
    return jsonify(results)

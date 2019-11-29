from flask import Flask, abort, jsonify, request

from web.search import (
   build_search_index,
   execute_queries,
   load_queries,
)


app = Flask(__name__)

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


@app.route('/', methods=['POST'])
def root():
    descriptions = request.form.getlist('descriptions[]')

    index = build_search_index(descriptions)
    appliance_hits = execute_queries(index, appliance_queries)
    utensil_hits = execute_queries(index, utensil_queries)
    vessel_hits = execute_queries(index, vessel_queries)

    results = []
    for doc_id, description in enumerate(descriptions):
        results.append({
            'index': doc_id,
            'description': description,
            'appliances': [
                {'appliance': appliance}
                for appliance in appliance_hits[doc_id]
            ],
            'utensils': [
                {'utensil': utensil}
                for utensil in utensil_hits[doc_id]
            ],
            'vessels': [
                {'vessel': vessel}
                for vessel in vessel_hits[doc_id]
            ],
        })
    return jsonify(results)

from flask import current_app
from app import app


def add_to_index(index, model):
    if not current_app.elasticsearch:
        return
    payload = {}
    for field in model.__searchable__:
        payload[field] = getattr(model, field)
    current_app.elasticsearch.index(index=index, doc_type=index, id=model.id,
                                    body=payload)

def remove_from_index(index, model):
    if not current_app.elasticsearch:
        return
    current_app.elasticsearch.delete(index=index, doc_type=index, id=model.id)


def query_index(index, query, page, per_page, fields):
    if not current_app.elasticsearch:
        return [], 0
    body = {'query': {'multi_match': {'query': query, 'fields': fields}},
              'from': (page - 1) * per_page, 'size': per_page}
    app.logger.info("Elastic Search Query: \n{}".format(body))
    search = current_app.elasticsearch.search(index=index, body=body)
    app.logger.info("Elastic Search Response: \n{}".format(search))
    ids = [hit['_id'] for hit in search['hits']['hits']]
    return ids, search['hits']['total']

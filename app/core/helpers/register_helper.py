from app import app


def register_api(view, endpoint, url, pk='_id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(
        url, defaults={pk: None},
        view_func=view_func, methods=['GET', ]
    )
    app.add_url_rule(url, view_func=view_func, methods=['POST', ])
    app.add_url_rule(
        '{}/<{}:{}>'.format(url, pk_type, pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )


def register_basic_api(view, endpoint, url, methods=None):
    if methods is None:
        methods = ['GET', ]
    view_func = view.as_view(endpoint)
    app.add_url_rule(
        '{}'.format(url), view_func=view_func, methods=methods
    )


def register_complex_api(
        view, endpoint, url_path_one, url_path_two,
        pk='_id', pk_type='int'):
    view_func = view.as_view(endpoint)
    app.add_url_rule(
        '{}/<{}:{}>{}'.format(url_path_one, pk_type, pk, url_path_two),
        view_func=view_func, methods=['GET', ]
    )
    app.add_url_rule(
        '{}/<{}:{}>{}'.format(url_path_one, pk_type, pk, url_path_two),
        view_func=view_func, methods=['POST', ]
    )
    app.add_url_rule(
        '{}/<{}:{}>{}'.format(url_path_one, pk_type, pk, url_path_two),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )

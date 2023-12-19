def register_api(blue_print, view, endpoint, url, pk='_id', pk_type='string'):
    view_func = view.as_view(endpoint)
    blue_print.add_url_rule(
        url, defaults={pk: None},
        view_func=view_func, methods=['GET', ]
    )
    blue_print.add_url_rule(url, view_func=view_func, methods=['POST', ])
    blue_print.add_url_rule(
        '{}/<{}:{}>'.format(url, pk_type, pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )


def register_basic_api(blue_print, view, endpoint, url, methods=None):
    if methods is None:
        methods = ['GET', ]
    view_func = view.as_view(endpoint)
    blue_print.add_url_rule(
        '{}'.format(url), view_func=view_func, methods=methods
    )


def register_complex_api(
        blue_print, view, endpoint, url_path_one, url_path_two,
        pk='_id', pk_type='int'):
    view_func = view.as_view(endpoint)
    blue_print.add_url_rule(
        '{}/<{}:{}>{}'.format(url_path_one, pk_type, pk, url_path_two),
        view_func=view_func, methods=['GET', ]
    )
    blue_print.add_url_rule(
        '{}/<{}:{}>{}'.format(url_path_one, pk_type, pk, url_path_two),
        view_func=view_func, methods=['POST', ]
    )
    blue_print.add_url_rule(
        '{}/<{}:{}>{}'.format(url_path_one, pk_type, pk, url_path_two),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )


def register_multiple_id_api(
        blue_print, view, endpoint, url_path_one,
        url_path_two, id_one, id_one_type, id_two, id_two_type):
    view_func = view.as_view(endpoint)
    blue_print.add_url_rule(
        '{}/<{}:{}>{}/<{}:{}>'.format(
            url_path_one, id_one_type, id_one,
            url_path_two, id_two_type, id_two),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )

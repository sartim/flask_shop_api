from app.core.constants import ApiVersion


def register_api(
        blue_print,
        view, endpoint, url, pk='_id', pk_type='int', version=ApiVersion.V1):
    view_func = view.as_view(endpoint)
    blue_print.add_url_rule(
        "/api/{}{}".format(version, url), defaults={pk: None},
        view_func=view_func, methods=['GET', ]
    )
    blue_print.add_url_rule(
        "/api/{}{}".format(version, url), view_func=view_func,
        methods=['POST', ])
    blue_print.add_url_rule(
        '/api/{}{}/<{}:{}>'.format(version, url, pk_type, pk),
        view_func=view_func,
        methods=['GET', 'PUT', 'DELETE']
    )


def register_basic_api(
        blue_print,
        view, endpoint, url, methods=None, version=ApiVersion.V1):
    if methods is None:
        methods = ['GET', ]
    view_func = view.as_view(endpoint)
    blue_print.add_url_rule(
        '/api/{}{}'.format(version, url), view_func=view_func, methods=methods
    )


def register_complex_api(
        blue_print: object,
        view: object, endpoint: object, url_path_one: object, url_path_two: object,
        pk: object = '_id', pk_type: object = 'int', version: object = ApiVersion.V1) -> object:
    view_func = view.as_view(endpoint)
    blue_print.add_url_rule(
        '/api/{}{}/<{}:{}>{}'.format(
            version, url_path_one, pk_type, pk, url_path_two),
        view_func=view_func, methods=['GET', 'PUT', 'DELETE']
    )

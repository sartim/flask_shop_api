from app import app


def clean_methods(methods):
    if 'HEAD' in methods:
        methods.remove('HEAD')
    if 'OPTIONS' in methods:
        methods.remove('OPTIONS')
    return methods


def generate_permissions_from_routes(methods, endpoint, path):
    perm = dict(path=path)
    if 'GET' in methods and len(methods) == 1:
        perm.update(
            permissions=[
                {
                    "name": "CAN_VIEW_{}".format(
                        endpoint.upper()),
                    "description": "Can view {} record".format(
                        endpoint)
                }
            ]
        )
    if 'POST' in methods and len(methods) == 1:
        perm.update(
            permissions=[
                {
                    "name": "CAN_ACCESS_CREATE_{}".format(
                        endpoint.upper()),
                    "description": "Can access create {}".format(endpoint)
                },
                {
                    "name": "CAN_CREATE_{}".format(
                        endpoint.upper()),
                    "description": "Can create {} record".format(endpoint)
                }
            ]
        )
    if 'GET' in methods and 'PUT' in methods and 'DELETE' in methods:
        permission = [
            {
                "name": "CAN_VIEW_BELONGING_{}".format(endpoint.upper()),
                "description": "Can view only belonging {} records".format(endpoint)
            },
            {
                "name": "CAN_VIEW_ALL_{}".format(endpoint.upper()),
                "description": "Can view all {} records".format(endpoint)
            },
            {
                "name": "CAN_VIEW_{}_BY_ID".format(endpoint.upper()),
                "description": "Can view {} record by id".format(endpoint)
            },
            {
                "name": "CAN_ACCESS_VIEW_{}".format(endpoint.upper()),
                "description": "Can access view".format(endpoint)
            },
            {
                "name": "CAN_UPDATE_CREATE_{}".format(
                    endpoint.upper()),
                "description": "Can update {} record".format(endpoint)
            },
            {
                "name": "CAN_UPDATE_CREATE_ANY_{}".format(
                    endpoint.upper()),
                "description": "Can update any {} record".format(endpoint)
            },
            {
                "name": "CAN_UPDATE_CREATE_BELONGING_{}".format(
                    endpoint.upper()),
                "description": "Can update belonging {} record".format(endpoint)
            },
            {
                "name": "CAN_ACCESS_UPDATE_CREATE_{}".format(
                    endpoint.upper()),
                "description": "Can access update".format(endpoint)
            },
            {
                "name": "CAN_DELETE_{}".format(endpoint.upper()),
                "description": "Can delete {} record".format(
                    endpoint)
            },
            {
                "name": "CAN_ACCESS_DELETE_{}".format(
                    endpoint.upper()),
                "description": "Can access delete".format(
                    endpoint)
            }
        ]
        perm.update(permissions=permission)
    return perm


def get_permissions_from_routes():
    data = []
    for rule in app.url_map.iter_rules():
        blacklist = [
            'static', 'generate_jwt_api', 'refresh_jwt_api',
            'password_reset_api', 'password_reset_auth_api',
            'password_reset_token_api', 'send_password_reset_notification_api',
            'wallet_auth_api', 'validate_auth_api']
        if rule.endpoint not in blacklist:
            methods = clean_methods(list(rule.methods))
            endpoint = rule.endpoint[:-4]
            perm = generate_permissions_from_routes(methods, endpoint, rule.rule)
            data.append(perm)
    return data

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
                    "name": "CAN_GET_{}".format(
                        endpoint.upper()),
                    "description": "Can get {} record".format(
                        endpoint)
                }
            ]
        )
    if 'POST' in methods and len(methods) == 1:
        perm.update(
            permissions=[
                {
                    "name": "CAN_POST_{}".format(
                        endpoint.upper()),
                    "description": "Can post {} record".format(endpoint)
                }
            ]
        )
    if 'GET' in methods and 'PUT' in methods and 'DELETE' in methods:
        permission = [
            {
                "name": "CAN_GET_{}".format(endpoint.upper()),
                "description": "Can get {} record".format(endpoint)
            },
            {
                "name": "CAN_PUT_{}".format(
                    endpoint.upper()),
                "description": "Can put {} record".format(endpoint)
            },
            {
                "name": "CAN_DELETE_{}".format(endpoint.upper()),
                "description": "Can delete {} record".format(
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

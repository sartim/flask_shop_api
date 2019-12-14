import json
import bcrypt
import pycountry


def generate_password_hash(password, rounds=14, prefix=b'2b'):
    """
    Generate password hash with bcrypt having default prefix being 2b if not parsed. Also default
    log rounds is 14.
    :param password:
    :param rounds:
    :param prefix:
    :return:
    """
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt(rounds=rounds, prefix=prefix)).decode('utf-8')


def check_password_hash(hashed, password):
    """
    To check for password against hash
    :param password:
    :param hashed:
    :return:
    """
    if bcrypt.checkpw(password.encode(), hashed.encode()):
        return True
    return False


def list_countries():
    """
    Returns a list of countries
    :return countries:
    """
    return [{"country_id": country.numeric, 'country': country.name} for country in list(pycountry.countries)]


def open_file(file_path, type_='json'):
    """Reads file given"""
    with open(file_path) as f:
        if type_ == 'xml':
            data = f.read()
        else:
            data = json.load(f)
    return data

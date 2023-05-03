import json
import secrets
import pycountry

RESULT_LEN = 6
DIGITS = "0123456789"


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


def generate_random_value(size: int = RESULT_LEN, digits: str = DIGITS) -> int:
    """Generate random values based on the size and the digits preferred"""
    random_int = int("".join(secrets.choice(digits) for i in range(size)))
    return random_int


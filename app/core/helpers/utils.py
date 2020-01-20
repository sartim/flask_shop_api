import json
import pycountry


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

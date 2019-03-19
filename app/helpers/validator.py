import re


def password_validator(password):
    """
    Validate passwords
    At least 1 letter between [a-z] and 1 letter between [A-Z].
    At least 1 number between [0-9].
    At least 1 character from [$#@].
    Minimum length 6 characters.
    Maximum length 16 characters.
    :return:
    """
    x = True
    while x:
        if len(password) < 6 or len(password) > 12:
            break
        elif not re.search("[a-z]", password):
            break
        elif not re.search("[0-9]", password):
            break
        elif not re.search("[A-Z]", password):
            break
        elif not re.search("[$#@]", password):
            break
        elif re.search("\s", password):
            break
        else:
            x = False
            break

    return x


def email_validator(email):
    return bool(re.search(r"^[\w\.\+\-]+\@[\w]+\.[a-z]{2,3}$", email))


def field_validator(keys, data_):
    """
    Validates the submitted data are POSTed with the required fields
    :param keys:
    :param data_:
    :return:
    """
    data = {}
    for v in keys:
        if v not in data_:
            data[v] = ["This field may not be null."]
    if len(data) != 0:
        return {"success": False, "data": data}
    elif len(data) == 0:
        return {"success": True, "data": data}

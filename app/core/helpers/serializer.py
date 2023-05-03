import pickle


def serialize(obj):
    """
    Return serialized object
    :param obj:
    :return:
    """
    return pickle.dumps(obj)


def deserialize(serialized_obj):
    """
    Return deserialized object
    :param serialized_obj:
    :return:
    """
    return pickle.loads(serialized_obj)

def remove_none_values(dictionary: dict):
    return {key: value for key, value in dictionary.items() if value not in [None, []]}

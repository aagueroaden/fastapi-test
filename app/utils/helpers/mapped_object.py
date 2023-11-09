def mappedObject(dict_base: dict, data):
    new_data = {}
    for key in data:
        if key in dict_base:
            new_data[dict_base[key]] = data[key]
        else:
            continue
    return new_data

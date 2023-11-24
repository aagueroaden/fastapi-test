def sliceFullName(fullName):
    pass


def addLabelAndId(pickListValues: dict):
    if "value" not in pickListValues or 'label' not in pickListValues:
        return {
            'error': 'could not retrieve value and label'
        }
    else:
        return {
            'id': pickListValues["value"],
            'label': pickListValues["label"],
        }


def getNameAndFields(name: str, item: dict, names_formatted: dict):
    fieldName = names_formatted[name]
    fieldValue = list(map(addLabelAndId, item['picklistValues']))
    return fieldName, fieldValue

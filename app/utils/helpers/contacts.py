def sliceFullName(fullName: str) -> list[str]:
    """example:
    fullName = "Jhon Smith"     -> firstName="Jhon" , lastName="Smith"
    fullName = "Jhon Doe Smith" -> firstName="Jhon" , lastName="Doe Smith"
    fullName = "Jhon"           -> firstName="Jhon" , lastName=""
    fullName = ""               -> firstName=""     , lastName=""
    """
    fullNameArray: list = fullName.split(' ')
    firstName: str = fullNameArray[0]
    lastName: str = ' '.join(fullNameArray[1:])
    return [firstName, lastName]


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

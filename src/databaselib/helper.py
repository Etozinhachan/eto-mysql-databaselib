def getFirstDictionaryRow(dictionary:dict) -> tuple:
    
    return getDictionaryRow(dictionary, 1)

def getDictionaryRow(dictionary:dict, row:int) -> tuple:
    
    index = row-1
    return (list(dictionary.keys())[index], list(dictionary.values())[index])
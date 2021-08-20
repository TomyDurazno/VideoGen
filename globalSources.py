import sys

def isGlobalLog():
    return "log" in sys.argv
    
def nameFromArgs():
    auxName = [x for x, x in enumerate(sys.argv) if 'file=' in x]

    if len(auxName) > 0:
        return auxName.pop().replace("file=", "")
    else:
        return None
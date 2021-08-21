import sys


def getKeyPair(key):
    auxName = [x for x, x in enumerate(sys.argv) if f'{key}=' in x]
    return auxName.pop().replace(f'{key}=', "") if len(auxName) > 0 else None


def fromArgs(s):
    return getKeyPair(s)


def singleArg(s):
    return s in sys.argv


class Config:

    LOG = singleArg("log") or fromArgs("log") == "verbose"
    FULLMODE = fromArgs("mode") == "full"
    UNIQUE_NAMES = FULLMODE
    NAME = fromArgs("file")

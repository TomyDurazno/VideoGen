import sys


def getKeyPair(key):
    auxName = [x for x, x in enumerate(sys.argv) if f'{key}=' in x]
    return auxName.pop().replace(f'{key}=', "") if len(auxName) > 0 else None


def fromArgs(s):
    return getKeyPair(s)


def singleArg(s):
    return s in sys.argv


class GlobalConfig:
    LOG = singleArg("log".lower())
    MODE = fromArgs("mode".lower())
    FULLMODE = MODE == "full".lower()
    PARSER_ONLY_MODE = MODE == "parser".lower()
    TOKEN_ONLY_MODE = MODE == "token".lower()
    UNIQUE_NAMES = FULLMODE
    NAME = fromArgs("file".lower())

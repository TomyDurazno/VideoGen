import sys


def getKeyPair(key):
    auxName = [x for x, x in enumerate(sys.argv) if f'{key}=' in x]
    return auxName.pop().replace(f'{key}=', "") if len(auxName) > 0 else None


def fromArgs(s):
    return getKeyPair(s)


def singleArg(s):
    return s in sys.argv


class GlobalConfig:
    LOG = singleArg("log") or fromArgs("log")
    SENTENCE = fromArgs("log") == "sentence"
    MODE = fromArgs("mode")
    FULLMODE = MODE == "full"
    PARSER_ONLY_MODE = MODE == "parser"
    TOKEN_ONLY_MODE = MODE == "token"
    UNIQUE_NAMES = FULLMODE
    NAME = fromArgs("file")

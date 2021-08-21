from globalSources import Config

log = Config.LOG


class Token_Symbol:
    Start = "Start"
    SingleTagOpener = "SingleTagOpener"
    TagOpener = "TagOpener"
    TagOpenerWithSlash = "TagOpenerWithSlash"
    TagCloser = "TagCloser"
    SingleStringArg = "SingleStringArg"
    StartStringArg = "StartStringArg"
    StartStringArgWithCloser = "StartStringArgWithCloser"
    EndStringArg = "EndStringArg"
    Word = "Word"


def isTagOpener(s):
    return s[0] == '<'


def isTagOpenerWithSlash(s):
    return isTagOpener(s) and s[1] == '/'


def isTagCloser(s):
    return s[-1] == '>'


def isQuoteOpener(s):
    return s[0] == '"'


def isQuoteCloser(s):
    return s[-1] == '"'


def GetToken(s):
    if isTagOpenerWithSlash(s):
        return (Token_Symbol.TagOpenerWithSlash, s[2:-1])
    if isTagOpener(s) and isTagCloser(s):
        return (Token_Symbol.SingleTagOpener, s[1:-1])
    if isTagOpener(s):
        return (Token_Symbol.TagOpener, s[1:])
    if isTagCloser(s):
        return (Token_Symbol.TagCloser, s[:-1].replace('"', ''))
    if isQuoteOpener(s):
        if isQuoteCloser(s):
            return (Token_Symbol.SingleStringArg, s.replace('"', ''))
        else:
            # acumulative case
            aux = s.replace('"', '').replace('>', '')
            return (Token_Symbol.StartStringArg, aux)
    if isQuoteCloser(s):
        return (Token_Symbol.EndStringArg, s.replace('"', ''))
    return (Token_Symbol.Word, s.replace('"', ''))


def tokenize(lines):

    # Words acumulator
    words = []
    # Temp object used to build tags
    obj = {}
    tempargs = []
    isTagBuilding = False

    # The return type is an array with all the symbols
    ret = []

    # Join all acumulated words into a sentence
    def joinSentence():
        if len(words) > 0:
            wx = {
                "sentence": " ".join(words)
            }
            ret.append(wx)
            words.clear()

    # set temp object args
    def setArgs():
        args = obj.get("args") or []
        args.append(value)
        obj["args"] = args

    for l in lines:
        for w in l.split():
            (tokenType, value) = GetToken(w)

            if log:
                print((tokenType, value))

            if tokenType == Token_Symbol.SingleTagOpener:
                obj = {"tag": value}
                ret.append(obj)

            if tokenType == Token_Symbol.TagOpener:
                joinSentence()
                obj = {"tag": value}

            # Implicit tag building
            if tokenType == Token_Symbol.SingleStringArg:
                setArgs()

            if tokenType == Token_Symbol.TagCloser:
                setArgs()
                ret.append(obj)
                obj = {}
                isTagBuilding = False

            if tokenType == Token_Symbol.Word:
                # Words can appear in sentences or used as tag string literal argument
                if isTagBuilding:
                    tempargs.append(value)
                else:
                    words.append(value)

            if tokenType == Token_Symbol.StartStringArg:
                tempargs.append(value)
                isTagBuilding = True

            if tokenType == Token_Symbol.EndStringArg:
                args = obj.get("args") or []
                tempargs.append(value)
                args.append(" ".join(tempargs))
                obj["args"] = args
                tempargs = []

            if tokenType == Token_Symbol.TagOpenerWithSlash:
                joinSentence()
                obj = {
                    "tag": value,
                    "type": "close"
                }
                ret.append(obj)

    return ret

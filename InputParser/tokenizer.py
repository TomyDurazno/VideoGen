import re
from globalSources import GlobalConfig

log = GlobalConfig.LOG


class Token_Symbols:
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


class Token_Values:
    Open = '<'
    Close = '>'
    Slash = '/'
    Quote = '"'
    Separator = " "
    Empty = ''


class Token_Keys:
    Sentence = "sentence"
    Args = "args"
    Tag = "tag"
    Type = "type"


class Token_Types:
    Close = "close"


def isTagOpener(s):
    return s[0] == Token_Values.Open


def isTagOpenerWithSlash(s):
    return isTagOpener(s) and s[1] == Token_Values.Slash


def isTagCloser(s):
    return s[-1] == Token_Values.Close


def isQuoteOpener(s):
    return s[0] == Token_Values.Quote


def isQuoteCloser(s):
    return s[-1] == Token_Values.Quote


def invalidTagPosition(s):
    open = [m.start() for m in re.finditer(Token_Values.Open, s)]

    if len(open) > 1 or (len(open) and open[0] != 0):
        raise ValueError(
            f'Wrong position: {open[0]} for tag {Token_Values.Open} at: {s}')

    close = [m.start() for m in re.finditer(Token_Values.Close, s)]

    if len(close) > 1 or (len(close) and close[0] != len(s) - 1):
        raise ValueError(
            f'Wrong position: {close[0]} for tag {Token_Values.Close} at: {s}')

    return False


def GetToken(s):
    if isTagOpenerWithSlash(s):
        return (Token_Symbols.TagOpenerWithSlash, s[2:-1])
    if isTagOpener(s) and isTagCloser(s):
        return (Token_Symbols.SingleTagOpener, s[1:-1])
    if isTagOpener(s):
        return (Token_Symbols.TagOpener, s[1:])
    if isTagCloser(s):
        return (Token_Symbols.TagCloser, s[:-1].replace(Token_Values.Quote, Token_Values.Empty))
    if isQuoteOpener(s):
        if isQuoteCloser(s):
            return (Token_Symbols.SingleStringArg, s.replace(Token_Values.Quote, Token_Values.Empty))
        else:
            # acumulative case
            aux = s.replace(Token_Values.Quote, Token_Values.Empty).replace(
                Token_Values.Close, Token_Values.Empty)
            return (Token_Symbols.StartStringArg, aux)
    if isQuoteCloser(s):
        return (Token_Symbols.EndStringArg, s.replace(Token_Values.Quote, Token_Values.Empty))
    if not invalidTagPosition(s):
        return (Token_Symbols.Word, s.replace(Token_Values.Quote, Token_Values.Empty))


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
                Token_Keys.Sentence: Token_Values.Separator.join(words)
            }
            ret.append(wx)
            words.clear()

    # set temp object args
    def setArgs():
        args = obj.get(Token_Keys.Args) or []
        args.append(value)
        obj[Token_Keys.Args] = args

    for l in lines:
        for w in l.split():
            (tokenType, value) = GetToken(w)

            if log:
                print((tokenType, value))

            if tokenType == Token_Symbols.SingleTagOpener:
                obj = {Token_Keys.Tag: value}
                ret.append(obj)

            if tokenType == Token_Symbols.TagOpener:
                joinSentence()
                obj = {Token_Keys.Tag: value}

            # Implicit tag building
            if tokenType == Token_Symbols.SingleStringArg:
                setArgs()

            if tokenType == Token_Symbols.TagCloser:
                setArgs()
                ret.append(obj)
                obj = {}
                isTagBuilding = False

            if tokenType == Token_Symbols.Word:
                # Words can appear in sentences or used as tag string literal argument
                if isTagBuilding:
                    tempargs.append(value)
                else:
                    words.append(value)

            if tokenType == Token_Symbols.StartStringArg:
                tempargs.append(value)
                isTagBuilding = True

            if tokenType == Token_Symbols.EndStringArg:
                args = obj.get(Token_Keys.Args) or []
                tempargs.append(value)
                args.append(Token_Values.Separator.join(tempargs))
                obj[Token_Keys.Args] = args
                tempargs = []

            if tokenType == Token_Symbols.TagOpenerWithSlash:
                joinSentence()
                obj = {
                    Token_Keys.Tag: value,
                    Token_Keys.Type: Token_Types.Close
                }
                ret.append(obj)

    return ret

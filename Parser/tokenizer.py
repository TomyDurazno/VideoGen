import re
from globalSources import GlobalConfig

log = GlobalConfig.LOG


class Token_Symbols:
    Start = "Start"
    SingleTagOpenerAndCloser = "SingleTagOpenerAndCloser"
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
    return s[0] is Token_Values.Open


def isTagOpenerWithSlash(s):
    return isTagOpener(s) and s[1] is Token_Values.Slash


def isTagCloser(s):
    return s[-1] is Token_Values.Close


def isQuoteOpener(s):
    return s[0] is Token_Values.Quote


def isQuoteCloser(s):
    return s[-1] is Token_Values.Quote


def invalidTagPosition(s, i):
    open = [m.start() for m in re.finditer(Token_Values.Open, s)]

    if len(open) > 1 or (len(open) and open[0] != 0):
        raise ValueError(
            f'Wrong position ({open[0]}) for tag {Token_Values.Open} at line {i}: {s}')

    close = [m.start() for m in re.finditer(Token_Values.Close, s)]

    if len(close) > 1 or (len(close) and close[0] != len(s) - 1):
        raise ValueError(
            f'Wrong position ({close[0]}) for tag {Token_Values.Close} at line {i}: {s}')

    return False


def GetToken(s, i):

    # raises ValueError
    invalidTagPosition(s, i)

    if isTagOpenerWithSlash(s):
        return (Token_Symbols.TagOpenerWithSlash, s[2:-1])
    if isTagOpener(s) and isTagCloser(s):
        return (Token_Symbols.SingleTagOpenerAndCloser, s[1:-1])
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
    return (Token_Symbols.Word, s.replace(Token_Values.Quote, Token_Values.Empty))


def tokenize(lines):

    # Words acumulator
    words = []
    # Temp object used to build tags
    obj = {}
    tempargs = []
    stringLiteralAcum = []
    # Flags
    isTagBuilding = False
    isStringLiteralBuilding = False

    # The return type is an array with all the symbols
    ret = []

    # Join all acumulated words into a sentence
    def joinSentence():
        if len(words):
            ret.append({
                Token_Keys.Sentence: Token_Values.Separator.join(words)
            })
            words.clear()

    # set temp object args
    def setArgs():
        args = obj.get(Token_Keys.Args) or []
        args.append(value)
        obj[Token_Keys.Args] = args

    for i, l in enumerate(lines):
        for w in l.split():
            (tokenType, value) = GetToken(w, i + 1)  # pass the text line

            if log:
                print((tokenType, value))

            # <laugh> tag for example
            if tokenType is Token_Symbols.SingleTagOpenerAndCloser:
                obj = {Token_Keys.Tag: value}
                ret.append(obj)

            if tokenType is Token_Symbols.TagOpener:
                if isTagBuilding:
                    # Already a tag open
                    raise ValueError(
                        f'Non closing tag {Token_Values.Open} at line {i}: {Token_Values.Open}{value}')

                joinSentence()
                isTagBuilding = True
                obj = {Token_Keys.Tag: value}

            if tokenType is Token_Symbols.SingleStringArg:
                if isTagBuilding:
                    setArgs()
                else:
                    words.append(value)

            if tokenType is Token_Symbols.TagCloser:
                if not isTagBuilding:
                    # Already a tag close
                    raise ValueError(
                        f'Non closing tag {Token_Values.Close} at line {i}: {Token_Values.Close}{value}')

                setArgs()
                ret.append(obj)
                obj = {}
                isTagBuilding = False

            if tokenType is Token_Symbols.Word:
                if isTagBuilding:
                    # Words can appear in sentences or used as tag string literal argument
                    tempargs.append(value)
                else:
                    # String literal expression
                    if isStringLiteralBuilding:
                        stringLiteralAcum.append(value)
                    else:
                        words.append(value)

            if tokenType is Token_Symbols.StartStringArg:
                if isTagBuilding:
                    tempargs.append(value)
                else:
                    isStringLiteralBuilding = True
                    stringLiteralAcum.append(value)

            if tokenType is Token_Symbols.EndStringArg:
                if isTagBuilding:
                    args = obj.get(Token_Keys.Args) or []
                    tempargs.append(value)
                    args.append(Token_Values.Separator.join(tempargs))
                    obj[Token_Keys.Args] = args
                    tempargs = []
                else:
                    stringLiteralAcum.append(value)
                    literal = f'{Token_Values.Quote}{Token_Values.Separator.join(stringLiteralAcum)}{Token_Values.Quote}'
                    words.append(literal)
                    stringLiteralAcum = []
                    isStringLiteralBuilding = False

            if tokenType is Token_Symbols.TagOpenerWithSlash:
                joinSentence()
                ret.append({
                    Token_Keys.Tag: value,
                    Token_Keys.Type: Token_Types.Close
                })

    return ret

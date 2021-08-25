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
    Separator = ' '
    Empty = ''


class Token_Keys:
    Sentence = "sentence"
    Args = "args"
    Tag = "tag"
    Type = "type"


class Token_Types:
    Open = "open"
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
            return (Token_Symbols.StartStringArg, s.replace(Token_Values.Quote, Token_Values.Empty).replace(Token_Values.Close, Token_Values.Empty))
    if isQuoteCloser(s):
        return (Token_Symbols.EndStringArg, s.replace(Token_Values.Quote, Token_Values.Empty))
    return (Token_Symbols.Word, s.replace(Token_Values.Quote, Token_Values.Empty))


def splitByTags(s):

    openTags = [m.start() for m in re.finditer(
        Token_Values.Open, s) if m.start() != 0]

    closeTags = [m.start()for m in re.finditer(
        Token_Values.Close, s) if m.start() != len(s) - 1]

    tags = len(openTags) or len(closeTags)

    if not tags:
        yield s
    else:
        chars = []
        for i, c in enumerate([c for c in s]):

            if i in openTags:
                if len(chars):
                    yield Token_Values.Empty.join(chars)
                chars = []

            if i in closeTags:
                yield Token_Values.Empty.join([*chars, c])
                chars = []
                continue

            chars.append(c)

        if len(chars):
            yield Token_Values.Empty.join(chars)


def splitLineIntoWords(l):
    for w in l.split():
        for auxw in splitByTags(w):
            yield auxw


def wordsByLines(lines):
    for i, l in enumerate(lines):
        yield (i, list(splitLineIntoWords(l)))


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

    for i, line in wordsByLines(lines):
        for word in line:
            (tokenType, value) = GetToken(word, i + 1)  # pass the text line

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

                # Join all acumulated words into a sentence
                if len(words):
                    ret.append({
                        Token_Keys.Sentence: Token_Values.Separator.join(words)
                    })
                    words.clear()

                isTagBuilding = True
                obj = {Token_Keys.Tag: value}

            if tokenType is Token_Symbols.SingleStringArg:
                if isTagBuilding:
                    obj[Token_Keys.Args] = [
                        *(obj.get(Token_Keys.Args) or []), value]
                else:
                    words.append(value)

            if tokenType is Token_Symbols.TagCloser:
                if not isTagBuilding:
                    # Already a tag close
                    raise ValueError(
                        f'Non closing tag {Token_Values.Close} at line {i}: {Token_Values.Close}{value}')

                obj[Token_Keys.Args] = [
                    *(obj.get(Token_Keys.Args) or []), value]
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
                    obj[Token_Keys.Args] = [*(obj.get(Token_Keys.Args) or []), Token_Values.Separator.join(
                        [*tempargs, value])]
                    tempargs = []
                else:
                    words.append(
                        f'{Token_Values.Quote}{Token_Values.Separator.join([*stringLiteralAcum, value])}{Token_Values.Quote}')
                    stringLiteralAcum = []
                    isStringLiteralBuilding = False

            if tokenType is Token_Symbols.TagOpenerWithSlash:

                # Join all acumulated words into a sentence
                if len(words):
                    ret.append(
                        {Token_Keys.Sentence: Token_Values.Separator.join(words)})
                    words.clear()

                ret.append({
                    Token_Keys.Tag: value,
                    Token_Keys.Type: Token_Types.Close
                })

    return ret

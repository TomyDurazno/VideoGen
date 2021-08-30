from Parser.tokenizer import tokenize, Token_Types, Token_Keys
from Providers.providers import tag_providers
from globalSources import GlobalConfig

log = GlobalConfig.LOG
name = GlobalConfig.NAME
mode = GlobalConfig.MODE
parserOnly = GlobalConfig.PARSER_ONLY_MODE
tokenOnly = GlobalConfig.TOKEN_ONLY_MODE
logSentence = GlobalConfig.SENTENCE

name = "guion.txt" if name is None else name

with open("Guiones/" + name, "r", encoding="utf-8") as f:
    # Transform the input text to a series of tokens
    tokens = tokenize(f.read())

if parserOnly:
    exit()

if log:
    print('')

    for token in tokens:
        print(token)

    print('')

    print(f'name: {name}')
    print(f'log: {log}')
    print(f'mode: {mode}')

    print('')

f = open(f"Guiones/{name.split('.')[0]}_clean.txt", "w")

for token in tokens:
    sentence = token.get(Token_Keys.Sentence)
    newline = token.get(Token_Keys.NewLine)

    if sentence:
        f.write(sentence)

        # if logSentence:
        # print(sentence)

    if newline:
        f.write("\n")

f.close()

print('')

if tokenOnly:
    exit()

providers = tag_providers()

for token in tokens:

    tag = token.get(Token_Keys.Tag)

    if tag and token.get(Token_Keys.Type) != Token_Types.Close:

        provider = providers.get(tag)
        if provider:
            provider(*token.get(Token_Keys.Args) or [])
        else:
            print("Non matching provider found: " + tag)

print('')
print('Run finish succesfully')

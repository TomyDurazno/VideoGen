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

f = open("Guiones/" + name, "r", encoding="utf-8")

# Transform the input text to a series of tokens
tokens = tokenize(f.readlines())

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
    if sentence:
        f.write(sentence)
        f.write("\n")
        if logSentence:
            print(sentence)

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

from InputParser.tokenizer import tokenize
from Providers.providers import tag_providers
from globalSources import Config

log = Config.LOG
name = Config.NAME

name = "guion.txt" if name is None else name

f = open("Guiones/" + name, "r", encoding="utf-8")

# Transform the input text to a series of tokens
tokens = tokenize(f.readlines())

if log:
    print("name: " + name)
    print("log: " + str(log))
    print("fullmode: " + str(Config.FULLMODE))

    for token in tokens:
        print(token)

    print("")

providers = tag_providers()

for token in tokens:

    tag = token.get("tag")
    open = token.get("type") != "close"

    if tag and open:

        provider = providers.get(tag)
        if provider:
            provider(*token.get("args") or [])
        else:
            print("Non matching provider found: " + tag)

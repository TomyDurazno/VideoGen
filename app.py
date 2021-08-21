from tokenizer import tokenize
from providers import tag_providers
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

providrs = tag_providers()

for token in tokens:
    # find if the token is a tag
    tag = token.get("tag")

    if tag is not None and token.get("type") != "close":

        providr = providrs.get(tag)

        if(providr is not None):
            args = token.get("args")
            args = args if args is not None else []

            # invoke the provider with the arguments
            try:
                providr(*args)
            except:
                print("An exception occurred")

        else:
            print("Non matching provider found: " + tag)

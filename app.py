from tokenizer import tokenize
from providers import tag_providers
from globalSources import isGlobalLog, nameFromArgs

log = isGlobalLog()

name = nameFromArgs()

if name is None:
    if log:
        print("using story from default file guion.txt")
    name = "Guiones/guion.txt"
else:
    if log:
        print("using story from: " + name)
    name = "Guiones/" + name

f = open(name, "r", encoding="utf-8")

#Transform the input text to a series of tokens
tokens = tokenize(f.readlines())

if log:
    print("")

    for token in tokens:
        print(token)

    print("")

providrs = tag_providers()

for token in tokens:
    #find if the token is a tag
    tag = token.get("tag")
    
    if tag is not None and token.get("type")!= "close":   
        
        providr = providrs.get(tag)
    
        if(providr is not None):            
            args = token.get("args")
            args = args if args is not None else []
    
            #invoke the provider with the arguments
            providr(*args)
        else:
            print("Non matching provider found: " + tag)
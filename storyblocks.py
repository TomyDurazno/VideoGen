from globalSources import isGlobalLog

log = isGlobalLog()

def storyblocksImgProvider(name):
    if(log):
        print("")
        print("calling storyblocks image provider with arg: " + name)
        print("There is no actual implementation for the storyblocks image provider, skipping")
        
def storyblocksMusicProvider(name):
    if(log):
        print("")
        print("calling storyblocks music provider with arg: " + name)
        print("There is no actual implementation for the storyblocks music provider, skipping")        
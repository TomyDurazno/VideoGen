from globalSources import isGlobalLog

log = isGlobalLog()

def localImgProvider(name):
    if(log):
        print("")
        print("calling local image provider with arg: " + name)
        print("There is no actual implementation for the image provider, skipping")
        
def localMusicProvider(name):
    if(log):
        print("")
        print("calling local music provider with arg: " + name)
        print("There is no actual implementation for the local music provider, skipping")        
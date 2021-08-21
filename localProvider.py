from globalSources import Config

log = Config.LOG


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


def localVideoProvider(name):
    if(log):
        print("")
        print("calling local video provider with arg: " + name)
        print("There is no actual implementation for the local video provider, skipping")

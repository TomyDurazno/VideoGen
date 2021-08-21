from globalSources import Config

log = Config.LOG


def notImplemented(name, provider):
    print("")
    print(f'calling {provider} provider with arg: {name}')
    print(
        "There is no actual implementation for {provider}, skipping")


def localImgProvider(name):
    notImplemented(name, "local image")


def localMusicProvider(name):
    notImplemented(name, "local music")


def localVideoProvider(name):
    notImplemented(name, "local video")

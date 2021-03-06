from globalSources import GlobalConfig

log = GlobalConfig.LOG


def notImplemented(name, provider):
    print("")
    print(f'calling {provider} provider with arg: {name}')
    print(f'There is no actual implementation for {provider}, skipping')


def localImgProvider(name):
    notImplemented(name, "local image")


def localMusicProvider(name, source):
    notImplemented(name, "local music")


def localVideoProvider(name):
    notImplemented(name, "local video")


providerMap = {
    "source": "local",
    "tags": {
        "music": localMusicProvider,
        "img": localImgProvider,
        "video": localVideoProvider
    }
}

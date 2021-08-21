from globalSources import Config
from Providers.imgur import imgurProvider
from Providers.storyblocks import storyblocksImgProvider, storyblocksMusicProvider, storyblocksVideoProvider
from Providers.localProvider import localImgProvider, localMusicProvider, localVideoProvider

log = Config.LOG


providers = {
    "music": {
        "storyblocks": storyblocksMusicProvider,
        "local": localMusicProvider
    },
    "img": {
        "imgur": imgurProvider,
        "storyblocks": storyblocksImgProvider,
        "local": localImgProvider
    },
    "video": {
        "storyblocks": storyblocksVideoProvider,
        "local": localVideoProvider
    }
}


def getProviders(key):
    def getImplementation(*args):
        source = args[1]
        provider = providers.get(key).get(source)

        if provider:
            nargs = provider.__code__.co_argcount
            provider(*args[0:nargs])
        else:
            if log:
                print("not found provider for source: " + source)
        return

    return getImplementation


def tag_providers():

    obj = {}
    for k in providers.keys():
        obj[k] = getProviders(k)

    return obj

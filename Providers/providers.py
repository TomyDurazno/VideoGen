from globalSources import GlobalConfig
from Providers.imgur import imgurProvider
from Providers.storyblocks import storyblocksImgProvider, storyblocksMusicProvider, storyblocksVideoProvider
from Providers.localProvider import localImgProvider, localMusicProvider, localVideoProvider

log = GlobalConfig.LOG


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

        if len(args) <= 1:
            if log:
                print("arg not found: source")
            return

        source = args[1]
        provider = providers.get(key).get(source)

        if provider:
            nargs = provider.__code__.co_argcount
            provider(*args[0:nargs])
        else:
            if log:
                print(f'provider for source: {source} not found')
        return

    return getImplementation


def tag_providers():

    obj = {}
    for k in providers.keys():
        obj[k] = getProviders(k)

    return obj

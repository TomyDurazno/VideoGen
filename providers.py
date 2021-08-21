from globalSources import Config
from imgur import imgurProvider
from storyblocks import storyblocksImgProvider, storyblocksMusicProvider
from localProvider import localImgProvider, localMusicProvider

log = Config.LOG

# music providers dictionary


def get_music():
    m = {
        "storyblocks": storyblocksMusicProvider,
        "local": localMusicProvider
    }
    return m

# images providers dictionary


def get_imgs():
    i = {
        "imgur": imgurProvider,
        "storyblocks": storyblocksImgProvider,
        "local": localImgProvider
    }
    return i


def getImgProviders(name, source):

    provider = get_imgs().get(source)

    if provider is not None:
        provider(name)
    else:
        if log:
            print("not found provider for source: " + source)
    return 0


def getMusicProviders(name, source):

    provider = get_music().get(source)

    if provider is not None:
        provider(name)
    else:
        if log:
            print("not found provider for source: " + source)
    return 0


def tag_providers():

    obj = {
        "music": getMusicProviders,
        "img": getImgProviders,
    }

    return obj

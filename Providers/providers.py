from globalSources import GlobalConfig
from Providers.providersMaps import ProvidersMaps

log = GlobalConfig.LOG


def getProviders(key):
    def getImplementation(*args):

        if len(args) <= 1:
            if log:
                print("arg not found: source")
            return

        source = args[1]

        providersForSource = {}
        for pm in ProvidersMaps:
            if pm["source"] == source:
                providersForSource = pm

        if providersForSource is None:
            if log:
                print(f'providers for source: {source} not found')
            return

        provider = providersForSource.get("tags").get(key)

        if provider:
            nargs = provider.__code__.co_argcount
            provider(*args[0:nargs])
        else:
            if log:
                print(f'provider {key} for source: {source} not found')
        return

    return getImplementation


def tag_providers():

    obj = {}
    for map in ProvidersMaps:
        for tag, p in map.get("tags").items():
            obj[tag] = getProviders(tag)
    return obj

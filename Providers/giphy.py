def giphyGifProvider(name):
    print(f'from giphyGifProvider: {name}')


def giphyImgProvider(name):
    print(f'from giphyImgProvider: {name}')


providerMap = {
    "source": "giphy",
    "tags": {
        "gif": giphyGifProvider,
        "img": giphyImgProvider
    }
}

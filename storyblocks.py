import requests
from random import sample
from globalSources import isGlobalLog
from apikeyHMACgeneration import generate


log = isGlobalLog()

# example url
# https://api.graphicstock.com/api/v2/images/search?APIKEY=test_84db697b2f4bfba32add84758f6bd501ea3ccf805ae53dff4aae6a759c3&EXPIRES=1629588362&HMAC=0a50e32c177c11c59cc4586af69dccbd83b60d0d852549625f245de8e67d7a13&project_id=1&user_id=1&keywords=guitars


def buildUrl(args, gen):

    qs = None
    prefix = ""
    for k in ["APIKEY", "EXPIRES", "HMAC"]:
        if qs is not None:
            prefix = "&"
        else:
            qs = ""
            prefix = "?"
        qs = qs + f'{prefix}{k}={gen[k]}'

    url = f'{args["baseUrl"]}{args["resource"]}{qs}&project_id=1&user_id=1'

    return url


def makeRequest(args, keypairs=None):

    gen = generate(args)

    if gen is None:
        print("Hex generation unsuccesful, bypass")
        return

    url = f'{buildUrl(args, gen)}'

    if keypairs:
        suffix = ""
        for k, v in keypairs.items():
            suffix = f'{suffix}&{k}={v}'
        url = url + suffix

    return requests.get(url).json()


def storyblocksImgProvider(name):

    if(log):
        print("")
        print("calling storyblocks image provider with arg: " + name)

    args = {
        "baseUrl": "https://api.graphicstock.com",
        "resource": "/api/v2/images/search"
    }

    result = makeRequest(args, {"keywords": name})

    total = len(result["results"])

    if not total > 0:
        if log:
            print("Couldnt find image for: " + name)
        return

    if log:
        print("Images found: " + str(total))

    index = sample(range(total), 1).pop()

    if(log):
        print("attempting download of index: " + str(index))

    actualImg = result["results"][index]

    # actually downloading the thumbnail
    imgLink = actualImg["thumbnail_url"]

    if log:
        print("Image found: " + imgLink)

    img = requests.get(imgLink)

    extension = imgLink.split(".").pop()

    if(extension not in ["jpg", "png", "jpeg"]):
        print("File found is not an image, downloading it anyways")

    with open("Images/" + name + "." + extension, "wb") as f:
        # download image to local folder
        f.write(img.content)
        return


def storyblocksMusicProvider(name):

    if(log):
        print("")
        print("calling storyblocks music provider with arg: " + name)

    args = {
        "baseUrl": "https://api.audioblocks.com",
        "resource": "/api/v2/audio/search"
    }

    result = makeRequest(args, {"keywords": name})

    total = len(result["results"])

    if not total > 0:
        if log:
            print("Couldnt find music for: " + name)
        return

    if log:
        print("Music found: " + str(total))

    index = sample(range(total), 1).pop()

    music = result["results"][index]

    args["resource"] = f"/api/v2/audio/stock-item/download/{str(music['id'])}"

    fileResult = makeRequest(args)

    # Avoid Downloading 5/5 Limit
    #r = requests.get(fileResult["MP3"], allow_redirects=True)
    #open(f'Music/{name}.mp3', 'wb').write(r.content)

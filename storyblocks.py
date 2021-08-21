import os
from random import sample
from globalSources import Config
from apikeyHMACgeneration import generate
import requests

log = Config.LOG
fullMode = Config.FULLMODE
uniqueNames = Config.UNIQUE_NAMES


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

    # apikeyHMACgeneration
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

    if log:
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

    def downloadImg(index):

        if log:
            print("attempting download of index: " + str(index))

        actualImg = result["results"][index]

        # actually downloading the thumbnail
        link = actualImg["thumbnail_url"]

        if log:
            print("Image found: " + link)

        img = requests.get(link)

        uniqueName = link.split(
            "/").pop().split(".")[0] if uniqueNames else name

        extension = link.split(".").pop()

        if extension not in ["jpg", "png", "jpeg"]:
            print("File found is not an image, downloading it anyways")

        path = "Images/" + name
        isExist = os.path.exists(path)

        if not isExist:
            os.makedirs(path)
            print("New directory is created")

        with open(f'{path}/{uniqueName}.{extension}', "wb") as f:
            # download image to local folder
            f.write(img.content)
            return uniqueName

    # try/except
    def call(index):
        uqname = "NN"
        try:
            uqname = downloadImg(index)
        except:
            print("Exception: " + uqname)

    if not fullMode:
        # pop a random rample
        index = sample(range(total), 1).pop()
        call(index)
    else:
        for i in range(total):
            call(i)


def storyblocksMusicProvider(name):

    if log:
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
    # r = requests.get(fileResult["MP3"], allow_redirects=True)
    # open(f'Music/{name}.mp3', 'wb').write(r.content)


def storyblocksVideoProvider(name):
    if log:
        print("")
        print("calling storyblocks video provider with arg: " + name)
        print("There is no actual implementation for storyblocks video provider, skipping")

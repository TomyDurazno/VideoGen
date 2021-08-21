import requests
from random import sample
from globalSources import isGlobalLog
from apikeyHMACgeneration import generate


log = isGlobalLog()

# example url
# https://api.graphicstock.com/api/v2/images/search?APIKEY=test_84db697b2f4bfba32add84758f6bd501ea3ccf805ae53dff4aae6a759c3&EXPIRES=1629588362&HMAC=0a50e32c177c11c59cc4586af69dccbd83b60d0d852549625f245de8e67d7a13&project_id=1&user_id=1&keywords=guitars

baseUrl = "https://api.graphicstock.com/api/v2/images/search?APIKEY={{apikey}}&EXPIRES={{expires}}&&HMAC={{hmac}}&project_id=1&user_id=1&keywords={{q}}"


def storyblocksImgProvider(name):

    if(log):
        print("")
        print("calling storyblocks image provider with arg: " + name)

    args = {
        "baseUrl": "https://api.graphicstock.com",
        "resource": "/api/v2/images/search"
    }

    gen = generate(args)

    if gen is None:
        print("Hex generation unsuccesful, bypass")
        return

    # print("storyblocks hex:")
    # print(gen)

    url = baseUrl.replace("{{apikey}}", gen["publicKey"]).replace(
        "{{expires}}", gen["expires"]).replace("{{hmac}}", gen["hmacHex"]).replace("{{q}}", name)

    result = requests.get(url).json()

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

    imgLink = result["results"][index]["thumbnail_url"]

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
        print(
            "There is no actual implementation for the storyblocks music provider, skipping")

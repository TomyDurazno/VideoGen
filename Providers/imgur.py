import os
import requests
from random import sample
from globalSources import GlobalConfig

# Imgur url and auth key
imgur_url = "https://api.imgur.com/3/gallery/search"
auth = {"Authorization": "Client-ID 240628d1a11d544"}


log = GlobalConfig.LOG
fullMode = GlobalConfig.FULLMODE
uniqueNames = GlobalConfig.UNIQUE_NAMES


def imgurProvider(name):

    if log:
        print("")
        print("calling imgur provider with arg: " + name)

    result = requests.get(f'{imgur_url}?q={name}', headers=auth)

    for gallery in result.json()["data"]:

        images = gallery.get("images")

        if images is None:
            if log:
                print("not found images for: " + name)
            return

        total = len(images)

        if log:
            print(name)
            print("Images found: " + str(total))

        def downloadImg(index):

            image = images[index]

            link = image["link"]

            if log:
                print("attempting download of index: " + str(index))
                print({'id': image["id"], 'link': link})

            extension = link.split(".").pop()

            img = requests.get(link)

            uniqueName = link.split(
                "/").pop().split(".")[0] if uniqueNames else name

            if extension not in ["jpg", "jpeg", "png"] and log:
                print("File found is not an image, downloading it anyways")

            path = "Images/" + name

            if not os.path.exists(path):
                os.makedirs(path)
                if log:
                    print(f'New directory created: {name}')

            with open(f'{path}/{uniqueName}.{extension}', "wb") as f:
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

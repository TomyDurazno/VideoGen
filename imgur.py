import os
import requests
from random import sample
from globalSources import Config

# Imgur url and auth key
imgur_url = "https://api.imgur.com/3/gallery/search?q="
auth = {"Authorization": "Client-ID 240628d1a11d544"}


log = Config.LOG
fullMode = Config.FULLMODE
uniqueNames = Config.UNIQUE_NAMES


def imgurProvider(name):

    if(log):
        print("")
        print("calling imgur provider with arg: " + name)

    result = requests.get(imgur_url + name, headers=auth)

    for gallery in result.json()["data"]:

        images = gallery.get("images")

        if images is None:
            if(log):
                print("not found images for: " + name)
                return

        total = len(images)

        if(log):
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

            if extension not in ["jpg", "png", "jpeg"]:
                if log:
                    print("File found is not an image, downloading it anyways")

            path = "Images/" + name
            isExist = os.path.exists(path)

            if not isExist:

                # Create a new directory because it does not exist
                os.makedirs(path)

                if log:
                    print("New directory was created")

            with open(f'{path}/{uniqueName}.{extension}', "wb") as f:
                # download image to local folder
                f.write(img.content)
                return

        if not fullMode:
            # pop a random rample
            index = sample(range(total), 1).pop()
            downloadImg(index)
            return
        else:
            for i in range(total):
                downloadImg(i)

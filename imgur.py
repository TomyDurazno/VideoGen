import requests
from random import sample
from globalSources import isGlobalLog

#Imgur url and auth key
imgur_url = "https://api.imgur.com/3/gallery/search?q="
auth = {"Authorization": "Client-ID 240628d1a11d544"}

log = isGlobalLog()

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
        
        imagesLength = len(images)
        
        if(log):
            print("Images found: " + str(imagesLength))

        index = sample(range(imagesLength), 1).pop()    
        
        image = images[index]
        
        if(log):
            print("attempting download of index: " + str(index))
            print({ 'id': image["id"], 'link': image["link"] })
                
        link = image["link"]
        
        extension = link.split(".").pop()
        
        img = requests.get(image["link"])
        
        if(extension not in ["jpg","png","jpeg"]):
            print("File found is not an image, downloading it anyways")
        
        with open("Images/" + name + "." + extension, "wb") as f:
            #download image to local folder  
            f.write(img.content)
            return
          
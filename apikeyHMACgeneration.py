# required modules
import time
import hmac
import hashlib
from config import get_config

# Provided by Storyblocks
#publicKey = "test_84db697b2f4bfba32add84758f6bd501ea3ccf805ae53dff4aae6a759c3"
#privateKey = "test_b97d62ffd8682e556014c4b25a9ebfed66f968570a2a2e5d3e0d6187580"

# url info
#baseUrl = "https://api.graphicstock.com"
#resource = "/api/v2/images/search"


def generate(params):
    # HMAC generation

    conf = get_config()

    if conf is None:
        print("missing config file")
        return None

    privateKey = conf["privateKey"]

    baseUrl = params.get("baseUrl")

    if baseUrl is None:
        raise ReferenceError("missing baseUrl argument")

    resource = params.get("resource")

    if baseUrl is None:
        raise ReferenceError("missing resource argument")

    # Add seconds of a day
    expires = str(int(time.time() + 86400))

    hmacBuilder = hmac.new(bytearray(privateKey + expires, 'utf-8'),
                           resource.encode('utf-8'), hashlib.sha256)
    hmacHex = hmacBuilder.hexdigest()

    obj = {}

    obj["EXPIRES"] = expires
    obj["HMAC"] = hmacHex
    obj["APIKEY"] = conf["publicKey"]
    return obj

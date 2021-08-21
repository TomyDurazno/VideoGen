# required modules
import time
import hmac
import hashlib
from config import get_config


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

    obj = {
        "EXPIRES": expires,
        "HMAC": hmacHex,
        "APIKEY": conf["publicKey"]
    }

    return obj

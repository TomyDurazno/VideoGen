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

    resource = params.get("resource")

    if resource is None:
        raise ReferenceError("missing resource argument")

    privateKey = conf["privateKey"]

    if privateKey is None:
        raise ReferenceError("missing privateKey argument")

    publicKey = conf["publicKey"]

    if publicKey is None:
        raise ReferenceError("missing publicKey argument")

    # Add seconds of a day
    expires = str(int(time.time() + 86400))

    hmacBuilder = hmac.new(bytearray(privateKey + expires, 'utf-8'),
                           resource.encode('utf-8'), hashlib.sha256)
    hmacHex = hmacBuilder.hexdigest()

    obj = {
        "EXPIRES": expires,
        "HMAC": hmacHex,
        "APIKEY": publicKey
    }

    return obj

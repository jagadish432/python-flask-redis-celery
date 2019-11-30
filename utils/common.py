# contains common methoods used overall project

from config import HASH_SECRET
import hmac
import hashlib
import base64

def get_hash(string):
    # print(string)
    digest = hmac.new(HASH_SECRET.encode(), msg=string.encode(), digestmod=hashlib.sha256).digest()
    hash_value = base64.b64encode(digest).decode()
    # print(hash_value)
    return hash_value

import hashlib


TOKEN = 'nouzan414'


def check_signature(signature, timestamp, nonce):
    info = [TOKEN, timestamp, nonce]
    info.sort()
    s = bytes(info[0] + info[1] + info[2], encoding='utf8')
    hashcode = hashlib.sha1(s).hexdigest()
    print("check_signature: hashcode, signature:", hashcode, signature)
    return hashcode == signature

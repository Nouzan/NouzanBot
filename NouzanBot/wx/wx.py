import hashlib
import xml.sax
from .token import TOKEN


def check_signature(signature, timestamp, nonce):
    info = [TOKEN, timestamp, nonce]
    info.sort()
    s = bytes(info[0] + info[1] + info[2], encoding='utf8')
    hashcode = hashlib.sha1(s).hexdigest()
    print("check_signature: hashcode, signature:", hashcode, signature)
    return hashcode == signature


def query_str2dict(query_str):
    strs = query_str.split('&')
    str_dict = {}
    for s in strs:
        k, v = s.split('=')
        str_dict[k] = v
    return str_dict


class MsgHandler(xml.sax.ContentHandler):
    def __init__(self):
        self.buffer = ""
        self.currentTag = ""
        self.mapping = {}

    def startElement(self, tag, attributes):
        self.buffer = ""
        self.currentTag = tag

    def endElement(self, tag):
        self.mapping[tag] = self.buffer

    def characters(self, content):
        if self.currentTag == "Content":
            if self.mapping['MsgType'] == 'text':
                self.buffer = content.encode("utf-8")
            else:
                self.buffer = "!!其他类型的Msg!!"
        else:
            self.buffer += content

    def getDict(self):
        return self.mapping


def receive(msg_xml):
    msg_h = MsgHandler()
    xml.sax.parseString(msg_xml, msg_h)
    msg_data = msg_h.getDict()
    print(msg_data)

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
        self.CurrentData = ""
        self.ToUserName = ""
        self.FromUserName = ""
        self.CreateTime = ""
        self.MsgType = ""
        self.Content = ""

    def startElement(self, tag, attributes):
        self.CurrentData = tag

    def endElement(self, tag):
        pass

    def characters(self, content):
        if self.CurrentData == "ToUserName":
            self.ToUserName = content
        elif self.CurrentData == "FromUserName":
            self.FromUserName = content
        elif self.CurrentData == "CreateTime":
            self.CreateTime = ""
        elif self.CurrentData == "MsgType":
            self.MsgType = content
        elif self.CurrentData == "Content":
            self.Content = content


def receive(msg_xml):
    msg_data = xml.sax.parseString(msg_xml, MsgHandler())
    print(msg_data)

import hashlib
import pprint
import xml.sax
import time
from .models import WxUser, WxTextMsg
from .token import TOKEN
from . import bot


def check_signature(signature, timestamp, nonce):
    if signature is None or timestamp is None or nonce is None:
        return False
    info = [TOKEN, timestamp, nonce]
    info.sort()
    s = bytes(info[0] + info[1] + info[2], encoding='utf8')
    hashcode = hashlib.sha1(s).hexdigest()
    # print("check_signature: hashcode, signature:", hashcode, signature)
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
        self.buffer += content

    def getDict(self):
        return self.mapping


def receive(msg_xml):
    msg_h = MsgHandler()
    xml.sax.parseString(msg_xml, msg_h)
    msg_dict = msg_h.getDict()
    showMsg(msg_dict)
    toUser = WxUser.objects.get_or_create(userName=msg_dict['ToUserName'])
    fromUser = WxUser.objects.get_or_create(userName=msg_dict['FromUserName'])
    if msg_dict['MsgType'] == 'text':
        msg = WxTextMsg.objects.create(
            toUser=toUser,
            fromUser=fromUser,
            createTime=msg_dict['CreateTime'],
            msgType='text',
            content=msg_dict['Content']
        )
    else:
        msg = None
    return reply(bot.run(msg))


def reply(msg):
    return msg.getXml


def showMsg(msg_dict):
    timeArray = time.localtime(int(msg_dict['CreateTime']))
    otherStyleTime = time.strftime("%Y年%m月%d日 %H:%M:%S", timeArray)
    print('*' + otherStyleTime + '*用户(' + msg_dict['FromUserName'] + '):', msg_dict['Content'])

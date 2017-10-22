from django.db import models
from django.utils import timezone


class WxUser(models.Model):
    userName = models.CharField(max_length=128, unique=True)
    name = models.CharField(max_length=128, blank=True)
    rank = models.IntegerField(default=0)
    is_valid = models.BooleanField(default=False)
    created_time = models.DateTimeField(default=timezone.now)
    last_received_time = models.DateTimeField(default=timezone.now)

    def __str__(self):
        if self.name is None or self.name == "":
            return str(self.pk)
        else:
            return self.name


class WxMsg(models.Model):
    toUser = models.ForeignKey(WxUser, on_delete=models.CASCADE, related_name='toUserName')
    fromUser = models.ForeignKey(WxUser, on_delete=models.CASCADE, related_name='fromUserName')
    createTime = models.IntegerField()
    msgType = models.CharField(max_length=128)

    def getCreateDateTime(self):
        return timezone.datetime.fromtimestamp(self.createTime)


class WxTextMsg(WxMsg):
    content = models.CharField(max_length=512)

    XmlForm = """
    <xml>
    <ToUserName><![CDATA[{ToUserName}]]></ToUserName>
    <FromUserName><![CDATA[{FromUserName}]]></FromUserName>
    <CreateTime>{CreateTime}</CreateTime>
    <MsgType><![CDATA[text]]></MsgType>
    <Content><![CDATA[{Content}]]></Content>
    </xml>
    """

    def getXml(self):
        msg = {}
        msg['ToUserName'] = self.toUser.userName
        msg['FromUserName'] = self.fromUser.userName
        msg['CreateTime'] = self.createTime
        msg['Content'] = self.content

        return self.XmlForm.format(**msg)

    def __str__(self):
        return ' '.join([self.getCreateDateTime(), str(self.fromUser), 'to', str(self.toUser), self.content])


class WxObject(models.Model):
    textMsg = models.ForeignKey(WxTextMsg, on_delete=models.CASCADE)
    name = models.CharField(max_length=128, default='object')
    is_valid = models.BooleanField(default=False)

    def getFromUser(self):
        return self.textMsg.fromUser

    def getCreateDateTime(self):
        return timezone.datetime.fromtimestamp(self.textMsg.createTime)

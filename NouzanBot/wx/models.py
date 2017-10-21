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
        return str(self.pk)


class WxMsg(models.Model):
    toUser = models.ForeignKey(WxUser, on_delete=models.CASCADE, related_name='toUserName')
    fromUser = models.ForeignKey(WxUser, on_delete=models.CASCADE, related_name='fromUserName')
    createTime = models.IntegerField()
    msgType = models.CharField(max_length=128)


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
        return ' '.join(str(self.toUser), 'to', str(self.fromUser), self.content)

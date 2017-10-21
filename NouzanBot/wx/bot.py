from .models import WxUser, WxTextMsg
from django.utils import timezone


def run(msg):
    if msg is not None:
        msg.save()
        rep = WxTextMsg.objects.create(
            toUser=msg.fromUser,
            fromUser=msg.toUser,
            createTime=int(timezone.now()),
            msgType='text',
            content=msg.content
        )
        rep.save()
        return rep
    else:
        return None

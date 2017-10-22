from .models import WxUser, WxTextMsg, WxObject
from django.db import models
from django.utils import timezone


class WxFlow(WxObject):
    infoStr = models.CharField(max_length=512)

    def getNextFlow_or_Reply(self):
        if self.is_valid:
            infos = str(self.infoStr).strip().split(' ')
            print(infos)
            if self.name == 'flow':
                if infos != ['']:
                    info = infos.pop(0)
                    if info == 'add':
                        nextFlow = WxFlow.objects.create(
                            textMsg=self.textMsg,
                            name='add-flow',
                            is_valid=True,
                            infoStr=' '.join(infos),
                        )
                        nextFlow.save()
                        self.is_valid = False
                        self.save()
                        return nextFlow.getNextFlow_or_Reply()
                    elif info == 'repeat':
                        self.is_valid = False
                        self.save()
                        return reply(self.textMsg, ' '.join(infos))
                    else:
                        self.is_valid = False
                        self.save()
                        return None
                else:
                    self.is_valid = False
                    self.save()
                    return None
            elif self.name == 'add-flow':
                if infos != ['']:
                    info = infos.pop(0)
                    if info == 'test':
                        self.is_valid = False
                        self.save()
                        return reply(self.textMsg, 'add-flow test')
                    else:
                        self.is_valid = False
                        self.save()
                        return reply(self.textMsg, 'add-flow error')
                else:
                    return reply(
                        self.textMsg,
                        "Please tell me what you want to add:"
                    )
            else:
                self.is_valid = False
                self.save()
                return None
        else:
            return None


def run(msg):
    if msg is not None:
        validFlowSet = WxFlow.objects.filter(is_valid=True, textMsg__fromUser=msg.fromUser)
        if validFlowSet.count() > 0:
            print(validFlowSet[0])
            flow = validFlowSet[0]
            flow.infoStr = msg.content
            flow.save()
            return flow.getNextFlow_or_Reply()
        else:
            flow = WxFlow.objects.create(
                textMsg=msg,
                name='flow',
                is_valid=True,
                infoStr=msg.content,
            )
            flow.save()
            return flow.getNextFlow_or_Reply()
    else:
        return None


def reply(msg, content=''):
    rep = WxTextMsg.objects.create(
        toUser=msg.fromUser,
        fromUser=msg.toUser,
        createTime=int(timezone.now().timestamp()),
        msgType='text',
        content=content
    )
    rep.save()
    return rep

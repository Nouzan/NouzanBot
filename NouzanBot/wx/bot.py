from .models import WxUser, WxTextMsg, WxObject
from django.db import models
from django.utils import timezone
import json


class WxFlow(WxObject):
    infoStr = models.CharField(max_length=512)

    def __str__(self):
        return self.name + ': ' + self.infoStr

    def getNextFlow_or_Reply(self):
        if self.is_valid:
            infos = str(self.infoStr).strip().split(' ')
            print(infos)
            if self.name == 'flow':
                if infos != ['']:
                    info = infos.pop(0)
                    if info == 'add' or info == '添加':
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
                    elif info == 'repeat' or info == '重复':
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
                    if info == '测试':
                        self.is_valid = False
                        self.save()
                        return reply(self.textMsg, 'add-flow test')
                    elif info == '收集任务':
                        self.is_valid = False
                        self.save()
                        nextFlow = WxFlow.objects.create(
                            textMsg=self.textMsg,
                            name='collectTask-add-flow',
                            is_valid=True,
                            infoStr=' '.join(['任务名称'] + infos),
                        )
                        nextFlow.save()
                        flowBuffer = WxFlowBuffer.objects.create(
                            flow=nextFlow,
                            bufferJson=json.dumps({})
                        )
                        flowBuffer.save()
                        return nextFlow.getNextFlow_or_Reply()
                    elif info == '.' or info == '。':
                        self.is_valid = False
                        self.save()
                        return None
                    else:
                        return reply(
                            self.textMsg,
                            "我并不知道你想添加些什么，请重新说（输入句号表示取消添加）："
                        )
                else:
                    return reply(
                        self.textMsg,
                        "请告诉我你想要添加的东西（输入句号表示取消添加）："
                    )
            elif self.name == 'collectTask-add-flow':
                tag = infos.pop(0)
                if infos != ['']:
                    info = infos.pop(0)
                    if info == '.' or info == '。':
                        if tag == '下一个属性名称':
                            self.is_valid = False
                            self.save()
                            flowBuffer = self.flowBuffer
                            bufferJson = json.loads(flowBuffer.bufferJson)
                            return reply(
                                self.textMsg,
                                flowBuffer
                            )
                        else:
                            self.is_valid = False
                            self.save()
                            return None
                    elif tag == '任务名称':
                        flowBuffer = self.flowBuffer
                        bufferJson = json.loads(flowBuffer.bufferJson)
                        bufferJson['name'] = info
                        flowBuffer.bufferJson = json.dumps(bufferJson)
                        flowBuffer.save()
                        self.infoStr = ' '.join(['对象名称'] + infos)
                        self.save()
                        return self.getNextFlow_or_Reply()
                    elif tag == '对象名称':
                        flowBuffer = self.flowBuffer
                        bufferJson = json.loads(flowBuffer.bufferJson)
                        bufferJson['itemName'] = info
                        flowBuffer.bufferJson = json.dumps(bufferJson)
                        flowBuffer.save()
                        self.infoStr = ' '.join(['第一个属性名称'] + infos)
                        self.save()
                        return self.getNextFlow_or_Reply()
                    elif tag == '第一个属性名称':
                        flowBuffer = self.flowBuffer
                        bufferJson = json.loads(flowBuffer.bufferJson)
                        bufferJson['fieldName'] = [info]
                        flowBuffer.bufferJson = json.dumps(bufferJson)
                        flowBuffer.save()
                        self.infoStr = ' '.join(['下一个属性名称'] + infos)
                        self.save()
                        return self.getNextFlow_or_Reply()
                    elif tag == '下一个属性名称':
                        flowBuffer = self.flowBuffer
                        bufferJson = json.loads(flowBuffer.bufferJson)
                        bufferJson['fieldName'] = bufferJson['fieldName'].append(info)
                        flowBuffer.bufferJson = json.dumps(bufferJson)
                        flowBuffer.save()
                        self.infoStr = ' '.join(['下一个属性名称'] + infos)
                        self.save()
                        return self.getNextFlow_or_Reply()
                    else:
                        return reply(
                            self.textMsg,
                            "我并不知道你想添加些什么，请重新说（输入句号表示取消添加）："
                        )
                else:
                    return reply(
                        self.textMsg,
                        "请向我提供“收集任务”的"+ tag +"信息（输入句号表示取消添加）："
                    )
            else:
                self.is_valid = False
                self.save()
                return None
        else:
            return None


class WxFlowBuffer(models.Model):
    flow = models.OneToOneField(
        WxFlow,
        on_delete=models.CASCADE,
    )
    bufferJson = models.CharField(max_length=512)


def run(msg):
    if msg is not None:
        validFlowSet = WxFlow.objects.filter(is_valid=True, textMsg__fromUser=msg.fromUser)
        if validFlowSet.count() > 0:
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

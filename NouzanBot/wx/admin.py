from django.contrib import admin
from .models import WxUser, WxTextMsg, WxCollectTask
from .bot import WxFlow

admin.site.register(WxUser)
admin.site.register(WxTextMsg)
admin.site.register(WxFlow)
admin.site.register(WxCollectTask)

from django.contrib import admin
from .models import WxUser, WxTextMsg
from .bot import WxFlow

admin.site.register(WxUser)
admin.site.register(WxTextMsg)
admin.site.register(WxFlow)

from django.contrib import admin
from .models import WxUser, WxTextMsg

admin.site.register(WxUser)
admin.site.register(WxTextMsg)

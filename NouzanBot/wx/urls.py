from django.conf.urls import url
from . import views


app_name = 'wx'
urlpatterns = [
    url(r'^$', views.handle, name='handle')
]

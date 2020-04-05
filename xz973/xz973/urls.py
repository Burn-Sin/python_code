from django.conf.urls import url
from .import view

 
urlpatterns = [
    url(r'^$',view.xzbook),
    url(r'^jdye',view.jdye),
    url(r'^ceshi',view.ceshi),
    url(r'^xzdata',view.xzdata),
    url(r'^jd',view.jdfanhui)
]


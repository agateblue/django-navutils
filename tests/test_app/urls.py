from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.blank, name='index'),
    url(r'^category/(?P<slug>.*)$', views.blank, name='category'),
]

from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.Index.as_view(template_name='test_app/base.html'), name='index'),
    url(r'^blog$', views.BlogMixin.as_view(template_name='test_app/base.html'), name='blog'),
    url(r'^blog/category/(?P<slug>.*)$', views.CategoryMixin.as_view(template_name='test_app/base.html'), name='category'),
]

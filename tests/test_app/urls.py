from django.urls import path

from . import views

urlpatterns = [
    path('', views.Index.as_view(template_name='test_app/base.html'), name='index'),
    path('blog', views.BlogMixin.as_view(template_name='test_app/base.html'), name='blog'),
    path('blog/category/<slug:slug>', views.CategoryMixin.as_view(template_name='test_app/base.html'), name='category'),
]

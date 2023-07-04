from django.urls import re_path

from .views import query, index

urlpatterns = [
    # url(r'^(.+)/$', index, name='index')
    re_path(r'^index/$', index, name='index'),
    re_path(r'^$', query, name='query')
]

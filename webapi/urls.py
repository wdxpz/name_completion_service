from django.conf.urls import url

from .views import query, index

urlpatterns = [
    # url(r'^(.+)/$', index, name='index')
    url(r'^index/$', index, name='index'),
    url(r'^$', query, name='query')
]
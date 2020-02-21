from django.conf.urls import url
from django.views.generic import TemplateView
from blog.views import IndexView, PostDetailView, ArchivesView, CategoryView, \
                       TagView, ContactView, search, image, upload_file, \
                       SourceView, download, air_price_monitor

app_name = 'blog'

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^post/(?P<pk>[0-9]+)/$', PostDetailView.as_view(), name='detail'),
    url(r'^archives/(?P<year>[0-9]{4})/(?P<month>[0-9]{1,2})/$', ArchivesView.as_view(), name='archives'),
    url(r'^category/(?P<pk>[0-9]+)/$', CategoryView.as_view(), name='category'),
    url(r'^tag/(?P<pk>[0-9]+)/$', TagView.as_view(), name='tag'),
    url(r'^contact/$', ContactView.as_view(), name='contact'),
    url(r'^source/$', SourceView.as_view(), name='source'),
    url(r'^source/(?P<file>.+)/$', download, name='download'),
    url(r'^search', search, name='search'),
    url(r'^img/(?P<name>.+)/$', image, name='image'),
    url(r'^upload/$', upload_file, name='upload'),
    url(r'^airmonitor/$', air_price_monitor)
]

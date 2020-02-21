from django.conf.urls import url
from django.views.generic import TemplateView
from wiki.views import PeopleDetailView
                       

app_name = 'wiki'

urlpatterns = [
    url(r'^wiki$', TemplateView.as_view(template_name="wiki/index.html")),
    url(r'^wiki/people/(?P<name>.*)/$', PeopleDetailView, name='detail'),
]

import datetime

from django.shortcuts import render

DT_FORMAT = "%Y-%m-%d %H:%M:%S"

# Create your views here.
# class IndexView(TemplateView):
#     template_name = 'wiki/index.html'


def PeopleDetailView(request, name):
    with open('people_view_cnt.txt', 'a') as f:
        if '/' not in name:
            now = datetime.datetime.now()
            f.write('{},{}\n'.format(now.strftime(DT_FORMAT), name))
    return render(request, 'wiki/people/{}.html'.format(name))
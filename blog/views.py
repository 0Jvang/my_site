import datetime

from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic import ListView, DetailView, TemplateView
from django.utils.text import slugify
from markdown.extensions.toc import TocExtension
from django.db.models import Q
from django.utils.timezone import now
from django.http import FileResponse
import requests
from lxml import etree
import markdown

from comments.forms import CommentForm
from .models import Post, Category, Tag
from .forms import UploadFileForm

# Create your views here.
class IndexView(ListView):
    model = Post
    template_name = 'blog/index.html'
    context_object_name = 'post_list'
    paginate_by = 8

    def ip_loc(self, ip):
        r = requests.get('http://www.ip138.com/ips1388.asp?ip=' + ip + '&action=2')
        r.encoding = 'gb2312'
        loc = etree.HTML(r.text).xpath('/html/body/table/tr[3]/td/ul/li[1]/text()')[0][5:]
        return loc

    def get_context_data(self, **kwargs):
        #ip = self.request.META.get('HTTP_X_FORWARDED_FOR')
#        try:
#            loc = self.ip_loc(ip)
#        except:
#            loc = 'null'
        #loc = 'null'
        #with open('visitor.txt', 'a') as f:
        #    f.write('{}\t{}\t{}\n'.format(now(), ip, loc))

        context = super().get_context_data(**kwargs)
        paginator = context.get('paginator')
        page = context.get('page_obj')
        is_paginated = context.get('is_paginated')
        pagination_data = self.pagination_data(paginator, page, is_paginated)
        context.update(pagination_data)
        return context

    def pagination_data(self, paginator, page, is_paginated):
        if not is_paginated:
            return {}
        left = []
        right = []
        left_has_more = False
        right_has_more = False
        first = False
        last = False

        page_number = page.number
        total_pages = paginator.num_pages
        page_range = paginator.page_range

        left = page_range[(page_number - 3) if (page_number - 3) > 0 else 0:
        (page_number - 1) if (page_number - 1) > 0 else 0]
        right = page_range[page_number:page_number + 2]

        if right:
            if right[-1] < total_pages:
                last = True
            if right[-1] < total_pages - 1:
                right_has_more = True
        if left:
            if left[0] > 1:
                first = True
            if left[0] > 2:
                left_has_more = True

        data = {'left': left,
                'right': right,
                'left_has_more': left_has_more,
                'right_has_more': right_has_more,
                'first': first,
                'last': last, }

        return data


class CategoryView(IndexView):
    def get_queryset(self):
        # 类视图中从url捕获的命名组参数保存在实例属性的kwargs（字典）中，非命名组参数保存在args（列表）里
        cate = get_object_or_404(Category, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(category=cate)


class TagView(IndexView):
    def get_queryset(self):
        tag = get_object_or_404(Tag, pk=self.kwargs.get('pk'))
        return super().get_queryset().filter(tags=tag)


class ArchivesView(IndexView):
    def get_queryset(self):
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        dayMax = 30
        months = [1, 3, 5, 7, 8, 10, 12]
        if int(month) in months:
            dayMax = 31
        return super().get_queryset().filter(
            created_time__range=(
                datetime.date(int(year), int(month), 1),
                datetime.date(int(year), int(month), dayMax)
            ))


class PostDetailView(DetailView):
    model = Post
    template_name = 'blog/detail.html'
    context_object_name = 'post'

    def get(self, request, *args, **kwargs):
        # 覆写get方法是为了实现文章阅读量+1
        # 先调用父类get方法的原因是，只有当get方法被调用后，才会有self.object属性，即Post模型实例
        response = super().get(request, *args, **kwargs)
        self.object.increase_views()
        return response

    def get_object(self, queryset=None):
        # 此方法是为了对post.body进行渲染
        post = super().get_object(queryset=None)
        md = markdown.Markdown(extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
	    'markdown.extensions.toc',	
        ])
        if '#' in post.body:
            post.body = md.convert(post.body)
            post.toc = md.toc
        else:
            css_lines = []
            for line in post.body.split('\n'):
                css_lines.append('<font face="宋体">{}</font><br>'.format(line.strip()))
            post.body = ''.join(css_lines)
        return post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        form = CommentForm()
        comment_list = self.object.comment_set.all()
        context.update({
            'form': form,
            'comment_list': comment_list,
        })
        return context


class SourceView(TemplateView):
    template_name = 'blog/source.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        source_en = ['char_image.py', 'resume.docx']
        source_zh = ['图片转字符画', '简历']
        context['sources'] = zip(source_en, source_zh)
        return context


def search(request):
    q = request.GET.get('q')
    error_msg = ''
    if not q:
        error_msg = '请输入关键词'
        return render(request, 'blog/index.html', {'error_msg': error_msg})
    post_list = Post.objects.all().filter(Q(title__icontains=q) | Q(body__icontains=q))
    return render(request, 'blog/index.html', {'error_msg': error_msg, 'post_list': post_list})


class ContactView(TemplateView):
    template_name = 'blog/contact.html'


def image(request, name):
    with open('img/' + name + '.png', 'rb') as f:
        content = f.read()
    return HttpResponse(content, content_type='image/png')


def handle_uploaded_file(f):
    with open('img/' + f.name, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)


def upload_file(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            handle_uploaded_file(request.FILES['file'])
            return HttpResponse('ok')
    else:
        form = UploadFileForm()
    return render(request, 'upload.html', {'form': form})


def download(request, file):
    f = open('./source/' + file, 'rb')
    response = FileResponse(f)
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachment;filename="{}"'.format(file)
    return response

from .price_monitor import MonitorPrice
def air_price_monitor(request):
    #from .price_monitor import MonitorPrice

    MonitorAirPrice = type('MonitorAirPrice', (MonitorPrice,), {})
    air_url = 'https://flights.ctrip.com/itinerary/api/12808/lowestPrice'
    trip_msg = {"flightWay":"Oneway","dcity":"CTU","acity":"BJS","army":False}

    monitor_air_price = MonitorAirPrice(air_url, trip_msg)
    now, tbl = monitor_air_price.monitor_price(60*10, '20190703', '20190708')
    return HttpResponse(now + '\n' + tbl)

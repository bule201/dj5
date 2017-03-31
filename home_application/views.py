# -*- coding: utf-8 -*-
from common.mymako import render_mako_context

# first homework
import urllib2
import re
from home_application.models import zhihu
# second homework
import hashlib
from django.http import HttpResponse
# third homework


def home(request):
    tag_url = 'https://www.zhihu.com/topic/19607535/hot'
    try:
        response = urllib2.urlopen(tag_url)
        content = response.read()
        pattern = re.compile('<h2.*?href="(.*?)".*?Title">(.*?)</a></h2>', re.S)
        items = re.findall(pattern, content)
        list_data = zhihu.objects.all()
        list_data.delete()
        for item in items:
            zhihu.objects.create(url=item[0], title=item[1]).save()
        data = list(list_data.values('url', 'title'))

    except urllib2.URLError, e:
        if hasattr(e, "code"):
            print e.code
        if hasattr(e, "reason"):
            print e.reason
    return render_mako_context(request, '/home_application/home.html', {'data': data})


def dev_guide(request):
    if request.method != 'POST':
        return render_mako_context(request, '/home_application/dev_guide.html')

    context = {}
    for file_name, file_stream in request.FILES.iteritems():
        name = request.FILES[file_name].name
        md5sum = hashlib.md5(file_stream.read()).hexdigest()
        context = {
            'upload_file_name': name,
            'upload_file_name_md5': md5sum,
        }
    return HttpResponse(context['upload_file_name_md5'])


def contact(request):
    return render_mako_context(request, '/home_application/contact.html')

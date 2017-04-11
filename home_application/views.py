# -*- coding: utf-8 -*-
from common.mymako import render_mako_context

# first homework
import urllib2
import re
from home_application.models import zhihu
# second homework
import os
import hashlib
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
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
    return render_mako_context(request, '/home_application/dev_guide.html')

@csrf_exempt
def getdata(request):
    data = request.POST
    filename = data['path']
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = file(filename, 'rb')
    while True:
        b = f.read(8096)
        if not b:
            break
        myhash.update(b)
    f.close()
    file_md5 = myhash.hexdigest()
    return HttpResponse(file_md5)


def contact(request):
    return render_mako_context(request, '/home_application/contact.html')


# -*- coding: utf-8 -*-
import urllib2
import re
from common.mymako import render_mako_context
from home_application.models import zhihu

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


def contact(request):
    return render_mako_context(request, '/home_application/contact.html')

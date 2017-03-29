# -*- coding: utf-8 -*-
import urllib2
import re
from common.mymako import render_mako_context
from home_application.models import ZhiHu

def home(request):
    url = 'https://www.zhihu.com/topic/19607535/hot'
    user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
    headers = {'User-Agent': user_agent}
    try:
        request = urllib2.Request(url, headers=headers)
        response = urllib2.urlopen(request)
        content = response.read().decode('utf-8')
        pattern = re.compile('<h2.*?href="(.*?)".*?Title">(.*?)</a></h2>', re.S)
        items = re.findall(pattern, content)
        table_head = {'url', 'title'}
        data = []
        for i in range(5):
            list_data = dict(zip(table_head, list(items[i])))
            ZhiHu.objects.create(url=list_data['url'], title=list_data['title']).save()
            data.append(list_data)
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

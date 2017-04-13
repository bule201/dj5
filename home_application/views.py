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
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex

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

@csrf_exempt
def contact(request):
    if request.method == "POST":
        rec = request.POST
        print rec
        text = rec['text_input']
        padding = bytes('\0')
        key = bytes(rec['salt_input'] + padding * (16 - len(rec['salt_input']) % 16))[:16]
        ase_cryptor = AES.new(key, AES.MODE_CBC, '1234567812345678')

        try:
            if rec['method'] == "encrypt":
                result = b2a_hex(ase_cryptor.encrypt(text + padding * (16 - len(text) % 16)))

            else:
                result = ase_cryptor.decrypt(a2b_hex(text).rstrip('\0'))

            return HttpResponse(result)
        except Exception, e:
            print Exception, ":", e
    else:
        return render_mako_context(request, '/home_application/contact.html')


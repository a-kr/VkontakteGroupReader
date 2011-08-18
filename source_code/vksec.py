req = """POST /login.php HTTP/1.1
Accept: */*
Accept-Charset: windows-1251,utf-8;q=0.7,*;q=0.3
Accept-Encoding: gzip,deflate,sdch
Accept-Language: ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4
Content-Length: %d
Content-Type: application/x-www-form-urlencoded
Cookie:remixchk=5; audio_vol=16; remixsid=530fa78421fcaa9575b5f216a4008cdc50d0ea768d2c2aad96bd7de28d5c
Host: vkontakte.ru
Origin: http://vkontakte.ru
User-Agent: Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1
X-Requested-With: XMLHttpRequest

%s

"""

import httplib, urllib, urllib2
params = urllib.urlencode({
    'act': 'security_check', 
    'al': 1,
    'al_page': '',
    'code': '6046',
    'hash': '9605d0ffbaa08c8778',
})
headers = {"Content-type": "application/x-www-form-urlencoded",
           "Accept": "*/*",
           "Accept-Charset": "windows-1251,utf-8;q=0.7,*;q=0.3",
           "Accept-Encoding": "gzip,deflate,sdch",
           "Accept-Language": "ru-RU,ru;q=0.8,en-US;q=0.6,en;q=0.4",
           "Origin": "http://vkontakte.ru",
           "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/13.0.782.112 Safari/535.1",
           "X-Requested-With": "XMLHttpRequest"}
conn = httplib.HTTPConnection("vkontakte.ru")
conn.request("POST", "/login.php", params, headers)
response = conn.getresponse()
print response.status, response.reason
data = response.read()
print len(data), '"', data, '"', data.encode('hex')

loc = response.getheader('location')
if loc:
    print 'LOC', loc
    rr = urllib2.urlopen(loc)
    print rr.read()
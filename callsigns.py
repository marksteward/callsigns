#!/usr/bin/env python
import sys
from urllib import urlencode
import urllib2
import cookielib
from lxml import etree
from config import email, password, appid

BASE_URL = 'https://services.ofcom.org.uk/'

if len(sys.argv) != 2:
    print("Usage: callsigns.py ./callsigns.txt > ./callsigns_filtered.txt")
    sys.exit(1)

with open(sys.argv[1], 'r') as fp:
    callsigns = fp.readlines()

cookiejar = cookielib.CookieJar()
processor = urllib2.HTTPCookieProcessor(cookiejar)
opener = urllib2.build_opener(processor)
urllib2.install_opener(opener)


def browse(url, params=None):
    if params is not None:
        params = urlencode(params)
        page = urllib2.urlopen(BASE_URL + url, params)
        return etree.HTML(page.read())

logged_in = browse('', {
    'username': email,
    'password': password,
    'submit': 'login',
})

passed = browse('apply/amateur?appId=%s' % appid)
address = browse('apply/amateur?step=2')

params = {
    'step': 2,
    'submit': 'Next',
}

inputs = address.xpath('//input[@type="text"]')
params.update(dict((i.attrib['name'], i.attrib['value']) for i in inputs))

selects = address.xpath('//input[@type="select"]')
for s in selects:
    value = s.xpath('//option[@selected="selected"]')[0]
    params[s.attrib['name']] = value

choose_callsign = browse('/apply/amateur', params)

for callsign in callsigns:
    callsign = callsign.strip()
    params = {
        'step': 3,
        'callsign': callsign.strip(),
        'submit': 'Next',
    }

    confirm = browse('/apply/amateur', params)
    confirm_btn = confirm.xpath('//input[@type="submit"]')[0]
    if confirm_btn.attrib['value'] == 'Confirm information':
        sys.stdout.write("%s\n" % callsign)
    else:
        sys.stderr.write("Not available: %s\n" % callsign)

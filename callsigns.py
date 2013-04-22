#!/usr/bin/env python

from urllib import urlencode
import urllib2, cookielib
from lxml import etree

BASE_URL = 'https://services.ofcom.org.uk/'

email = 'user@example.com'
password = 'password'
appid = '1-123ABC'

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

params= {
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


chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

for i in range(0, 26 * 26 * 26):

  callsign = 'M6%s%s%s' % (chars[i / 26 / 26 % 26], chars[i / 26 % 26], chars[i % 26])

  params= {
    'step': 3,
    'callsign': callsign,
    'submit': 'Next',
  }

  confirm = browse('/apply/amateur', params)
  confirm_btn = confirm.xpath('//input[@type="submit"]')[0]
  if confirm_btn.attrib['value'] == 'Confirm information':
    print callsign


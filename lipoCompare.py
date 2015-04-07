#!/usr/bin/env python3

import requests
import shelve
from operator import itemgetter
from lxml import etree
import sys

us=True

def getData():
  data=[]
  s=1
  maxS=1

  while s<=maxS:
    page=1
    maxPage=1
    while page<=maxPage:
      print('Now processing %dS, page: %d' % (s, page))
      r=requests.get('http://www.hobbyking.com/hobbyking/store/uh_listCategoriesAndProducts.asp?cwhl=%s&pc=&idCategory=86&curPage=%d&v=&sortlist=%s&sortMotor=&LiPoConfig=%d&CatSortOrder=desc' % (('US' if us else 'XX'), page, ('H' if us else 'XX'), s))
      tree=etree.HTML(r.content)
      for input in tree.xpath("//div[@id='tableContent']/div/table/tr/td/table/tr/td/input"):
        sInput=int(input.get('onclick').split('LiPoConfig=')[1].split('&')[0])
        if sInput>maxS:
          maxS=sInput
      for link in tree.xpath("//div[@id='tableContent']/div/form/ul/li/a"):
        pageLink=int(link.get('href').split('curPage=')[1].split('&')[0])
        if pageLink>maxPage:
          maxPage=pageLink
      for item in tree.xpath("//div[@id='tableContent']/div/table/tr[@class='zeroLineHeight']/td/table/tr/td/table/tr/td/div/div/div/span/strong/font[contains(.,'$')]"):
        price=float(item.text.strip().lstrip('$'))
        itemA=item.xpath('../../../../../../div/a')
        href=itemA[0].get('href')
        mAh=[float(x.lower().rstrip('mah')) for x in itemA[0].text.split(' ') if x.lower().endswith('mah')]
        if len(mAh)>0:
          mAh=mAh[0]
        else:
          mAh=[float(x) for x in itemA[0].text.split(' ') if x.isdigit()]
          if len(mAh)>0:
            if len(mAh)>1:
              print('Found more than one mAh for %s, using the first one' % itemA[0].text)
            mAh=mAh[0]
          else:
            print("Couldn't find a mAh for %s" % itemA[0].text)
            continue
        Wh=s*3.7*mAh/1000
        data.append([Wh/price, price, Wh, mAh, s, href, itemA[0].text])
      page+=1
    s+=1
  d=shelve.open('batteries-W%s-V%s.data' % (('US' if us else 'XX'), str(sys.version_info[0])))
  d['data']=data
  d.close()

def processData():
  d=shelve.open('batteries-W%s-V%s.data' % (('US' if us else 'XX'), str(sys.version_info[0])))
  data=d['data']
  d.close()
  data.sort(key=itemgetter(0), reverse=True)
  for item in data[:20]:
    print('Wh/$: %4.2f, Wh: %5.2f, $: %5.2f, s: %s, %s, %s' % (item[0], item[2], item[1], item[4], item[6], item[5]))


getData()
processData()

import urllib
import sys
from itertools import count
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
from datetime import datetime
import collection.crawler as cw
import pandas as pd
from collection.data_dict import sido_dict, gungu_dict

def my_error(e):
    print('myerror:' + str(e))

def proc(html):     #처리
    print("process....:"+html)

def store(result):  #저장
    pass

# result = cw.crawling(
#     url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
#     encoding='cp949',
#     proc=proc,
#     store=store)      #바깥에서 하는거 보다 처리결과 받아서 하는 전처리처럼 안에 쓰자
                    #필터 함수란다.
# html= cw.crawling(
#     url='http://movie.naver.com/movie/sdb/rank/rmovie.nhn',
#     encoding='cp949',
# )
#crawler에서 줄인 코드를 쓰면 이렇게 줄여씀
# def proc(html):
#     print("process....:"+result)
# proc(result)      바깥에서 처리

RESULT_DIRECTORY = '__result__/crawling'

def crawling_pelicana():
    results = []
    for page in count(start=1):
        url = 'http://www.pelicana.co.kr/store/stroe_search.html?gu=&si=&page=%d' % (page)
        html = cw.crawling(url=url)
        # print(url)

        bs = BeautifulSoup(html, 'html.parser')

        tag_table = bs.find('table', attrs={'class':'table mt20'})
        # print(tag_table)
        tag_tbody = tag_table.find('tbody')
        tags_tr = tag_tbody.findAll('tr')
        # print(tags_tr)
        #끝 페이지 검출
        if len(tags_tr) == 0:
            break;

        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
            # print(strings)
            name = strings[1]
            # print(name)
            address = strings[3]
            # print(address.split())
            sidogu = address.split()[:2]    #슬라이싱 이용
            # print(sidogu)

            results.append((name, address) + tuple(sidogu)) #튜플로 넣어주는게 낫다
            #튜플과 튜플을 머지 시켜주면 sidogu가 리스트나 튜플로 안나옴.
            print(results)
        # print(page + ":" + len(tags_tr), sep=':')
    #proc 모든 데이터를 처리하기위해서 프록을 따로 쓸수 없음
    # print(results)
    #로그 남기기
    # print('%s: success for request [%s]' % (datetime.now(), url))


    #store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
    # print(table)

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v)) #처리까지 됐다.
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(
        '{0}/pelicana_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)

def proc_nene(xml):
    # print(xml)
    root = et.fromstring(xml)
    results = []
    # elements_item = root.findAll('item')
    for el in root.findall('item'):
        name = el.findtext('aname1')
        sido = el.findtext('aname2')
        gungu = el.findtext('aname3')
        address = el.findtext('aname5')

        results.append((name, sido, gungu, address))

    return results


def store_nene(data):
    # store
    table = pd.DataFrame(data, columns=['name', 'address', 'sido', 'gungu'])
    # print(table)

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))  # 처리까지 됐다.
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(
        '{0}/nene_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)


def crawling_kyochon():
    results = []
    for sido1 in range(1, 18):
        # sido1 = 'http://www.kyochon.com/shop/domestic.asp?sido1=%s&sido2=0&txtsearch=' % (sido1)
        # print(sido1)
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%s&sido2=%s' % (sido1, sido2)
            # print(url)
            html = cw.crawling(url=url)
            if html == None:
                break   #빠져나가면서 다음 sido가 2로 증가

            # print(html)
            bs = BeautifulSoup(html, 'html.parser')

            tag_div = bs.find('div', attrs={'class': 'shopSchList'})
            tag_li = tag_div.findAll('li')
            # print(tag_li)

            if tag_li == None:
                break;


            for tags_li in tag_li:
                strings = list(tags_li.strings)
                # print(strings)
                # print(strings)

            try:
                name = strings[3]
                address = strings[5].strip()
                sidogu = address.split()[:2]# 슬라이싱 이용
                results.append((name, address) + tuple(sidogu))
                print(sidogu)
            except Exception as e:
                print('%s : %s' % (e, datetime.now()), file=sys.stderr)
                # print(name)


                # print(address)

                # print(sidogu)

                # print(results)

            # print(sido1 + ":" + len(tag_li), sep=':')

        # store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
    print(table)
    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))  # 처리까지 됐다.
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv(
        '{0}/kyochon_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)
    # pass

if __name__ == '__main__':
    #페리카나
    # crawling_pelicana()

    #네네치킨
    # cw.crawling(
    #     url='http://nenechicken.com/subpage/where_list.asp?target_step2=%s&proc_type=step1&target_step1=%s' % (urllib.parse.quote("전체"), urllib.parse.quote("전체")), #urllib.parse.quote하면 encoding 한거로 넘어간다.
    #     proc=proc_nene,
    #     store=store_nene)

    #교촌
    crawling_kyochon()
import urllib
import sys
from itertools import count
from bs4 import BeautifulSoup
import xml.etree.ElementTree as et
from datetime import datetime
from selenium import webdriver
import collection.crawler as cw
import pandas as pd
import time
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
    result = []

    for sido1 in range(1, 18):
        for sido2 in count(start=1):
            url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d&txtsearch=' % (sido1, sido2)
            html = cw.crawling(url=url)

            if html is None:
                break

            bs = BeautifulSoup(html, 'html.parser')
            tag_ul = bs.find('ul', attrs={'class': 'list'})

            for tag_a in tag_ul.findAll('a'):
                tag_dt = tag_a.find('dt')
                if tag_dt is None:
                    break

                name = tag_dt.get_text()

                tag_dd = tag_a.find('dd')
                if tag_dd is None:
                    break

                address = tag_dd.get_text().strip().split('\r')[0]
                sidogu = address.split()[:2]
                result.append((name, address) + tuple(sidogu))

    table = pd.DataFrame(result, columns=['name', 'address', 'sido', 'gungu'])

    # 중복 제거
    table = table.\
        drop_duplicates(subset='name', keep='first').\
        reset_index(drop=True)

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))
    table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))

    table.to_csv('{0}/kyochon_table.csv'.format(RESULT_DIRECTORY), encoding='utf-8', mode='w', index=True)

# def crawling_kyochon():
#     results = []
#     for sido1 in range(1, 18):
#         # sido1 = 'http://www.kyochon.com/shop/domestic.asp?sido1=%s&sido2=0&txtsearch=' % (sido1)
#         # print(sido1)
#         for sido2 in count(start=1):
#             url = 'http://www.kyochon.com/shop/domestic.asp?sido1=%d&sido2=%d' % (sido1, sido2)
#             # print(url)
#             html = cw.crawling(url=url)
#
#
#             if html is None:
#                 break   #빠져나가면서 다음 sido가 2로 증가
#
#
#             # print(html)
#             bs = BeautifulSoup(html, 'html.parser')
#
#             tag_ul = bs.find('ul', attrs={'class': 'list'})
#
#         for tag_a in tag_ul.findAll('a'):
#             tag_dt = tag_a.find('dt')
#             if tag_dt is None:
#                 break
#
#             name = tag_dt.get_text()
#             # print(tag_li)
#
#             tag_dd = tag_a.find('dd')
#
#             if tag_dd == None:
#                 break;
#
#             address = tag_dd.get_text().strip().split('\r')[0]
#             sidogu = address.split()[:2]
#             results.append((name, address) + tuple(sidogu))
#             # print(address)
#
#             # print(sidogu)
#
#             # print(results)
#             # print(sido1 + ":" + len(tag_li), sep=':')
#         # store
#     table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])
#     # print(table)
#
#     table = table. \
#         drop_duplicates(subset='name', keep='first'). \
#         reset_index(drop=True)
#
#     table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))  # 처리까지 됐다.
#     table['gungu'] = table.gungu.apply(lambda v: gungu_dict.get(v, v))
#
#     table.to_csv(
#         '{0}/kyochon_table.csv'.format(RESULT_DIRECTORY),
#         encoding='utf-8',
#         mode='w',
#         index=True)

def crawling_goobne():
    url='http://www.goobne.co.kr/store/search_store.jsp'

    #첫 페이지 로딩
    wd= webdriver.Chrome('D:\PycharmProjects\chromedriver_win32\chromedriver.exe')
    wd.get(url)
    time.sleep(5)
    # print(wd.page_source)

    results = []
    for page in count(start=1):
        #자바스크립트 실행
        script = 'store.getList(%d)' % page
        wd.execute_script(script)   # 실행
        print('%s : success for script execute [%s]' % (datetime.now(), script))
        time.sleep(5)

        # 실행결과 HTML(rendering된 HTML) 가져오기
        html = wd.page_source

        # parsing with bs4
        bs = BeautifulSoup(html, 'html.parser')
        tag_tbody = bs.find('tbody', attrs={'id' : 'store_list'})
        tags_tr = tag_tbody.findAll('tr')   #s붙이면 리스트로 된다.
        # print(tag_tbody)

        #마지막 검출
        if tags_tr[0].get('class') is None:
            break


        for tag_tr in tags_tr:
            strings = list(tag_tr.strings)
        # print(strings)
            name = strings[1]
            address = strings[6]
            sidogu = address.split()[:2]    #어드레스에서 슬라이싱 해서 뽑아내야한다.

            results.append((name, address)+ tuple(sidogu))

        print(results)


    #store
    table = pd.DataFrame(results, columns=['name', 'address', 'sido', 'gungu'])

    table['sido'] = table.sido.apply(lambda v: sido_dict.get(v, v))   #리턴값을 세팅
    table['gungu'] = table.sido.apply(lambda v: gungu_dict.get(v, v))  # 리턴값을 세팅

    table.to_csv(
        '{0}/goobne_table.csv'.format(RESULT_DIRECTORY),
        encoding='utf-8',
        mode='w',
        index=True)

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

    #굽네
    # crawling_goobne()
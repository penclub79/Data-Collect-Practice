from urllib.request import Request, urlopen
from bs4 import BeautifulSoup
request = Request('https://movie.naver.com/movie/sdb/rank/rmovie.nhn?sel=cnt&date=20180618')
resp = urlopen(request)
html = resp.read().decode('cp949') #cp949로 해야 정확한 html을 한글화로 가져올수 있음
# print(html)

bs = BeautifulSoup(html, 'html.parser')
# print(bs.prettify())

tags = bs.findAll('div', attrs={'class':'tit3'})
print(tags)
for index, tag in enumerate(tags):
    print(index+1, tag.a.text, tag.a['hred'], sep=' : ')
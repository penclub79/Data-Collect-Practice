from bs4 import BeautifulSoup

html =  '<td class="title"><div class="tit3">'\
        '<a href="/movie/bi/mi/basic.nhn?code=154285"' \
        ' title="쥬라기 월드: 폴른 킹덤">쥬라기 월드: 폴른 킹덤</a></div></td>'

def ex1():
    bs = BeautifulSoup(html, 'html.parser')
    tag = bs.td
    print(tag)

    tag = bs.a
    print(tag)
    print(tag.name)

    tag = bs.td
    print(tag.div)

def ex2():
    bs = BeautifulSoup(html, 'html.parser')

    tag = bs.td
    print(tag)

def ex3():
    bs = BeautifulSoup(html, 'html.parser')
    tag = bs.find('td', attrs={'class': 'title'})
    print(tag)

    tag = bs.find(attrs={'class':'tit3'})
    print(tag)

if __name__ == '__main__':
    # ex1()
    # ex2()
    ex3()
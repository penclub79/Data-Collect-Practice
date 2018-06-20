import sys #print를 할때 파일을 지정할 수 있어서 스텐다드 에러를 보낼려고
from urllib.request import Request, urlopen
from datetime import datetime

def error(e):
    print('%s : %s' % (e, datetime.now()), file=sys.stderr)


def crawling(
        url='',
        encoding='utf-8',
        proc=lambda html: html,
        store = lambda html: html):
        # err=lambda e: print('%s : %s' % (e, datetime.now()), file=sys.stderr)):

    try:
        request = Request(url)
        resp = urlopen(request)

        try:
            receive = resp.read()
            # result = resp.read().decode(encoding)
            # if proc is not None: 이프는 되도록 쓰지마
            # result = proc(result)
            # if store is not None:
            # result = store(proc(result))
            result = store(proc(receive.decode(encoding)))
            #위 코드를 짧게 줄임
        except UnicodeDecodeError:
            result = receive.decode(encoding, 'replace')
        print('%s: success for request [%s]' % (datetime.now(), url))
        return result

    except:
        pass
    # except Exception as e:
        # err(e)      #이렇게 하면 에러 처리를 한다
        # print('%s : %s' % (e, datetime.now()), file=sys.stderr) <- 얘를 에러함수에 넣음
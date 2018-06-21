import time
from selenium import webdriver

wd = webdriver.Chrome('D:\PycharmProjects\chromedriver_win32\chromedriver.exe')
wd.get('https://developers.facebook.com/apps/454977421629007/dashboard/')

time.sleep(5)
html = wd.page_source
print(html)
wd.quit()
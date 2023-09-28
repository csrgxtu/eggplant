import time
import requests
from selenium import webdriver
from bs4 import BeautifulSoup

# url = "https://v.douyin.com/ievRk7uf/"
# url = "https://v.douyin.com/ievfYXSy/"
# url = "https://v.douyin.com/ievfVbTR/"
# url = "https://v.douyin.com/ievfKAXj/"
# url = "https://v.douyin.com/ievxa2UP/"
url = "https://v.douyin.com/ievxwT5U/"

driver = webdriver.Chrome()
driver.get(url)
time.sleep(5)

with open('./douyin.html', 'w') as f:
    f.write(driver.page_source)

if '<source' not in driver.page_source:
    print('Not Found')

soup = BeautifulSoup(driver.page_source, "html.parser")
sources = soup.find_all('source')
video_link = "https:" + sources[-1].attrs['src']
print(f'Video Link: {video_link}')

driver.get(video_link)
time.sleep(3)
cdn_link = driver.current_url
driver.close()
print(f'After 302: {cdn_link}')

res = requests.get(cdn_link)
print(f'{res.status_code}, {res.headers}')
with open('./test.mp4', 'wb') as f:
    f.write(res.content)
print(f'Done, saved video into file test.mp4')
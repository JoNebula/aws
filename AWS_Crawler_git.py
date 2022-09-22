from selenium import webdriver
import pandas as pd
import requests
import re
from bs4 import BeautifulSoup
from urllib.parse import quote
import json
import time

driver = webdriver.Chrome('./chromedriver.exe')

# URL 내의 검색어에 대한 모든 블로그의 링크를 리스트로 반환
def get_replys(driver,url,links):
    driver.get(url)
    time.sleep(0.5)
    html = driver.page_source

    soup = BeautifulSoup(html, 'lxml')  # html.parse
    posts = soup.find_all("div", attrs={"class": "desc"})
    cnt = 0

    for post in posts:
        cnt += 1
        post_link = post.find("a", attrs={"class":"text"})['href']
        links.append(post_link)

    return links

def get_link(place,driver):
    link = []
    for i in range(1,51):
        try:
            page = i
            url = f"https://section.blog.naver.com/Search/Post.naver?pageNo={page}&rangeType=ALL&orderBy=sim&keyword={quote(place)}"
            link = get_replys(driver,url,link)

            print(str(len(link))+" ", end="")
        except:
            continue
    print("completed")
    return link

def GetNaverBloginfo(URL):
  time.sleep(0.05)
  try:
    NAVERBLOG = URL
    response = requests.get(NAVERBLOG)
    soup = BeautifulSoup(response.text, 'html.parser')
    ifra = soup.find('iframe', id='mainFrame')
    post_url = 'https://blog.naver.com' + ifra['src']
    res = requests.get(post_url)
    soup2 = BeautifulSoup(res.text, 'html.parser')
    titles = soup2.find_all('div', {'class': re.compile('^se-module se-module-text se-title-tex.*')})

    title = titles[0].text
    title = title.replace('\n', '')
    special_char = '\/:*?"<>|.'

    for c in special_char:
        if c in title:
            title = title.replace(c, '')
    text = ''
    txt_contents = soup2.find_all('div', {'class': "se-module se-module-text"})

    for p_span in txt_contents:
        for txt in p_span.find_all('span'):
            text += txt.get_text()

  except:
      return 0,0

  return title, text


list_1 = []
list_2 = []

lk = get_link("남산타워",driver)

for i in lk:
    title, text = GetNaverBloginfo(i)
    list_1.append(title)
    list_2.append(text)
print(title)
print(len(title))


for place in place_list:
    lk = get_link(place,driver)
    print(f"[{place}] Result: ",len(lk))

    for i in lk:
        title, text = GetNaverBloginfo(i)
        if(title==0 and text==0): continue

        list_1.append(title)
        list_2.append(text)

dictionary = {}
main_dict = {}

driver.close()

for place_name in place_list:

    for i in range(len(list_1)):
        dictionary[list_1[i]] = list_2[i]
    main_dict[place_name] = [dictionary]


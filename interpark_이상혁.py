import urllib.request
import requests
import json
from bs4  import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import pandas as pd
import numpy as np 
import time


# WebDriver 초기화
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
url = 'https://isearch.interpark.com/search'

driver = webdriver.Chrome()
driver.get(url) #웹브라우저 열기기능

# 페이지 로딩 대기
driver.implicitly_wait(3)

# `placeholder` 속성을 사용하여 검색창 찾기
search_input = driver.find_element(By.ID, 'searchHeaderInput').send_keys("로마"+ Keys.ENTER)

driver.implicitly_wait(3)

driver.maximize_window()

tour_tab_selector = "div.isearchPage_categoryTabWrap__NQV8m > ul.categoryTab_categoryTab__gdkHf > li.categoryTab_tabItem__BPeI6:nth-child(2) > a"
driver.find_element(By.CSS_SELECTOR, tour_tab_selector).click()
driver.implicitly_wait(3)
current_url = driver.current_url
print("검색 결과 페이지의 URL:", current_url)

last_tab = driver.window_handles[-1]
driver.switch_to.window(window_name=last_tab)


items = driver.find_elements(By.CSS_SELECTOR, "ul.boxList > li.boxItem")



# items = soup.find_all('li', class_='tour_tourItem__StmU1')
# titles = [item.find('div', class_='itemTitle_title__vxNmU').get_text(strip=True) for item in items]
# prices = [item.find('strong').get_text(strip=True) for item in items]
# df = pd.DataFrame({'ItemTitle': titles, 'ItemPrice': prices})
# Extract item titles and prices
titles = []
prices = []


# Loop through each link element with product data
time.sleep(2)

for item in items:
    # 상품 제목
    title = item.find_element(By.CLASS_NAME, "infoTitle").text
    titles.append(title)
print(titles)
    # 상품 가격
    # infoPrice 요소 전체를 찾고, 그 내부에서 개별 정보 찾기
#     info_price = item.find_element(By.CLASS_NAME, "infoPrice")

#     # 판매가
#     sale_price = info_price.find_element(By.CLASS_NAME, "final").find_element(By.TAG_NAME, "strong").text
#     prices.append(sale_price)
    

# for title, price in zip(titles, prices):
#     print(f"상품명: {title}, 가격: {price}원")

# for link in soup.find_all('a', attrs={'data-prd-name': True}):
#     # Get the title from 'data-prd-name' attribute
#     title = link['data-prd-name']
#     titles.append(title)
    
#     # Find the price within this element
#     price_tag = link.find('strong')
#     price = price_tag.get_text(strip=True) if price_tag else 'N/A'
#     prices.append(price)

# Create DataFrame
# df = pd.DataFrame({'ItemTitle': titles, 'ItemPrice': prices})

# # Save to JSON
# df.to_json('interpark_data.json', orient='records', force_ascii=False)

# # Save to CSV
# df.to_csv('interpark_data.csv', index=False, encoding='utf-8-sig')

# print(df)
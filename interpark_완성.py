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
import sys;
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

url = 'https://isearch.interpark.com/search'

driver = webdriver.Chrome()
driver.get(url) #웹브라우저 열기기능

# 페이지 로딩 대기
driver.implicitly_wait(3)

# `placeholder` 속성을 사용하여 검색창 찾기
search_input = driver.find_element(By.ID, 'searchHeaderInput').send_keys("로마"+ Keys.ENTER)

driver.implicitly_wait(3)


#윈도우 확장해야... xpath 확인 가능할 것으로 생각함.
driver.maximize_window()

tour_tab_selector = "/html/body/div[1]/div[1]/div/section[1]/div[1]/ul/li[2]/a"
driver.find_element(By.XPATH, tour_tab_selector).click()
driver.implicitly_wait(3)
last_tab = driver.window_handles[-1]
driver.switch_to.window(window_name=last_tab)
current_url = driver.current_url

print("검색 결과 페이지의 URL:", current_url)

tour_tab_selector = "/html/body/div[1]/div/div[1]/div/div[3]/div[2]/div[1]/div/button"
driver.find_element(By.XPATH, tour_tab_selector).click()
current_url = driver.current_url
print("현재 URL: ", current_url)

items = driver.find_elements(By.CSS_SELECTOR, "ul.boxList > li")

titles = []
prices = []

# xpath 있는지 확인. //2024.10.15 수정... 쓸데없는 오지랖이었음
# def isExistXpath(xpath):
#     try:
#         driver.find_element(By.XPATH, xpath)
#         return True
#     except:
#         return False
# index = 1


while True:
    try:
        # 새로 요소를 로드하여 동적 갱신 반영
        time.sleep(1)  # 페이지 안정화를 위해 잠깐 대기

        # 패키지 이름 가져오기
        title_xpath = f'//*[@id="boxList"]/li[{index}]/div/div[2]/div[2]/div[1]/a/h5'
        title = driver.find_element(By.XPATH, title_xpath).text

        base_price_xpath = f'//*[@id="boxList"]/li[{index}]/div/div[2]/div[2]/div[2]/div/p/strong'
        price = driver.find_element(By.XPATH, base_price_xpath).text

        print(title, "\t", price)
        titles.append(title)
        prices.append(price)

        index += 1  # 다음 아이템으로 이동

    except Exception as e:
        print(f"Error processing item {index}: {e}")
        break  # 더 이상 항목이 없을 경우 종료
# DataFrame으로 저장 및 출력
df = pd.DataFrame({'패키지 이름': titles, '가격': prices})
print(df)
df.to_csv('인터파크.csv', index=False, encoding='utf-8-sig')

driver.quit()

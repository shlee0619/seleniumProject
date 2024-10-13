import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# 웹드라이버 설정
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
driver = webdriver.Chrome(options=options)

# 웹툰 페이지 URL 설정
url = "https://comic.naver.com/webtoon/detail?titleId=777767&no=162&week=fri"
driver.get(url)

# 페이지 로딩 대기
wait = WebDriverWait(driver, 10)
wait.until(EC.presence_of_element_located((By.CLASS_NAME, "u_cbox_list")))

# 댓글 및 답글 데이터를 저장할 리스트
comments_data = []

# 전체 댓글 리스트 가져오기
comments = driver.find_elements(By.CSS_SELECTOR, 'ul.u_cbox_list > li.u_cbox_comment')

# 댓글 정보 추출
for idx, comment in enumerate(comments, start=1):
    
    # 클린봇 필터 적용된 댓글은 제외
    if comment.find_elements(By.CLASS_NAME, 'u_cbox_cleanbot_contents'):
        print(f"{idx}번째 댓글은 '클린봇'이 부적절한 표현을 감지하여 패스합니다.\n")
        continue
    
    # 댓글 정보 추출
    u_cbox_nick = comment.find_element(By.CLASS_NAME, 'u_cbox_nick').text
    u_cbox_contents = comment.find_element(By.CLASS_NAME, 'u_cbox_contents').text
    u_cbox_date = comment.find_element(By.CLASS_NAME, 'u_cbox_date').text
    u_cbox_cnt_recomm = comment.find_element(By.CLASS_NAME, 'u_cbox_cnt_recomm').text
    u_cbox_reply_cnt = int(comment.find_element(By.CLASS_NAME, 'u_cbox_reply_cnt').text)

    # 댓글 데이터 구조에 답글 포함
    comment_entry = {
        '닉네임': u_cbox_nick,
        '내용': u_cbox_contents,
        '날짜': u_cbox_date,
        '추천 수': u_cbox_cnt_recomm,
        '답글': []
    }
    
    # 답글이 있는 경우 답글 목록을 수집
    if u_cbox_reply_cnt > 0:
        reply_button = comment.find_element(By.CLASS_NAME, 'u_cbox_btn_reply')
        driver.execute_script("arguments[0].click();", reply_button)
        time.sleep(2)  # 답글 로딩 대기
        while True:
            try:
                # 'Load More' button for replies
                more_button = comment.find_element(By.CLASS_NAME, 'u_cbox_btn_more')
                driver.execute_script("arguments[0].click();", more_button)
                time.sleep(2)  # 로딩 대기
            except:
                print("모든 답글 로딩완료")
                break
        # 답글 가져오기
        replies = comment.find_elements(By.CLASS_NAME, 'u_cbox_comment')
        time.sleep(0.3)
        for reply in replies:
            if reply.find_elements(By.CLASS_NAME, 'u_cbox_cleanbot_contents'):
                print(f"{idx}번째 댓글의 답글은 '클린봇'이 부적절한 표현을 감지하여 패스합니다.\n")
                continue

            reply_nick = reply.find_element(By.CLASS_NAME, 'u_cbox_nick').text
            reply_content = reply.find_element(By.CLASS_NAME, 'u_cbox_contents').text
            reply_date = reply.find_element(By.CLASS_NAME, 'u_cbox_date').text
            reply_recomm = reply.find_element(By.CLASS_NAME, 'u_cbox_cnt_recomm').text
            
            # 답글 데이터 추가
            comment_entry['답글'].append({
                '답글 닉네임': reply_nick,
                '답글 내용': reply_content,
                '답글 날짜': reply_date,
                '답글 추천 수': reply_recomm
            })
    
    comments_data.append(comment_entry)
    print(comment_entry['답글'])
    break

# # 드라이버 종료
# driver.quit()

# # 데이터프레임으로 변환
# df = pd.DataFrame(comments_data)
# print(df)

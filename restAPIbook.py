import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os

#성공
def getBookstoreData(numOfRows, pageNo):
    print()
    print('중고서점 조회 getBookstoreData() ')
    url = "http://api.kcisa.kr/API_CNV_045/request"

    # 파라미터 설정
    params = {
        'serviceKey': 'a1d0e4c6-aa4b-4c17-ba08-b2fe46a3ff8c',  # 실제 서비스 키로 대체하세요
        'numOfRows': numOfRows,  # 세션당 요청 레코드 수 입력
        'pageNo': pageNo  # 페이지 번호 입력
        # 'resultType': 'json'  # XML 응답을 받을 것이므로 주석 처리
    }

    # 헤더 설정
    headers = {
        "Content-type": "application/xml"
    }

    # GET 요청 보내기
    response = requests.get(url, params=params, headers=headers)

    # 응답 코드 출력
    print("Response code:", response.status_code)

    # 응답 처리
    if 200 <= response.status_code <= 300:
        return response.text
    else:
        print("Error:", response.text)
        return None

# 메인 실행 부분
result = []

xml_data = getBookstoreData('10', '1')

if xml_data:
    root = ET.fromstring(xml_data)
    resultCode = root.find('.//resultCode').text
    if resultCode == '0000':
        totalCount = int(root.find('.//totalCount').text)
        numOfRows = int(root.find('.//numOfRows').text)
        totalPages = (totalCount - 1) // numOfRows + 1  # 전체 페이지 수 계산

        for page in range(1, totalPages + 1):
            xml_data = getBookstoreData(str(numOfRows), str(page))
            if xml_data:
                root = ET.fromstring(xml_data)
                items = root.findall('.//item')
                for item in items:
                    FCLTY_NM = item.findtext('FCLTY_NM', '')
                    FCLTY_ROAD_NM_ADDR = item.findtext('FCLTY_ROAD_NM_ADDR', '')
                    ADIT_DC = item.findtext('ADIT_DC', '')
                    result.append([FCLTY_NM, FCLTY_ROAD_NM_ADDR, ADIT_DC])
            else:
                print(f"{page} 페이지 데이터를 가져오지 못했습니다.")
    else:
        resultMsg = root.find('.//resultMsg').text
        print("API 호출 오류:", resultMsg)
else:
    print("데이터를 가져오지 못했습니다.")

print()
print(result)
df = pd.DataFrame(result, columns=['FCLTY_NM', 'FCLTY_ROAD_NM_ADDR', 'ADIT_DC'])
path = './data/Bookstore.csv'
os.makedirs(os.path.dirname(path), exist_ok=True)
df.to_csv(path, encoding='utf-8-sig', index=False)
print(f"{path} 파일 저장 성공했습니다")
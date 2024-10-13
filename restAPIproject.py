import requests
import xml.etree.ElementTree as ET
import pandas as pd
import os

# 데이터 가져오기 함수
def getAreaData(sigunguCd, bjdongCd, platGbCd, bun, ji, numOfRows, pageNo):
    print('국토교통부_건축인허가 기본개요 조회')
    
    # API 엔드포인트 URL
    url = "https://apis.data.go.kr/1613000/ArchPmsService_v2/getApBasisOulnInfo"
    
    # 파라미터 설정
    params = {
        "serviceKey": "oMM+qUd5Dvoar9itmtJ3rwqG/Hs67am/x1RZf0vts3eTBQo9895J9yQZfewclR7d1zPNmvk1uIeJ1/cM/QHV9w==",
        "sigunguCd": sigunguCd,
        "bjdongCd": bjdongCd,
        "platGbCd": platGbCd,
        "bun": bun,
        "ji": ji,
        "numOfRows": numOfRows,
        "pageNo": pageNo
    }
    
    # GET 요청 보내기
    response = requests.get(url, params=params, verify=False)
    
    # 응답 처리
    if response.status_code == 200:
        return response.content
    else:
        print("API 요청 실패:", response.status_code)
        return None

# 메인 실행 부분
result = []

# 첫 페이지 데이터 가져오기
xml_data = getAreaData('11680', '10300','0','0012', '0004','10', '1')

if xml_data:
    root = ET.fromstring(xml_data)
    resultCode = root.find('.//resultCode').text
    if resultCode == '00':  # '00'이 정상 응답 코드입니다.
        totalCount = int(root.find('.//totalCount').text)
        numOfRows = int(root.find('.//numOfRows').text)
        totalPages = (totalCount - 1) // numOfRows + 1  # 전체 페이지 수 계산

        for page in range(1, totalPages + 1):
            xml_data = getAreaData('11680', '10300','0','0012', '0004', str(numOfRows), str(page))
            if xml_data:
                root = ET.fromstring(xml_data)
                items = root.findall('.//item')
                for item in items:
                    archArea = item.find('archArea').text
                    archGbCdNm = item.find('archGbCdNm').text
                    platPlc = item.find('platPlc').text
                    # 필요한 데이터 추가
                    result.append([archArea, archGbCdNm, platPlc])
            else:
                print(f"{page} 페이지 데이터를 가져오지 못했습니다.")
    else:
        resultMsg = root.find('.//resultMsg').text
        print("API 호출 오류:", resultMsg)
else:
    print("데이터를 가져오지 못했습니다.")

# 결과 출력 및 저장
df = pd.DataFrame(result, columns=['ArchArea', 'ArchGbCdNm', 'PlatPlc'])
path = './data/ArchitectureData.csv'
os.makedirs(os.path.dirname(path), exist_ok=True)
df.to_csv(path, encoding='utf-8-sig', index=False)
print(f"{path} 파일 저장 성공했습니다")

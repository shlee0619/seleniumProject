import requests
import xml.etree.ElementTree as ET
import pandas as pd
from tqdm import tqdm  # 진행률 바를 표시하기 위해 사용합니다.

# API 기본 정보 설정
service_key = 'oMM%2BqUd5Dvoar9itmtJ3rwqG%2FHs67am%2Fx1RZf0vts3eTBQo9895J9yQZfewclR7d1zPNmvk1uIeJ1%2FcM%2FQHV9w%3D%3D'
base_url = 'https://apis.data.go.kr/1300000/tjsBdgg/list'

# 첫 번째 요청을 보내 총 데이터 개수(totalCount)를 얻습니다.
params = {
    'serviceKey': service_key,
    'numOfRows': 10,
    'pageNo': 1
}

response = requests.get(base_url, params=params)
root = ET.fromstring(response.content)

# 네임스페이스 제거를 위한 함수
def remove_namespace(tag):
    if '}' in tag:
        return tag.split('}', 1)[1]
    else:
        return tag

# 총 데이터 개수 추출
total_count = int(root.find('.//totalCount').text)
print(f'총 데이터 개수: {total_count}')

# 데이터를 저장할 리스트 초기화
data_list = []

# 한 번에 가져올 행의 수 설정 (최대 1000으로 설정 가능합니다)
num_of_rows = 1000
total_pages = (total_count // num_of_rows) + 1

# 각 페이지에 대해 데이터 수집
for page_no in tqdm(range(1, total_pages + 1), desc='데이터 수집 중'):
    params = {
        'serviceKey': service_key,
        'numOfRows': num_of_rows,
        'pageNo': page_no
    }
    response = requests.get(base_url, params=params)
    root = ET.fromstring(response.content)
    
    items = root.findall('.//item')
    for item in items:
        data = {}
        for child in item:
            tag = remove_namespace(child.tag)
            data[tag] = child.text
        data_list.append(data)

# 데이터프레임으로 변환
df = pd.DataFrame(data_list)

# CSV 파일로 저장
df.to_csv('api_data.csv', index=False, encoding='utf-8-sig')
print('CSV 파일로 저장이 완료되었습니다.')

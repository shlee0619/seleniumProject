import urllib.request
import urllib.parse
import json
import pandas as pd
import os

#성공
#1단계
def getRequestURL(url, enc='utf-8'):
    request = urllib.request.Request(url)
    response = urllib.request.urlopen(request)
    if response.getcode() == 200:
        print(f"[{url}] 요청 성공")
        first = response.read()
        ret = first.decode(enc)
        return ret
    else:
        print("Error Code:", response.getcode())
        return None

def getAirsido(returnType, numOfRows, pageNo, sidoName, ver):
    print()
    print('공공데이터 시도별 실시간 측정정보 조회 getAirsido() ')
    serviceKey = 'oMM%2BqUd5Dvoar9itmtJ3rwqG%2FHs67am%2Fx1RZf0vts3eTBQo9895J9yQZfewclR7d1zPNmvk1uIeJ1%2FcM%2FQHV9w%3D%3D'  # 실제 서비스 키로 대체하세요
    url = 'http://apis.data.go.kr/B552584/ArpltnInforInqireSvc/getCtprvnRltmMesureDnsty'
    parameters = {
        'serviceKey': serviceKey,
        'returnType': returnType,
        'numOfRows': numOfRows,
        'pageNo': pageNo,
        'sidoName': sidoName,
        'ver': ver
    }
    encoded_params = urllib.parse.urlencode(parameters, safe="%")
    full_url = f"{url}?{encoded_params}"
    print(full_url)
    print()
    ret_data = getRequestURL(full_url)
    return json.loads(ret_data)

#3단계
result = []
# 문서형태 json 100행개수 1페이지 서울지역 version=1.0
json_data = getAirsido('json', '100', '1', '서울', '1.0')
if json_data['response']['header']['resultMsg'] == 'NORMAL_CODE':
    items = json_data['response']['body']['items']
    for i in range(6):
        sidoName = items[i]['sidoName']
        stationName = items[i]['stationName']
        o3Value = items[i]['o3Value']  # 오존농도
        no2Value = items[i]['no2Value']  # 이산화질소농도
        pm10Grade = items[i]['pm10Grade']  # 미세먼지농도
        print(f'sidoName={sidoName} stationName={stationName} o3Value={o3Value} no2Value={no2Value} pm10Grade={pm10Grade}')
        result.append([sidoName, stationName, o3Value, no2Value, pm10Grade])
else:
    print("API 호출 오류:", json_data['response']['header']['resultMsg'])

print()
print(result)
df = pd.DataFrame(result, columns=['sidoName', 'stationName', 'o3Value', 'no2Value', 'pm10Grade'])
path = './data/Air.csv'
os.makedirs(os.path.dirname(path), exist_ok=True)
df.to_csv(path, encoding='utf-8-sig', index=False)
print(f"{path} 파일 저장 성공했습니다")
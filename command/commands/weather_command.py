from irispy2 import ChatContext
import requests

def get_weather():
    session = requests.Session()

    # 1단계: 첫 요청 (예: 다음 모바일 날씨 검색)
    search_url = 'https://m.search.daum.net/search'
    params = {
        'nil_profile': 'btn',
        'w': 'tot',
        'DA': 'SBC',
        'q': '날씨 서울'
    }
    headers = {
        'User-Agent': 'Mozilla/5.0',
        'Accept-Language': 'ko-KR,ko;q=0.9',
    }

    response1 = session.get(search_url, params=params, headers=headers)
    print("첫 요청 완료, 받은 쿠키들:", session.cookies.get_dict())

    cookies = session.cookies.get_dict()

    second_url = f'https://m.search.daum.net/qsearch?uk={cookies['uvkey']}&w=weather&m=balloon&lcode=I&viewtype=json&type=0'
    response2 = session.get(second_url, headers=headers)

    print("두 번째 요청 완료, 상태 코드:", response2.status_code)
    print("응답 일부:", response2.text[:500])  # 결과 일부 출력
    return response2.json()

class WeatherCommand:
    invoke = "날씨"
    help = "!날씨 <지역>"
    type = "kl"

    def handle(self, event:ChatContext, kl):
        wheather = get_weather()['RESULT']['WEATHER_BALLOON']['result']
        kl.send(
                receiver_name=event.room.name,
                template_id=15476,
                template_args={
                    "${TH_IMAGE_URL_0}": wheather
                },
            )
        



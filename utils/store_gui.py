import json
import os
import re
from io import BytesIO

import requests
from PIL import Image



BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

def get_store(type_name: str, page: int, sess):
    data_file = os.path.join(BASE_DIR, "assets", "avatar_data", f"{type_name}.json")
    with open(data_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    limit = 40
    offset = (page - 1) * limit
    items = data["itemList"][offset:offset + limit]
    sess["type"] = items



def get_avatar(inventory):
    # POST 보낼 URL
    url = "https://meaegi.com/dressing-room"

    # payload 구성 (itemCode 부분에 변수 사용)
    payload = [
        {
            "gender": 1,
            "earType": 0,
            "weaponMotion": 0,
            "variation": 0,
            "itemCode": inventory,
            "itemPrism": {
                "hair": {
                    "baseColor": 0,
                    "mixColor": 7,
                    "mixRate": 50
                }
            }
        }
    ]

    # 요청 헤더 (필요에 따라 수정)
    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "Next-Action":"f6097e19afeedc0220b15f769fbcae478c540a0f"
    }

    # POST 요청
    response = requests.post(url, headers=headers, data=json.dumps(payload))

    # 결과 출력
    if response.ok:
        match = re.search(r'1:"([^"]+)"', response.text)
        if match:
            result = match.group(1)
            print("1번 값:", result)
            return result
        else:
            print("값을 찾을 수 없음")
            return False
    else:
        print("실패:", response.status_code, response.text)
        return False

def get_avatar_img(data):
    url = f"https://avatar.maplestory.nexon.com/Character/180/{data}.png"  # 네가 가져올 이미지 URL
    return url
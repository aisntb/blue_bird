import time

from utils.store_gui import get_store, get_avatar, get_avatar_img

# 메뉴 리스트는 이전과 동일
menu = [
    "귀고리", "눈장식", "망토", "모자", "무기", "방패", "상의", "성형",
    "신발", "얼굴장식", "장갑", "피부", "하의", "한벌옷", "헤어"
]

active_users = {}
inventory = {}
SESSION_TIMEOUT = 60  # 1분

def add_user(user_id):
    now = time.time()
    active_users[user_id] = {
        "timestamp": now,
        "type": None
    }

def cleanup_users():
    now = time.time()
    expired = [uid for uid, data in active_users.items() if now - data["timestamp"] > SESSION_TIMEOUT]
    for uid in expired:
        del active_users[uid]
        print(f"[세션 만료] {uid}")

def show_menu():
    return "\n".join(f"{i+1}. {item}" for i, item in enumerate(menu))

def handle_user_input(event, kl):
    cleanup_users()  # 매 입력 때마다 만료 세션 정리
    user_id = event.sender.id
    input_str = event.message.msg
    if user_id not in active_users:
        return False
    if input_str.isdigit() and active_users[user_id]["type"] is None:
        choice = int(input_str)
        if 1 <= choice <= len(menu):
            selected_item = menu[choice - 1]
            get_store(selected_item, 1, active_users[user_id])
            kl.send(
                receiver_name=event.room.name,
                template_id=15476,
                template_args={
                    "${TH_IMAGE_URL_0}": f"https://ondojung.mycafe24.com/api/maple/store.php?type={selected_item}&page=1",
                    "${TITLE}": "다음 페이지로 이동 하시려면 >다음 을 입력해주세요.",
                    "${SHARED_FROM}": "ondojung.mycafe24.com"
                }
            )
            return f"'{selected_item}' 아이템을 선택하셨습니다."
        else:
            return "번호가 메뉴 범위를 벗어났어요. 다시 입력해주세요."
    elif active_users[user_id]["type"] is not None:
        choice = int(input_str)
        data = active_users[user_id]["type"][choice-1]
        add_inventory(user_id, data)

        code = get_avatar(inventory[user_id])
        img = get_avatar_img(code)
        kl.send(
            receiver_name=event.room.name,
            template_id=15476,
            template_args={
                "${TH_IMAGE_URL_0}": img
            },
        )
        return None
    else:
        return "번호를 입력해주세요."

slot_name={
    "피부":"skin",
    "성형":"face",
    "헤어":"hair",
    "모자":"cap",
    "얼굴장식":"faceDeco",
    "눈장식":"eyeDeco",
    "귀고리":"earring",
    "한벌옷":"dress",
    "상의":"dress",
    "하의":"pants",
    "신발":"shoes",
    "장갑":"glove",
    "방패":"subWeapon",
    "망토":"cape",
    "무기":"weapon"
}


def add_inventory(user_id, data:dict):
    if user_id not in inventory:
        inventory[user_id] = {}
    type_name = slot_name[data["slot"]]
    inventory[user_id][type_name] = data["code"]


def reset_inventory(user_id):
    inventory[user_id] = {}
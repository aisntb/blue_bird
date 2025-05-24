import io
import os
import re

import yaml
from dataclasses import dataclass, field
from typing import Dict, List
from iris import ChatContext

from utils.store_gui import get_store, get_avatar, get_avatar_img

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
menus_file = os.path.join(BASE_DIR, "assets" ,"avatar_menu.yml")

with open(menus_file, encoding='utf-8') as f:
    tree = yaml.safe_load(f)

# flat 메뉴 맵과 parent 맵 생성
menu_tree: Dict[int, Dict[str, List[int]]] = {}
parent_map: Dict[int, int] = {}

@dataclass
class Frame:
    menu_id: int
    cursor: int = 0

@dataclass
class Session:
    stack: List[Frame] = field(default_factory=list)
    mode: str = "default"  # 또는 "shop"
    shop_stack: List[dict] = field(default_factory=list)
    shop_cursor: int = 0
    inventory_stack: dict = field(default_factory=dict)
    inventory_cursor: int = 0

# 재귀적으로 트리 순회하여 flat 맵 생성
def _build_maps(node: Dict, parent: int = None):
    mid = node['id']
    menu_tree[mid] = {
        'name': node['name'],
        'options': [child['id'] for child in node.get('options', [])],
        'action': node.get('action'),
        'value': node.get('value'),
    }
    parent_map[mid] = parent
    for child in node.get('options', []):
        _build_maps(child, mid)
# YAML 루트 노드를 빌드
_build_maps(tree, None)

# 유저별 세션 저장소
_sessions: Dict[int, Session] = {}

def get_session(user_id: int) -> Session:
    sess = _sessions.get(user_id)
    if not sess:
        # 초기 스택에 루트 메뉴를 올려둠
        sess = Session(stack=[Frame(menu_id=tree['id'], cursor=0)])
        _sessions[user_id] = sess
    return sess

# 메뉴 렌더링
def render_menu(menu_id: int, cursor: int) -> str:
    opts = menu_tree[menu_id]['options']
    lines = []
    for idx, child in enumerate(opts):
        name = menu_tree[child]['name']
        prefix = '>' if idx == cursor else '  '
        lines.append(f"{prefix} {name}")
    return "\n".join(lines)

def move_up(event: ChatContext, count: int):
    user = event.sender.id
    sess = get_session(user)
    if sess.mode == "default":
        frame = sess.stack[-1]
        opts = menu_tree[frame.menu_id]['options']
        frame.cursor = (frame.cursor - count) % len(opts)
        event.reply(render_menu(frame.menu_id, frame.cursor))




def move_down(event: ChatContext, count: int):
    user = event.sender.id
    sess = get_session(user)
    if sess.mode == "default":
        frame = sess.stack[-1]
        opts = menu_tree[frame.menu_id]['options']
        frame.cursor = (frame.cursor + count) % len(opts)
        event.reply(render_menu(frame.menu_id, frame.cursor))

def go_back(event: ChatContext):
    user = event.sender.id
    sess = get_session(user)
    if sess.mode == "shop": sess.mode = "default"
    if sess.mode == "inventory": sess.mode = "default"
    if len(sess.stack) > 1:
        sess.stack.pop()
    top = sess.stack[-1]
    event.reply(render_menu(top.menu_id, top.cursor))

def confirm(event: ChatContext, kl):
    user = event.sender.id
    sess = get_session(user)
    frame = sess.stack[-1]
    opts = menu_tree[frame.menu_id]['options']
    selected = opts[frame.cursor]

    if sess.mode == "shop":
        match = re.search(r"!선택\s+(\d+)", event.message.msg)

        if match:
            frame = sess.shop_stack[-1]
            ids = frame['data']
            add_inventory(sess,ids[int(match[1]) - 1])
            code = get_avatar(sess.inventory_stack)
            img = get_avatar_img(code)
            kl.send(
                receiver_name=event.room.name,
                template_id=15476,
                template_args={
                    "${TH_IMAGE_URL_0}": img
                },
            )
            sess.mode = "default"

        return

    if menu_tree[selected]['options']:
        sess.stack.append(Frame(menu_id=selected, cursor=0))
        event.reply(render_menu(selected, 0))
    else:
        name = menu_tree[selected]['name']

        if name == "초기화":
            sess.inventory_stack = {}
            code = get_avatar({})
            img = get_avatar_img(code)
            kl.send(
                receiver_name=event.room.name,
                template_id=15476,
                template_args={
                    "${TH_IMAGE_URL_0}": img
                },
            )
            return None

        # TODO: 실제 로직
        # 선택 완료 시 스택 리셋
        sess.stack = [Frame(menu_id=tree['id'], cursor=0)]
        event.reply(f"✅ {name} 선택 완료.\n 원하는 아이템을 골라주세요.(!선택 <아이템 번호>)")
        img = get_store(str(name), 0, sess)
        buf = io.BytesIO()
        img.save(buf, format="PNG")
        buf.seek(0)
        return event.reply_media([buf])

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

def add_inventory(sess:Session, data:dict):
    type_name = slot_name[data["slot"]]
    sess.inventory_stack[type_name] = data["code"]

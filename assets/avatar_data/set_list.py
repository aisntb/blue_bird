import json
import os
import shutil

# 경로 설정 -------------------------------------------------------
json_path = r"망토.json"
image_dir = r"C:\Users\hayeo\PycharmProjects\PythonProject1\assets\avatar\망토"

# 1) 원본 JSON 로드 ----------------------------------------------
with open(json_path, "r", encoding="utf-8") as f:
    data = json.load(f)

items = data.get("itemList", [])

# 2) 존재하는 이미지만 필터 ---------------------------------------
kept_items = []
for item in items:
    code = item.get("code")
    if not isinstance(code, int):
        continue                         # 잘못된 항목은 건너뜀

    filename = f"{code:08d}.png"         # 00068720.png 형태
    img_path = os.path.join(image_dir, filename)

    if os.path.isfile(img_path):
        kept_items.append(item)
    else:
        print(f"❌ 이미지 없음 → 제거: {filename}")

# 3) JSON 갱신 ----------------------------------------------------
data["itemList"] = kept_items

# 4) 안전을 위해 원본 백업 후 저장 --------------------------------
backup = json_path + ".bak"
shutil.copyfile(json_path, backup)
print(f"백업 저장: {backup}")

with open(json_path, "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print(f"✅ 완료 — 남은 아이템 수: {len(kept_items)}")

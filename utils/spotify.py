import requests
import time
import base64
import json

# === Spotify App Credentials ===
CLIENT_ID = ''
CLIENT_SECRET = ''
REDIRECT_URI = 'http://localhost:3000'

# === 사용자로부터 미리 받아서 저장한 refresh_token ===
REFRESH_TOKEN = '-R2jeNDOFY0a3-QoLTCjV0u1cMqg3ImGKc-c3xgiPKR-cDe3AR6XPsXRUZ08kV2MQXS9L7oJJ_7PHI22cVptnQ0zM_pE'

# === Access Token 상태 ===
access_token = None
access_token_expires_at = 0


def get_access_token():
    global access_token, access_token_expires_at

    if access_token and time.time() < access_token_expires_at:
        return access_token

    print('[!] Access token expired or not available. Refreshing...')

    auth_str = f"{CLIENT_ID}:{CLIENT_SECRET}"
    b64_auth_str = base64.b64encode(auth_str.encode()).decode()

    response = requests.post(
        'https://accounts.spotify.com/api/token',
        data={
            'grant_type': 'refresh_token',
            'refresh_token': REFRESH_TOKEN,
        },
        headers={
            'Authorization': f'Basic {b64_auth_str}',
            'Content-Type': 'application/x-www-form-urlencoded',
        }
    )

    if response.status_code != 200:
        raise Exception(f"Failed to refresh token: {response.text}")

    token_data = response.json()
    access_token = token_data['access_token']
    expires_in = token_data.get('expires_in', 3600)
    access_token_expires_at = time.time() + expires_in - 10  # 여유 10초

    return access_token


def search_track(query, limit=1):
    token = get_access_token()

    response = requests.get(
        'https://api.spotify.com/v1/search',
        headers={
            'Authorization': f'Bearer {token}',
        },
        params={
            'q': query,
            'type': 'track',
            'limit': limit,
        }
    )

    if response.status_code != 200:
        raise Exception(f"Search failed: {response.text}")

    results = response.json()
    return results.get('tracks', {}).get('items', [])


# === 테스트 ===
if __name__ == '__main__':
    keyword = input("검색할 노래 제목: ")
    results = search_track(keyword)
    for i, track in enumerate(results):
        print(f"{i + 1}. {track['name']} - {track['artists'][0]['name']}")
        print(f"   URL: {track['external_urls']['spotify']}")

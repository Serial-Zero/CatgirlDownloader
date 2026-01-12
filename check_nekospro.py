import requests

try:
    print("Testing NekosPro NSFW Neko...")
    response = requests.get("https://api.nekos.pro/nsfw/neko", timeout=10)
    print(f"Status: {response.status_code}")
    print(f"Content: {response.text[:200]}") # First 200 chars
except Exception as e:
    print(f"NekosPro Failed: {e}")

import requests

try:
    response = requests.get("https://api.waifu.im/tags")
    response.raise_for_status()
    data = response.json()
    print("Versatile:", data.get("versatile", []))
    print("NSFW:", data.get("nsfw", []))
except Exception as e:
    print(e)

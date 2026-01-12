import requests
from typing import List

class Provider:
    def fetch(self, limit: int, cat: str, nsfw: bool = False) -> List[str]:
        raise NotImplementedError

class Nekos(Provider):
    def fetch(self, limit: int, cat: str = "neko", nsfw: bool = False) -> List[str]:
        if nsfw: 
            return []
            
        urls = []
        ep = f"https://nekos.best/api/v2/{cat}"
        
        while len(urls) < limit:
            count = min(limit - len(urls), 20)
            try:
                res = requests.get(ep, params={"amount": count}, timeout=10)
                res.raise_for_status()
                data = res.json()
                
                if "results" in data:
                    urls.extend([item["url"] for item in data["results"]])
                else:
                    break
            except Exception:
                break
                
        return urls[:limit]

class Waifu(Provider):
    def fetch(self, limit: int, cat: str, nsfw: bool = False) -> List[str]:
        urls = []
        ep = "https://api.waifu.im/search"
        
        tag_map = {
            "waifu": "waifu",
            "maid": "maid",
            "uniform": "uniform",
            "selfies": "selfies",
            "ass": "ass",
            "hentai": "hentai",
            "milf": "milf",
            "oral": "oral",
            "paizuri": "paizuri",
            "ecchi": "ecchi",
            "ero": "ero"
        }
        
        tag = tag_map.get(cat.lower(), cat.lower())
        
        while len(urls) < limit:
            count = min(limit - len(urls), 30)
            q = {
                "included_tags": [tag],
                "limit": count,
                "is_nsfw": "true" if nsfw else "false"
            }
                
            try:
                res = requests.get(ep, params=q, timeout=10)
                res.raise_for_status()
                data = res.json()
                
                if "images" in data:
                    new = data["images"]
                    if not new:
                        break
                    urls.extend([item["url"] for item in new])
                else:
                    break
                    
            except Exception:
                break
                
        return urls[:limit]

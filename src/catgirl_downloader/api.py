import requests
from typing import List

class CatgirlProvider:
    """Interface for fetching catgirl image URLs."""
    def get_images(self, amount: int, category: str, nsfw: bool = False) -> List[str]:
        raise NotImplementedError

class NekosBestProvider(CatgirlProvider):
    """Provider for nekos.best API (SFW Only)."""
    def get_images(self, amount: int, category: str = "neko", nsfw: bool = False) -> List[str]:
        if nsfw: 
            return [] # Nekos.best is SFW only
            
        urls = []
        base_url = f"https://nekos.best/api/v2/{category}"
        
        while len(urls) < amount:
            count = min(amount - len(urls), 20)
            try:
                response = requests.get(base_url, params={"amount": count}, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if "results" in data:
                    new_urls = [item["url"] for item in data["results"]]
                    urls.extend(new_urls)
                else:
                    break
            except requests.RequestException as e:
                print(f"Error fetching data from Nekos.best: {e}")
                break
                
        return urls[:amount]

class WaifuImProvider(CatgirlProvider):
    """Provider for waifu.im API (SFW & NSFW)."""
    def get_images(self, amount: int, category: str, nsfw: bool = False) -> List[str]:
        urls = []
        base_url = "https://api.waifu.im/search"
        
        # Map nice display names to waifu.im tags
        tag_mapping = {
            # Versatile
            "waifu": "waifu",
            "maid": "maid",
            "uniform": "uniform",
            "selfies": "selfies",
            
            # NSFW
            "ass": "ass",
            "hentai": "hentai",
            "milf": "milf",
            "oral": "oral",
            "paizuri": "paizuri",
            "ecchi": "ecchi",
            "ero": "ero"
        }
        
        tag = tag_mapping.get(category.lower(), category.lower())
        
        while len(urls) < amount:
            count = min(amount - len(urls), 30) # Waifu.im limit is 30
            params = {
                "included_tags": [tag],
                "limit": count,
            }
            
            # Explicitly set is_nsfw based on user mode
            if nsfw:
                params["is_nsfw"] = "true"
            else:
                params["is_nsfw"] = "false"
                
            try:
                response = requests.get(base_url, params=params, timeout=10)
                response.raise_for_status()
                data = response.json()
                
                if "images" in data:
                    new_items = data["images"]
                    if not new_items:
                        break
                        
                    new_urls = [item["url"] for item in new_items]
                    urls.extend(new_urls)
                else:
                    break
                    
            except requests.RequestException as e:
                print(f"Error fetching data from Waifu.im: {e}")
                break
                
        return urls[:amount]

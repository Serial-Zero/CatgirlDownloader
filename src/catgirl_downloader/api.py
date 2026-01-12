import requests
from typing import List, Dict

class Provider:
    def fetch(self, limit: int, cat: str, nsfw: bool = False) -> List[str]:
        raise NotImplementedError

class Nekos(Provider):
    def fetch(self, limit: int, cat: str = "neko", nsfw: bool = False) -> List[str]:
        if nsfw: return []
        urls = []
        ep = f"https://nekos.best/api/v2/{cat}"
        while len(urls) < limit:
            try:
                res = requests.get(ep, params={"amount": min(limit - len(urls), 20)}, timeout=10)
                res.raise_for_status()
                data = res.json()
                if "results" in data:
                    urls.extend([i["url"] for i in data["results"]])
                else: break
            except Exception: break
        return urls[:limit]

class Waifu(Provider):
    def fetch(self, limit: int, cat: str, nsfw: bool = False) -> List[str]:
        urls = []
        ep = "https://api.waifu.im/search"
        tag_map = {"waifu": "waifu", "maid": "maid", "uniform": "uniform", "selfies": "selfies", 
                  "ass": "ass", "hentai": "hentai", "milf": "milf", "oral": "oral", 
                  "paizuri": "paizuri", "ecchi": "ecchi", "ero": "ero"}
        tag = tag_map.get(cat.lower(), cat.lower())
        
        while len(urls) < limit:
            q = {"included_tags": [tag], "limit": min(limit - len(urls), 30), "is_nsfw": str(nsfw).lower()}
            try:
                res = requests.get(ep, params=q, timeout=10)
                res.raise_for_status()
                data = res.json()
                if "images" in data:
                    new = [i["url"] for i in data["images"]]
                    if not new: break
                    urls.extend(new)
                else: break
            except Exception: break
        return urls[:limit]

class WaifuPics(Provider):
    def fetch(self, limit: int, cat: str, nsfw: bool = False) -> List[str]:
        urls = []
        mode = "nsfw" if nsfw else "sfw"
        ep = f"https://api.waifu.pics/many/{mode}/{cat}"
        
        while len(urls) < limit:
            try:
                res = requests.post(ep, json={"exclude": []}, timeout=10)
                res.raise_for_status()
                data = res.json()
                if "files" in data:
                    new = data["files"]
                    if not new: break
                    urls.extend(new)
                else: break
            except Exception: break
        return urls[:limit]

class PurrBot(Provider):
    def fetch(self, limit: int, cat: str, nsfw: bool = False) -> List[str]:
        urls = []
        mode = "nsfw" if nsfw else "sfw"
        # PurrBot categories need mapping sometimes, but basic ones work
        ep = f"https://purrbot.site/api/img/{mode}/{cat}/img"
        
        # Sequential due to no bulk endpoint
        for _ in range(limit):
            try:
                res = requests.get(ep, timeout=5)
                res.raise_for_status()
                data = res.json()
                if not data.get("error") and "link" in data:
                    urls.append(data["link"])
            except Exception: pass
        return urls

class Manager:
    def __init__(self):
        self.provs = {
            "nekos": Nekos(),
            "waifu": Waifu(),
            "pics": WaifuPics(),
            "purr": PurrBot()
        }
        
        # Map categories to (ProviderKey, ApiCategoryName)
        self.map_sfw = {
            "Neko": ("nekos", "neko"),
            "Kitsune": ("nekos", "kitsune"),
            "Husbando": ("nekos", "husbando"),
            "Waifu": ("waifu", "waifu"),
            "Maid": ("waifu", "maid"),
            "Uniform": ("waifu", "uniform"),
            "Selfies": ("waifu", "selfies"),
            "Shinobu": ("pics", "shinobu"),
            "Megumin": ("pics", "megumin"),
            "Bully": ("pics", "bully"),
            "Cuddle": ("pics", "cuddle"),
            "Cry": ("pics", "cry"),
            "Hug": ("pics", "hug"),
            "Awoo": ("pics", "awoo"),
            "Kiss": ("pics", "kiss"),
            "Lick": ("pics", "lick"),
            "Pat": ("pics", "pat"),
            "Smug": ("pics", "smug"),
            "Bonk": ("pics", "bonk"),
            "Yeet": ("pics", "yeet"),
            "Blush": ("pics", "blush"),
            "Smile": ("pics", "smile"),
            "Wave": ("pics", "wave"),
            "Highfive": ("pics", "highfive"),
            "Handhold": ("pics", "handhold"),
            "Nom": ("pics", "nom"),
            "Bite": ("pics", "bite"),
            "Glomp": ("pics", "glomp"),
            "Slap": ("pics", "slap"),
            "Kill": ("pics", "kill"),
            "Kick": ("pics", "kick"),
            "Happy": ("pics", "happy"),
            "Wink": ("pics", "wink"),
            "Poke": ("pics", "poke"),
            "Dance": ("pics", "dance"),
            "Cringe": ("pics", "cringe"),
            "Senko": ("purr", "senko"),
            "Holo": ("purr", "holo"),
        }
        
        self.map_nsfw = {
            "Waifu": ("waifu", "waifu"), 
            "Maid": ("waifu", "maid"),
            "Ass": ("waifu", "ass"),
            "Hentai": ("waifu", "hentai"),
            "Milf": ("waifu", "milf"),
            "Oral": ("waifu", "oral"),
            "Paizuri": ("waifu", "paizuri"),
            "Ecchi": ("waifu", "ecchi"),
            "Ero": ("waifu", "ero"),
            "Neko": ("pics", "neko"), 
            "Trap": ("pics", "trap"), 
            "Blowjob": ("pics", "blowjob"),
            "Yuri": ("purr", "yuri")
        }

    def get_opts(self, nsfw):
        return sorted(list(self.map_nsfw.keys() if nsfw else self.map_sfw.keys()))

    def get_urls(self, cat, nsfw, limit):
        m = self.map_nsfw if nsfw else self.map_sfw
        if cat not in m: return []
        
        pkey, tag = m[cat]
        return self.provs[pkey].fetch(limit, tag, nsfw)

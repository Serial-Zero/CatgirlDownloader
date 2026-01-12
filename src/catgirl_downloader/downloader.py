import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

class Downloader:
    def __init__(self, dest: str, threads: int = 10):
        self.dest = Path(dest)
        self.threads = threads
        self.dest.mkdir(parents=True, exist_ok=True)

    def _fetch(self, url: str) -> bool:
        try:
            name = url.split('/')[-1]
            if '?' in name:
                name = name.split('?')[0]
            
            if not name:
                return False

            fp = self.dest / name
            
            if fp.exists():
                return True
                
            res = requests.get(url, timeout=15)
            res.raise_for_status()
            
            with open(fp, 'wb') as f:
                f.write(res.content)
            return True
        except Exception:
            return False

    def run(self, urls: list[str]):
        if not urls:
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as prog:
            task = prog.add_task(f"[bold pink1]Downloading {len(urls)} files...", total=len(urls))
            
            with ThreadPoolExecutor(max_workers=self.threads) as exe:
                futs = [exe.submit(self._fetch, url) for url in urls]
                
                for _ in as_completed(futs):
                    prog.advance(task)

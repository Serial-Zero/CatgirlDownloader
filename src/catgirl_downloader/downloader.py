import os
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from rich.progress import Progress, SpinnerColumn, BarColumn, TextColumn

class Downloader:
    def __init__(self, dest_dir: str, max_workers: int = 10):
        self.dest_dir = Path(dest_dir)
        self.max_workers = max_workers
        self.dest_dir.mkdir(parents=True, exist_ok=True)

    def _download_single(self, url: str) -> bool:
        """Download a single file helper."""
        try:
            # Extract filename from URL
            filename = url.split('/')[-1]
            if '?' in filename:
                filename = filename.split('?')[0]
            
            if not filename:
                return False

            filepath = self.dest_dir / filename
            
            # Skip if already exists
            if filepath.exists():
                return True
                
            response = requests.get(url, timeout=15)
            response.raise_for_status()
            
            with open(filepath, 'wb') as f:
                f.write(response.content)
            return True
        except Exception as e:
            # Silent fail allows the progress bar to continue, but ideally we'd log errors
            return False

    def download_images(self, urls: list[str]):
        """Download multiple images in parallel with a progress bar."""
        if not urls:
            return

        with Progress(
            SpinnerColumn(),
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TextColumn("[progress.percentage]{task.percentage:>3.0f}%"),
        ) as progress:
            task = progress.add_task(f"[bold pink1]Downloading {len(urls)} Catgirls...", total=len(urls))
            
            with ThreadPoolExecutor(max_workers=self.max_workers) as executor:
                # Submit all tasks
                futures = [executor.submit(self._download_single, url) for url in urls]
                
                # As they complete, update progress
                for _ in as_completed(futures):
                    progress.advance(task)

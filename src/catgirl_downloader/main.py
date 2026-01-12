import click
import questionary
from rich.console import Console
from rich.panel import Panel
from .api import Nekos, Waifu
from .downloader import Downloader
import os
from pathlib import Path

console = Console()

def menu():
    console.print(Panel.fit("[bold pink1]Welcome to Catgirl Downloader[/bold pink1]", border_style="pink1"))

    while True:
        mode = questionary.select(
            "Select Mode:",
            choices=["SFW", "NSFW", "Exit"],
            style=questionary.Style([('qmark', 'fg:#ff00ff bold'),('question', 'bold'),('answer', 'fg:#00ff00 bold')])
        ).ask()
        
        if not mode or mode == "Exit":
            console.print("[yellow]Goodbye![/yellow]")
            break
            
        is_nsfw = "NSFW" in mode

        if is_nsfw:
            opts = ["Waifu", "Maid", "Ass", "Hentai", "Milf", "Oral", "Paizuri", "Ecchi", "Ero"]
        else:
            opts = ["Neko", "Kitsune", "Waifu", "Maid", "Husbando"]
            
        opts.append("Back")

        cat = questionary.select("What would you like to download?", choices=opts).ask()

        if not cat or cat == "Back":
            continue

        raw = cat
        
        limit_str = questionary.text(
            f"How many {raw} images?",
            default="10",
            validate=lambda x: x.isdigit() and int(x) > 0 or "Positive integer required."
        ).ask()
        
        if not limit_str: continue
        limit = int(limit_str)

        dest = questionary.text(
            "Save location?",
            default="downloads"
        ).ask()

        if not dest: continue
        
        sub = "nsfw" if is_nsfw else "sfw"
        out = Path(dest) / sub / raw.lower()

        if questionary.confirm(f"Download {limit} images to '{out}'?").ask():
            process(limit, str(out), raw, is_nsfw)
        
        if not questionary.confirm("Download more?").ask():
            console.print("[yellow]See you next time![/yellow]")
            break

def process(limit, out, cat, nsfw):
    slug = cat.lower()
    sfw_nekos = ["neko", "kitsune", "husbando"]
    
    if not nsfw and slug in sfw_nekos:
        prov = Nekos()
        name = "Nekos.best"
        tag = slug
    else:
        prov = Waifu()
        name = "Waifu.im"
        tag = slug
    
    with console.status(f"[bold cyan]Fetching metadata from {name}...[/bold cyan]"):
        urls = prov.fetch(limit, cat=tag, nsfw=nsfw)
    
    if not urls:
        console.print("[bold red]Error:[/bold red] No URLs found.")
        return

    console.print(f"Found [bold green]{len(urls)}[/bold green] images.")

    dl = Downloader(out)
    dl.run(urls)
    
    console.print(f"[bold green]Done![/bold green] Saved to [underline]{os.path.abspath(out)}[/underline]\n")

@click.command()
def main():
    try:
        menu()
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted.[/red]")

if __name__ == '__main__':
    main()

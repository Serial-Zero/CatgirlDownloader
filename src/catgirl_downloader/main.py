import click
import questionary
from rich.console import Console
from rich.panel import Panel
from .api import Manager
from .downloader import Downloader
import os
from pathlib import Path

console = Console()
api = Manager()

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

        opts = api.get_opts(is_nsfw)
        opts.append("Back")

        cat = questionary.select("What type?", choices=opts).ask()

        if not cat or cat == "Back":
            continue

        limit_str = questionary.text(
            f"How many {cat} images?",
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
        out = Path(dest) / sub / cat.lower()

        if questionary.confirm(f"Download {limit} images to '{out}'?").ask():
            process(limit, str(out), cat, is_nsfw)
        
        if not questionary.confirm("Download more?").ask():
            console.print("[yellow]See you next time![/yellow]")
            break

def process(limit, out, cat, nsfw):
    with console.status(f"[bold cyan]Fetching metadata...[/bold cyan]"):
        urls = api.get_urls(cat, nsfw, limit)
    
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

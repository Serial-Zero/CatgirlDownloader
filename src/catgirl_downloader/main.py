import click
import questionary
from rich.console import Console
from rich.panel import Panel
from .api import NekosBestProvider, WaifuImProvider
from .downloader import Downloader
import os
from pathlib import Path

console = Console()

def interactive_mode():
    """Runs the interactive TUI."""
    console.print(Panel.fit("[bold pink1]Welcome to Catgirl Downloader[/bold pink1]", border_style="pink1"))

    while True:
        # 0. Select Mode (SFW/NSFW)
        mode = questionary.select(
            "Select Mode:",
            choices=[
                "SFW (Safe for Work)",
                "NSFW (Not Safe for Work)",
                "Exit"
            ],
            style=questionary.Style([('qmark', 'fg:#ff00ff bold'),('question', 'bold'),('answer', 'fg:#00ff00 bold')])
        ).ask()
        
        if not mode or mode == "Exit":
            console.print("[yellow]Goodbye![/yellow]")
            break
            
        is_nsfw = "NSFW" in mode

        # 1. Select Category based on mode
        if is_nsfw:
            # Waifu.im NSFW tags
            choices = ["Waifu", "Maid", "Ass", "Hentai", "Milf", "Oral", "Paizuri", "Ecchi", "Ero"]
        else:
            # Nekos.best SFW categories (plus some Waifu.im ones if needed, but sticky to Neko)
            # Neko/Kitsune use NekosBest
            # Waifu/Maid use WaifuIm
            choices = ["Neko", "Kitsune", "Waifu", "Maid", "Husbando"]
            
        choices.append("Back")

        category_display = questionary.select(
            "What would you like to download?",
            choices=choices
        ).ask()

        if not category_display or category_display == "Back":
            continue

        # Extract actual API category slug
        raw_category = category_display
        
        # 2. Ask for Amount
        amount_str = questionary.text(
            f"How many {raw_category} images do you want?",
            default="10",
            validate=lambda text: text.isdigit() and int(text) > 0 or "Please enter a valid positive integer."
        ).ask()
        
        if not amount_str: continue
        amount = int(amount_str)

        # 3. Ask for Output Directory
        output_dir = questionary.text(
            "Where should they be saved? (A subfolder will be created)",
            default="downloads"
        ).ask()

        if not output_dir: continue
        
        # Create separate folder for category and mode
        mode_dir = "nsfw" if is_nsfw else "sfw"
        final_output_dir = Path(output_dir) / mode_dir / raw_category.lower()

        # 4. Confirm execution
        confirm = questionary.confirm(f"Ready to download {amount} images to '{final_output_dir}'?").ask()
        
        if confirm:
            _run_download(amount, str(final_output_dir), raw_category, is_nsfw)
        
        # 5. Loop?
        if not questionary.confirm("Do you want to download something else?").ask():
            console.print("[yellow]See you next time![/yellow]")
            break

def _run_download(amount, output, category, nsfw):
    """Helper to run the download logic."""
    
    # Choose provider logic
    cat_lower = category.lower()
    
    # Nekos.best only supports specific SFW categories
    nekos_best_cats = ["neko", "kitsune", "husbando"]
    
    if not nsfw and cat_lower in nekos_best_cats:
        provider = NekosBestProvider()
        provider_name = "Nekos.best (SFW)"
        api_category = cat_lower # internal name matches
    else:
        # Everything else (NSFW, or SFW Waifu/Maid) goes to Waifu.im
        provider = WaifuImProvider()
        provider_name = "Waifu.im"
        api_category = cat_lower
    
    with console.status(f"[bold cyan]Fetching metadata from {provider_name}...[/bold cyan]"):
        urls = provider.get_images(amount, category=api_category, nsfw=nsfw)
    
    if not urls:
        console.print("[bold red]Error:[/bold red] Could not fetch image URLs. API might be down or category empty.")
        return

    console.print(f"Found [bold green]{len(urls)}[/bold green] images.")

    downloader = Downloader(output)
    downloader.download_images(urls)
    
    console.print(f"[bold green]Done![/bold green] Saved to [underline]{os.path.abspath(output)}[/underline]\n")

@click.command()
def main():
    """
    Catgirl Downloader: Interactive CLI tool.
    """
    try:
        interactive_mode()
    except KeyboardInterrupt:
        console.print("\n[red]Interrupted by user.[/red]")

if __name__ == '__main__':
    main()

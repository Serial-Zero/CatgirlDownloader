# Catgirl Downloader

A clean, modular Python script to download high-quality catgirl (and other) images. Now featuring an interactive CLI, SFW & NSFW modes, and automatic organization.

## Features
- **Interactive CLI**: Easy-to-use menu system driven by `questionary`.
- **Dual Modes**: 
  - **SFW**: Neko, Kitsune, Waifu, Maid, Husbando.
  - **NSFW**: Waifu, Maid, Ass, Hentai, Milf, Oral, Paizuri, Ecchi, Ero.
- **Smart Sorting**: Images are automatically saved to `downloads/{mode}/{category}/`.
- **Multi-API Support**: seamlessly integrates **[nekos.best](https://nekos.best)** and **[waifu.im](https://waifu.im)**.

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Simply run the module to start the interactive wizard:

```bash
python -m src.catgirl_downloader.main
```

Follow the on-screen prompts:
1. **Select Mode**: Choose between SFW or NSFW.
2. **Select Category**: Browse available categories for your chosen mode.
3. **Amount**: Enter how many images you want.
4. **Output Directory**: Choose a base folder (default is `downloads`).

### Directory Structure
The tool organizes downloads automatically:
```
downloads/
├── sfw/
│   ├── neko/
│   └── waifu/
└── nsfw/
    ├── hentai/
    └── ass/
```

## APIs Used
- **Nekos.best API**: Primary source for SFW Nekos and Kitsunes.
- **Waifu.im API**: Powers NSFW content and additional SFW categories.

# Catgirl Downloader

A clean, modular Python script to download high-quality catgirl images using the [nekos.best](https://nekos.best) API.

## Structure
This project follows a standard Google-style Python project structure:
- `src/`: Source code package
- `tests/`: Unit tests (placeholder)
- `requirements.txt`: Dependencies

## Installation

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the downloader module:

```bash
python -m src.catgirl_downloader.main --amount 20 --output my_catgirls
```

### Options
- `--amount` / `-n`: Number of images to download (default: 10)
- `--output` / `-o`: Output directory (default: `downloads`)

## APIs Used
- **Nekos.best API**: High quality, SFW catgirl images.

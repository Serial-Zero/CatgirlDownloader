import unittest
from src.catgirl_downloader.api import NekosBestProvider, WaifuPicsProvider

class TestCatgirlDownloader(unittest.TestCase):
    def test_nekos_provider_init(self):
        """Test that the NekosBest provider initializes correctly."""
        provider = NekosBestProvider()
        self.assertIsNotNone(provider)

    def test_waifupics_provider_init(self):
        """Test that the WaifuPics provider initializes correctly."""
        provider = WaifuPicsProvider()
        self.assertIsNotNone(provider)

if __name__ == '__main__':
    unittest.main()

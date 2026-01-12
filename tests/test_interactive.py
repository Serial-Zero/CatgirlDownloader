import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.catgirl_downloader.main import interactive_mode

class TestInteractive(unittest.TestCase):
    @patch('src.catgirl_downloader.main.questionary')
    @patch('src.catgirl_downloader.main._run_download')
    def test_interactive_flow_sfw_neko(self, mock_run, mock_quest):
        """Test SFW Neko (uses NekosBest)."""
        mock_quest.select.return_value.ask.side_effect = ["SFW (Safe for Work)", "Neko"]
        mock_quest.text.return_value.ask.side_effect = ["5", "test_out"]
        mock_quest.confirm.return_value.ask.side_effect = [True, False]
        
        interactive_mode()
        
        expected_path = str(Path("test_out") / "sfw" / "neko")
        mock_run.assert_called_with(5, expected_path, "Neko", False)

    @patch('src.catgirl_downloader.main.questionary')
    @patch('src.catgirl_downloader.main._run_download')
    def test_interactive_flow_nsfw_maid(self, mock_run, mock_quest):
        """Test NSFW Maid (uses WaifuIm)."""
        mock_quest.select.return_value.ask.side_effect = ["NSFW (Not Safe for Work)", "Maid"]
        mock_quest.text.return_value.ask.side_effect = ["10", "test_out"]
        mock_quest.confirm.return_value.ask.side_effect = [True, False]
        
        interactive_mode()
        
        expected_path = str(Path("test_out") / "nsfw" / "maid")
        # Note: category passed is "Maid" (display name from list)
        mock_run.assert_called_with(10, expected_path, "Maid", True)

if __name__ == '__main__':
    unittest.main()

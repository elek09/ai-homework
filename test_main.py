import unittest
from unittest.mock import MagicMock, patch
from main import is_json, process_data
import time


class TestAnswerProcessing(unittest.TestCase):

    @patch('main.receive_data')
    def test_process_data(self, mock_receive_data):
        mock_receive_data.side_effect = [
            {"site": "stackoverflow", "creationdate": time.time()},
            {"site": "datascience", "creationdate": time.time()},
            {"site": "cooking", "creationdate": time.time()},
            None
        ]

        sock = MagicMock()

        with patch('main.time.sleep', return_value=None):
            process_data(sock, max_iterations=3)  # Set a limit on iterations

    def test_is_json(self):
        valid_json = '{"site": "stackoverflow"}'
        invalid_json = 'Non-JSON line'

        self.assertTrue(is_json(valid_json))
        self.assertFalse(is_json(invalid_json))


if __name__ == '__main__':
    unittest.main()

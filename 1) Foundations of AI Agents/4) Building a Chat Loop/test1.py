import unittest
from unittest.mock import patch
from io import StringIO
import sys

class TestAssistantCLI(unittest.TestCase):
    @patch('builtins.input', side_effect=["What is AI?", "Tell me a joke.", "exit"])
    def test_cli_loop_responses(self, mock_input):
        from solution import main

        captured_output = StringIO()
        sys.stdout = captured_output

        main()

        sys.stdout = sys.__stdout__
        output = captured_output.getvalue()

        # Print the full stdout (including user inputs and assistant answers)
        print("Captured stdout for test_cli_loop_responses:\n", output)

        self.assertIn("Goodbye", output)

if __name__ == '__main__':
    unittest.main()
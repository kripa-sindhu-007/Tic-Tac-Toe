import unittest
import importlib
from tkinter import StringVar # Needed for mocking game_mode and difficulty

# Import functions to be tested
from tic_tac_toe import is_winner, is_board_full
# computer_move will be accessed via the reloaded module in setUp

# MockButton Class
class MockButton:
    def __init__(self):
        self.text = ""
        self.state = "normal" # Tkinter's NORMAL constant is "normal"
        self.fg = "" # Foreground color
        self.bg = "" # Background color

    def config(self, text=None, state=None, fg=None, bg=None):
        if text is not None:
            self.text = text
        if state is not None:
            self.state = state
        if fg is not None:
            self.fg = fg
        if bg is not None:
            self.bg = bg

    def cget(self, option): # Mock cget if any part of your code uses it on buttons
        if option == "text":
            return self.text
        elif option == "state":
            return self.state
        elif option == "fg":
            return self.fg
        elif option == "bg":
            return self.bg
        return None

# MockStatusLabel Class
class MockStatusLabel:
    def __init__(self):
        self.text = ""

    def config(self, text):
        self.text = text # Just store the text for potential assertions if needed

class TestTicTacToeLogic(unittest.TestCase):

    def setUp(self):
        # Reload tic_tac_toe module to reset its state as much as possible
        # This is crucial because tic_tac_toe.py uses global variables extensively.
        import tic_tac_toe # Import here to use the reloaded version
        importlib.reload(tic_tac_toe)
        self.ttt = tic_tac_toe

        # Initialize/mock all necessary global variables from tic_tac_toe
        self.ttt.board = [""] * 9
        self.ttt.buttons = [MockButton() for _ in range(9)] # Use MockButton
        self.ttt.clicked = True  # Default: X's turn
        self.ttt.count = 0
        self.ttt.winner = False

        # Mock Tkinter StringVars for game_mode and difficulty
        self.ttt.game_mode = StringVar()
        self.ttt.difficulty = StringVar()
        self.ttt.game_mode.set("PvC") # Default for AI tests
        self.ttt.difficulty.set("easy") # Default difficulty

        # Mock UI elements that AI or its helper functions might interact with minimally
        self.ttt.status_label = MockStatusLabel()

        # Mock color constants if they are used by logic being tested (e.g. computer_move setting button colors)
        # These are defined in tic_tac_toe.py but good to have them on self.ttt if needed for clarity
        # or if there's any chance they might not be loaded when tests run in some environments.
        if not hasattr(self.ttt, 'X_COLOR'): self.ttt.X_COLOR = "#e74c3c"
        if not hasattr(self.ttt, 'O_COLOR'): self.ttt.O_COLOR = "#f1c40f"
        if not hasattr(self.ttt, 'TEXT_COLOR'): self.ttt.TEXT_COLOR = "#ecf0f1"
        if not hasattr(self.ttt, 'WIN_COLOR'): self.ttt.WIN_COLOR = "#2ecc71"

        # The is_winner function (imported directly) and check_won (called by computer_move)
        # define winning_lines locally, so no need to mock self.ttt.winning_lines.
        # Ensure disable_all is callable if check_won calls it (it's a global func in ttt)
        # self.ttt.disable_all = lambda: None # Mock if it causes issues; for now, assume it's fine.
        # self.ttt.update_status_label = lambda message: None # Mock if needed

    # --- Tests for is_winner ---
    def test_is_winner_rows_X(self):
        board = ["X", "X", "X", "", "", "", "", "", ""]
        self.assertTrue(is_winner(board, "X"))

    def test_is_winner_rows_O(self):
        board = ["", "", "", "O", "O", "O", "", "", ""]
        self.assertTrue(is_winner(board, "O"))

    def test_is_winner_cols_X(self):
        board = ["X", "", "", "X", "", "", "X", "", ""]
        self.assertTrue(is_winner(board, "X"))

    def test_is_winner_cols_O(self):
        board = ["", "O", "", "", "O", "", "", "O", ""]
        self.assertTrue(is_winner(board, "O"))

    def test_is_winner_diag1_X(self):
        board = ["X", "", "", "", "X", "", "", "", "X"]
        self.assertTrue(is_winner(board, "X"))

    def test_is_winner_diag2_O(self):
        board = ["", "", "O", "", "O", "", "O", "", ""]
        self.assertTrue(is_winner(board, "O"))

    def test_is_winner_no_winner_full_board(self):
        board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]
        self.assertFalse(is_winner(board, "X"))
        self.assertFalse(is_winner(board, "O"))

    def test_is_winner_incomplete_no_winner(self):
        board = ["X", "O", "", "X", "", "", "", "", ""]
        self.assertFalse(is_winner(board, "X"))
        self.assertFalse(is_winner(board, "O"))

    def test_is_winner_empty_board(self):
        board = [""] * 9
        self.assertFalse(is_winner(board, "X"))
        self.assertFalse(is_winner(board, "O"))

    # --- Tests for is_board_full ---
    def test_is_board_full_true(self):
        board = ["X", "O", "X", "O", "X", "O", "O", "X", "O"]
        self.assertTrue(is_board_full(board))

    def test_is_board_full_false_some_empty(self):
        board = ["X", "O", "", "O", "X", "", "O", "X", ""]
        self.assertFalse(is_board_full(board))

    def test_is_board_full_completely_empty(self):
        board = [""] * 9
        self.assertFalse(is_board_full(board))

    # --- Tests for computer_move (AI) ---
    def test_ai_easy_makes_a_move(self):
        self.ttt.clicked = False # Computer's turn (O)
        self.ttt.board = ["X", "", "", "", "", "", "", "", ""]
        self.ttt.buttons[0].text = "X" # Simulate player X's move on button
        self.ttt.count = 1
        self.ttt.difficulty.set("easy")

        self.ttt.computer_move(self.ttt.difficulty.get())

        # Check that 'O' was placed in one of the empty spots
        self.assertIn("O", [btn.text for btn in self.ttt.buttons if btn.text == "O"])
        self.assertEqual(self.ttt.board.count("O"), 1)
        self.assertEqual(self.ttt.count, 2)
        self.assertTrue(self.ttt.clicked) # Should be player X's turn again

    def test_ai_medium_wins(self):
        self.ttt.difficulty.set("medium")
        self.ttt.board = ["O", "O", "", "X", "X", "", "", "X", ""]
        # Simulate button texts based on board
        for i, mark in enumerate(self.ttt.board):
            if mark: self.ttt.buttons[i].text = mark
        self.ttt.count = 5
        self.ttt.clicked = False # Computer's turn

        self.ttt.computer_move(self.ttt.difficulty.get())

        self.assertEqual(self.ttt.board[2], "O")
        self.assertEqual(self.ttt.buttons[2].text, "O")
        self.assertTrue(self.ttt.winner) # computer_move calls check_won

    def test_ai_medium_blocks(self):
        self.ttt.difficulty.set("medium")
        self.ttt.board = ["X", "X", "", "O", "O", "", "", "", ""]
        for i, mark in enumerate(self.ttt.board):
            if mark: self.ttt.buttons[i].text = mark
        self.ttt.count = 4
        self.ttt.clicked = False

        self.ttt.computer_move(self.ttt.difficulty.get())

        self.assertEqual(self.ttt.board[2], "O") # Should block at index 2
        self.assertEqual(self.ttt.buttons[2].text, "O")
        self.assertFalse(self.ttt.winner) # Blocking move, not a winning one for O

    def test_ai_hard_takes_win(self):
        self.ttt.difficulty.set("hard")
        self.ttt.board = ["O", "O", "", "X", "X", "", "", "X", ""]
        for i, mark in enumerate(self.ttt.board):
            if mark: self.ttt.buttons[i].text = mark
        self.ttt.count = 5
        self.ttt.clicked = False

        self.ttt.computer_move(self.ttt.difficulty.get())

        self.assertEqual(self.ttt.board[2], "O")
        self.assertEqual(self.ttt.buttons[2].text, "O")
        self.assertTrue(self.ttt.winner)

    def test_ai_hard_blocks_immediate_loss(self):
        self.ttt.difficulty.set("hard")
        # Scenario: X has X X _, O has O _ O. X is about to win at board[2].
        # Computer (O) should block at board[2].
        self.ttt.board = ["X", "X", "", "O", "O", "", "", "", ""]
        for i, mark in enumerate(self.ttt.board):
            if mark: self.ttt.buttons[i].text = mark
        self.ttt.count = 4 # X, X, O, O
        self.ttt.clicked = False # O's turn (computer)

        self.ttt.computer_move(self.ttt.difficulty.get())

        self.assertEqual(self.ttt.board[2], "O", "Hard AI should block immediate loss")
        self.assertEqual(self.ttt.buttons[2].text, "O")
        self.assertFalse(self.ttt.winner) # Should be a block, not a win for O

if __name__ == '__main__':
    unittest.main()

from tkinter import *
from tkinter import messagebox
import random

window = Tk(className="Tic tac toe")

# --- UI Styling Variables ---
BG_COLOR = "#2c3e50"
BUTTON_COLOR = "#3498db"
BUTTON_ACTIVE_COLOR = "#2980b9" # Color when button is pressed
TEXT_COLOR = "#ecf0f1" # For button text
X_COLOR = "#e74c3c" # X player color
O_COLOR = "#f1c40f" # O player/computer color
WIN_COLOR = "#2ecc71" # Background for winning buttons
FONT_NAME = "Segoe UI"
FONT_SIZE_NORMAL = 24
FONT_SIZE_STATUS = 14
# --- End UI Styling Variables ---

# Game state variables
clicked = True  # True if X's turn, False if O's turn
count = 0       # Number of moves made

# Game board
board = [""] * 9  # Internal representation of the board
buttons = []      # List to store button widgets

# Game mode and difficulty
game_mode = StringVar()
difficulty = StringVar()
winner = False # Tracks if there's a winner
status_label = None # Will be initialized later

# disable button
def disable_all(): # Modified to use the buttons list
    global buttons
    for button in buttons:
        if button: # Check if button object exists
            button.config(state=DISABLED)


# winning condition
def check_won():
    global winner, board, buttons, count, game_mode # Added count and game_mode
    # winner is already global from the top of the script, but good to have here for clarity if needed.

    winning_lines = [
        (0, 1, 2), (3, 4, 5), (6, 7, 8),  # Rows
        (0, 3, 6), (1, 4, 7), (2, 5, 8),  # Columns
        (0, 4, 8), (2, 4, 6)             # Diagonals
    ]

    for line in winning_lines:
        b0, b1, b2 = line
        if board[b0] == board[b1] == board[b2] and board[b0] != "":
            player = board[b0]
            winner = True # Set global winner flag

            # Highlight winning buttons
            buttons[b0].config(bg=WIN_COLOR)
            buttons[b1].config(bg=WIN_COLOR)
            buttons[b2].config(bg=WIN_COLOR)

            # Determine win message for status label
            if game_mode.get() == "PvC":
                win_message = "Congratulations! You Won!" if player == "X" else "Game Over! Computer Won."
            else: # PvP
                win_message = f"Game Over! Player {player} Won!"

            update_status_label(win_message) # Update status label instead of messagebox
            # messagebox.showinfo("Tic Tac Toe", win_message) # Optionally keep messagebox or remove
            disable_all()
            return # Exit after a win is found

    # Tie condition: if no winner and count is 9
    if not winner and count == 9:
        tie_message = "Game Over! It's a Tie!"
        update_status_label(tie_message) # Update status label instead of messagebox
        # messagebox.showinfo("Tic Tac Toe", "It's a Tie!") # Optionally keep messagebox or remove
        disable_all()
        # No return needed here as it's the end of checks


# Buttom Click Function
def b_click(b):
    global clicked, count, board, buttons, game_mode, difficulty, winner # Added game_mode, difficulty, winner

    if winner: # If game is already over, do nothing
        return

    index = -1
    try:
        index = buttons.index(b)
    except ValueError:
        messagebox.showerror("Tic Tac Toe Error", "Button not recognized.")
        return

    if board[index] == "":
        if clicked:  # Player X's turn (always human)
            board[index] = "X"
            b.config(text="X", state=DISABLED, fg=X_COLOR) # Disable button and set X color
            count += 1
            clicked = False # Switch turn to O
            check_won()

            if not winner: # Only proceed if X's move wasn't a win/tie
                if game_mode.get() == "PvC":
                    if count < 9:
                        update_status_label("Computer 'O' is thinking...")
                        computer_move(difficulty.get())
                    # computer_move will call check_won and update status for X's turn if game continues
                else: # PvP mode
                    update_status_label("Player O's Turn")
            # If winner is True, check_won already updated the status label

        else:  # Player O's turn (only in PvP mode)
            if game_mode.get() == "PvP":
                board[index] = "O"
                b.config(text="O", state=DISABLED, fg=O_COLOR) # Disable button and set O color
                count += 1
                clicked = True # Switch turn back to X
                check_won()
                if not winner: # If O's move wasn't a win/tie
                    update_status_label("Player X's Turn")
            elif game_mode.get() == "PvC":
                 messagebox.showwarning("Tic Tac Toe", "It should be the Computer's turn.")

    else: # Spot already taken
        messagebox.showerror("Tic Tac Toe", "This spot is already taken!")
        # Optionally, re-update status to current player if error occurs
        current_player_text = "Player X's Turn"
        if game_mode.get() == "PvC" and not clicked: # Should be computer's turn but somehow X tried
             current_player_text = "Computer 'O's Turn"
        elif game_mode.get() == "PvP":
            current_player_text = "Player X's Turn" if clicked else "Player O's Turn"
        elif game_mode.get() == "PvC" and clicked: # Player X's turn in PvC
            current_player_text = "Your (X) Turn"

        if not winner : update_status_label(current_player_text)


# --- UI Helper Functions ---
def update_status_label(message):
    global status_label
    if status_label: # Check if label exists
        status_label.config(text=message)
    else:
        print(f"Status Update (label not ready): {message}") # Fallback if label not init yet

# resetting the game
def reset():
    global clicked, count, board, buttons, winner
    # b1-b9 globals are no longer needed here as buttons are managed via the list

    clicked = True
    count = 0
    winner = False # Explicitly reset winner state
    board = [""] * 9

    # Destroy old game buttons before creating new ones
    for btn in buttons:
        if btn: # Check if the object exists and is valid
            btn.destroy()
    buttons.clear() # Clear the list of button widgets

    # Create and grid new buttons
    for i in range(9):
        row, col = divmod(i, 3)
        # Create the button
        button = Button(window, text='',
                        font=(FONT_NAME, FONT_SIZE_NORMAL, "bold"),
                        bg=BUTTON_COLOR, fg=TEXT_COLOR,
                        activebackground=BUTTON_ACTIVE_COLOR,
                        activeforeground=TEXT_COLOR,
                        height=2, width=4, # Adjusted size for a more modern look
                        relief=FLAT, bd=0, state=NORMAL)
        # Assign its command using a lambda that captures the button instance
        button.config(command=lambda b=button: b_click(b))
        button.grid(row=row, column=col, padx=5, pady=5, sticky="nsew") # Added padding and sticky
        buttons.append(button) # Add new button to the global list

    # Set initial status message
    if game_mode.get() == "PvC":
        update_status_label(f"You are X. Difficulty: {difficulty.get().capitalize()}. Your turn!")
    else:
        update_status_label("Player X's Turn")

# create menu button
# This 'menu = Menu(window)' and 'window.config(menu=menu)' seems to be duplicated.
# The menu setup is already done below. Let's remove this duplicate.
# menu = Menu(window)
# window.config(menu=menu)

# Menu commands
def set_game_mode_and_reset():
    # game_mode.get() is already updated by the radiobutton's variable
    # Changing mode should reset the game.
    reset()

def set_difficulty_and_reset():
    # difficulty.get() is already updated by the radiobutton's variable
    # Only reset if in PvC mode, as difficulty is irrelevant for PvP.
    if game_mode.get() == "PvC":
        reset()

# create menu button
menu = Menu(window)
window.config(menu=menu)

# Create options in menu (renamed 'option' to 'options_menu')
options_menu = Menu(menu, tearoff=False)
menu.add_cascade(label="Options", menu=options_menu)
options_menu.add_command(label="Reset Game", command=reset)

# Game Mode submenu
game_mode_submenu = Menu(options_menu, tearoff=False)
options_menu.add_cascade(label="Game Mode", menu=game_mode_submenu)
game_mode_submenu.add_radiobutton(label="Player vs Player", variable=game_mode, value="PvP", command=set_game_mode_and_reset)
game_mode_submenu.add_radiobutton(label="Player vs Computer", variable=game_mode, value="PvC", command=set_game_mode_and_reset)

# Difficulty submenu
difficulty_submenu = Menu(options_menu, tearoff=False)
options_menu.add_cascade(label="Difficulty (PvC)", menu=difficulty_submenu)
difficulty_submenu.add_radiobutton(label="Easy", variable=difficulty, value="easy", command=set_difficulty_and_reset)
difficulty_submenu.add_radiobutton(label="Medium", variable=difficulty, value="medium", command=set_difficulty_and_reset)
difficulty_submenu.add_radiobutton(label="Hard", variable=difficulty, value="hard", command=set_difficulty_and_reset)

# Set default game mode and difficulty
game_mode.set("PvP") # Default to Player vs Player
difficulty.set("easy") # Default difficulty


# Helper functions for AI
def is_winner(current_board, player):
    # Check rows
    for i in range(0, 9, 3):
        if current_board[i] == player and current_board[i+1] == player and current_board[i+2] == player:
            return True
    # Check columns
    for i in range(3):
        if current_board[i] == player and current_board[i+3] == player and current_board[i+6] == player:
            return True
    # Check diagonals
    if current_board[0] == player and current_board[4] == player and current_board[8] == player:
        return True
    if current_board[2] == player and current_board[4] == player and current_board[6] == player:
        return True
    return False

def is_board_full(current_board):
    return "" not in current_board


def minimax(current_board, is_maximizing_player):
    # Base cases
    if is_winner(current_board, "O"): # AI is 'O'
        return 1
    if is_winner(current_board, "X"): # Player is 'X'
        return -1
    if is_board_full(current_board):
        return 0

    possible_moves = [i for i, spot in enumerate(current_board) if spot == ""]

    if is_maximizing_player: # AI 'O' turn - maximize score
        best_score = -float('inf')
        for move in possible_moves:
            temp_board = list(current_board)
            temp_board[move] = "O"
            score = minimax(temp_board, False) # Next turn is player 'X' (minimizing)
            best_score = max(best_score, score)
        return best_score
    else: # Player 'X' turn - minimize score for AI
        best_score = float('inf')
        for move in possible_moves:
            temp_board = list(current_board)
            temp_board[move] = "X"
            score = minimax(temp_board, True) # Next turn is AI 'O' (maximizing)
            best_score = min(best_score, score)
        return best_score


def computer_move(difficulty):
    global clicked, count, board, buttons, winner, game_mode # Added winner, game_mode

    # Ensure it's computer's turn (O), in PvC mode, game not over, and board not full
    if clicked is True or game_mode.get() != "PvC" or winner or count >= 9:
        return

    empty_cells = [i for i, spot in enumerate(board) if spot == ""]
    if not empty_cells:
        return # No move possible

    move_index = -1

    if difficulty == "easy":
        move_index = random.choice(empty_cells)

    elif difficulty == "medium":
        # 1. Can computer ('O') win?
        for i in empty_cells:
            temp_board = list(board) # Create a copy
            temp_board[i] = "O"
            if is_winner(temp_board, "O"):
                move_index = i
                break

        if move_index == -1:
            # 2. Can player ('X') win? Block them.
            for i in empty_cells:
                temp_board = list(board) # Create a copy
                temp_board[i] = "X"
                if is_winner(temp_board, "X"):
                    move_index = i
                    break

        if move_index == -1:
            # 3. Make a random move
            move_index = random.choice(empty_cells)

    elif difficulty == "hard":
        best_score = -float('inf')
        # move_index is already -1 by default
        for i in empty_cells:
            temp_board = list(board) # Create a copy
            temp_board[i] = "O" # Make a test move for AI
            score = minimax(temp_board, False) # Evaluate this move (next turn is player 'X')
            # temp_board[i] = "" # Undo the test move - not strictly necessary here as we use a fresh copy each time
            if score > best_score:
                best_score = score
                move_index = i
        # If all moves have negative infinity score (e.g., immediate loss), pick any valid move.
        # This can happen if minimax returns -inf for all initial moves.
        # However, standard minimax should find a move unless board is full.
        # A failsafe random move if no better move is found by minimax (should ideally not be needed if minimax is correct)
        if move_index == -1 and empty_cells: # check empty_cells to prevent error if board is full
             move_index = random.choice(empty_cells)


    # Make the chosen move if one was determined
    if move_index != -1: # Ensure a move was actually selected
        board[move_index] = "O"
        buttons[move_index].config(text="O", state=DISABLED, fg=O_COLOR) # Set O color
        count += 1
        clicked = True # Set turn back to player X
        check_won() # Check if computer's move was winning or a tie

        if not winner and count < 9 : # If game is still ongoing
            update_status_label("Your (X) Turn")

    elif not empty_cells and not winner:
        # This case should ideally be caught by check_won if count == 9
        # but as a fallback if no move was made and board is full (e.g. error in AI logic)
        check_won() # Will declare a tie if count is 9 and no winner
    # If empty_cells is false AND winner is true, check_won would have handled it.
    # If empty_cells is false AND winner is false AND count < 9 (should not happen), it's a logic error.


if __name__ == "__main__":
    # Configure main window
    window.title("Modern Tic Tac Toe")
    window.config(bg=BG_COLOR)

    # Create and grid Status Label
    # Ensure status_label is global if it's manipulated by functions outside this block before this point
    # However, given its UI nature, it's best initialized and used here or passed around.
    # For testing, it will be mocked.
    status_label = Label(window, text="Welcome to Tic Tac Toe!",
                         font=(FONT_NAME, FONT_SIZE_STATUS),
                         bg=BG_COLOR, fg=TEXT_COLOR,
                         relief=GROOVE, bd=2, wraplength=300) # wraplength for longer messages
    status_label.grid(row=3, column=0, columnspan=3, sticky="ew", pady=(10, 5), padx=10)

    # Configure grid weights for responsiveness (especially for the status label row)
    # Buttons are in rows 0, 1, 2. Status label in row 3.
    window.grid_rowconfigure(0, weight=1) # Button rows can take some space
    window.grid_rowconfigure(1, weight=1)
    window.grid_rowconfigure(2, weight=1)
    window.grid_rowconfigure(3, weight=0) # Status label row - fixed size initially, but sticky="ew" helps
    window.grid_columnconfigure(0, weight=1) # Columns for buttons
    window.grid_columnconfigure(1, weight=1)
    window.grid_columnconfigure(2, weight=1)

    # Initial game setup
    reset()
    window.mainloop()

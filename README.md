# Tic-Tac-Toe Enhanced

## Description

A classic Tic-Tac-Toe game implemented in Python using the Tkinter library. This version features a modernized user interface, the ability to play against an AI opponent with varying difficulty levels, and clear user feedback through a status display.

## Features

*   **Classic Tic-Tac-Toe Gameplay:** Play the timeless game of X's and O's.
*   **Player vs. Player Mode:** Play against a friend on the same computer.
*   **Player vs. Computer Mode:** Challenge an AI opponent with three difficulty levels:
    *   **Easy:** The AI makes random valid moves.
    *   **Medium:** The AI uses heuristics to look for winning moves or block opponent wins.
    *   **Hard:** The AI employs the Minimax algorithm to determine the optimal move.
*   **Modern User Interface:** A visually refreshed interface with a clean design, updated color palette, and improved button styling.
*   **Dynamic Status Label:** Provides real-time feedback on the game state, including whose turn it is, game outcomes (win, lose, tie), and current game mode/difficulty.
*   **Menu-Driven Options:** Easily switch between game modes and AI difficulty levels using the application menu.
*   **Unit Tested:** Key game logic and AI components are covered by unit tests to ensure reliability.

## Screenshots

*(Placeholder: Add screenshots of the game interface here. For example, main game board, mode selection, winning state display)*

*   `screenshot_main_game.png` - Main game interface.
*   `screenshot_options_menu.png` - Options menu showing game mode and difficulty selection.

## Technologies Used

*   **Python 3:** Core programming language.
*   **Tkinter:** Python's standard GUI (Graphical User Interface) package, used for building the game interface.

## Setup and Installation

1.  **Prerequisites:**
    *   Ensure you have Python 3 installed on your system. You can download it from [python.org](https://www.python.org/downloads/).
    *   Tkinter is usually included with standard Python installations. If not, you might need to install it separately (e.g., `sudo apt-get install python3-tk` on Debian/Ubuntu, or it might be part of a `python-devel` or `python-tools` package on other systems).

2.  **Clone the Repository (Optional):**
    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```
    (Replace `<repository_url>` and `<repository_directory>` with the actual URL and local directory name if you are cloning it. If you just have the `tic_tac_toe.py` file, you can skip this.)

3.  **Run the Game:**
    Open a terminal or command prompt, navigate to the directory containing the `tic_tac_toe.py` file, and run:
    ```bash
    python tic_tac_toe.py
    ```

## How to Play

1.  **Launch the Game:** Execute `python tic_tac_toe.py` from your terminal.
2.  **Game Modes & Difficulty:**
    *   By default, the game starts in "Player vs. Player" mode.
    *   To change the mode or AI difficulty:
        *   Click on "Options" in the menu bar.
        *   Select "Game Mode" to choose between "Player vs Player" or "Player vs Computer".
        *   If "Player vs Computer" is selected, go to "Options" > "Difficulty (PvC)" to choose "Easy", "Medium", or "Hard".
        *   Changing the game mode or difficulty will reset the current game.
3.  **Making a Move:**
    *   Player X always starts the game.
    *   Click on an empty cell on the 3x3 grid to place your mark.
    *   In "Player vs. Computer" mode, after you (Player X) make a move, the computer (Player O) will automatically make its move.
4.  **Winning the Game:**
    *   The first player to get three of their marks in a row (horizontally, vertically, or diagonally) wins the game.
    *   The status label at the bottom will announce the winner or if the game is a tie.
    *   Winning cells will be highlighted.
5.  **Resetting the Game:**
    *   To start a new game at any time, go to "Options" > "Reset Game".

## License

This project is licensed under the terms of the LICENSE file.

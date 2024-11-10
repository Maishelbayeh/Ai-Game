import tkinter as tk
import random
import copy

# Setting up the game window
root = tk.Tk()
root.title("Tic Tac Toe")
root.geometry("600x650")  # Set fixed window size
root.state('zoomed')  # Make window full screen
root.config(bg="#f0f0f0")  # Background color for the window

# Global variables
board = ['' for _ in range(9)]
current_player = "X"
difficulty = None  # No difficulty selected initially
buttons = []

# Functions
def check_winner(b):
    winning_combinations = [(0, 1, 2), (3, 4, 5), (6, 7, 8), (0, 3, 6), (1, 4, 7), (2, 5, 8), (0, 4, 8), (2, 4, 6)]
    for (i, j, k) in winning_combinations:
        if b[i] == b[j] == b[k] and b[i] != '':
            return b[i]
    if '' not in b:
        return "Draw"
    return None

def switch_player():
    global current_player
    current_player = "O" if current_player == "X" else "X"

def handle_click(i):
    global current_player
    if difficulty is None:
        # Show a message if the user tries to play before selecting difficulty
        label.config(text="Please select a difficulty level first!", fg="#ff6347", font=('Arial', 24, 'bold'))
        return
    if board[i] == '' and current_player == "X":
        board[i] = current_player
        buttons[i].config(text=current_player, bg="#ffffff", fg="#333333", font=('Arial', 24, 'bold'), state="disabled", relief="solid")
        if check_winner(board):
            end_game(check_winner(board))
        else:
            switch_player()
            root.after(500, ai_move)  # AI moves after 0.5s delay

def ai_move():
    if difficulty == "Easy":
        make_random_move()
    elif difficulty == "Medium":
        if random.random() < 0.5:
            make_random_move()
        else:
            make_optimal_move()
    elif difficulty == "Hard":
        make_optimal_move()
    
    if check_winner(board):
        end_game(check_winner(board))
    else:
        switch_player()

def make_random_move():
    empty_cells = [i for i, x in enumerate(board) if x == '']
    if empty_cells:
        move = random.choice(empty_cells)
        board[move] = current_player
        buttons[move].config(text=current_player, bg="#ffffff", fg="#333333", font=('Arial', 24, 'bold'), state="disabled", relief="solid")

def make_optimal_move():
    best_score = float('-inf')
    best_move = None
    for i in range(9):
        if board[i] == '':
            board[i] = current_player
            score = minimax(board, False)
            board[i] = ''
            if score > best_score:
                best_score = score
                best_move = i
    if best_move is not None:
        board[best_move] = current_player
        buttons[best_move].config(text=current_player, bg="#ffffff", fg="#333333", font=('Arial', 24, 'bold'), state="disabled", relief="solid")

def minimax(b, is_maximizing):
    winner = check_winner(b)
    if winner == "X":
        return -1
    elif winner == "O":
        return 1
    elif winner == "Draw":
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for i in range(9):
            if b[i] == '':
                b[i] = "O"
                score = minimax(b, False)
                b[i] = ''
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for i in range(9):
            if b[i] == '':
                b[i] = "X"
                score = minimax(b, True)
                b[i] = ''
                best_score = min(score, best_score)
        return best_score

def end_game(result):
    if result == "Draw":
        label.config(text="It's a Draw!", fg="#ff6347", font=('Arial', 28, 'bold'))
    else:
        label.config(text=f"{result} Wins!", fg="#32cd32", font=('Arial', 28, 'bold'))
    for button in buttons:
        button.config(state="disabled")

def reset_game():
    global board, current_player, difficulty
    board = ['' for _ in range(9)]
    current_player = "X"
    label.config(text="Tic Tac Toe", fg="#000000", font=('Arial', 28, 'bold'))
    for button in buttons:
        button.config(text="", state="normal", bg="#f4f4f9", fg="#333", font=('Arial', 24, 'bold'))
    difficulty = None
    disable_gameboard()

def disable_gameboard():
    """Disable all the gameboard buttons until difficulty is selected."""
    for button in buttons:
        button.config(state="disabled")

def enable_gameboard():
    """Enable all the gameboard buttons after difficulty is selected."""
    for button in buttons:
        button.config(state="normal")

def set_difficulty(new_difficulty):
    global difficulty
    difficulty = new_difficulty
    enable_gameboard()  # Enable the game board after selecting difficulty
    label.config(text=f"Difficulty: {difficulty}", fg="#000000", font=('Arial', 24, 'bold'))

# GUI setup
frame = tk.Frame(root, bg="#f4f4f9")
frame.pack(pady=30)

label = tk.Label(root, text="Tic Tac Toe", font=('Arial', 28, 'bold'), bg="#f4f4f9", fg="#333")
label.pack()

# Create buttons for the Tic Tac Toe board
for i in range(9):
    button = tk.Button(frame, text="", width=8, height=3, font=('Arial', 24, 'bold'),
                       command=lambda i=i: handle_click(i), bg="#f4f4f9", fg="#333", relief="solid")
    button.grid(row=i // 3, column=i % 3, padx=5, pady=5)
    buttons.append(button)

difficulty_frame = tk.Frame(root, bg="#f4f4f9")
difficulty_frame.pack(pady=20)

easy_button = tk.Button(difficulty_frame, text="Easy", command=lambda: set_difficulty("Easy"), font=('Arial', 16), bg="#87CEEB", fg="#fff", relief="solid", padx=10, pady=5)
easy_button.grid(row=0, column=0, padx=10)

medium_button = tk.Button(difficulty_frame, text="Medium", command=lambda: set_difficulty("Medium"), font=('Arial', 16), bg="#FFD700", fg="#fff", relief="solid", padx=10, pady=5)
medium_button.grid(row=0, column=1, padx=10)

hard_button = tk.Button(difficulty_frame, text="Hard", command=lambda: set_difficulty("Hard"), font=('Arial', 16), bg="#FF4500", fg="#fff", relief="solid", padx=10, pady=5)
hard_button.grid(row=0, column=2, padx=10)

reset_button = tk.Button(root, text="Reset", command=reset_game, font=('Arial', 16, 'bold'), bg="#32cd32", fg="#fff", relief="solid", padx=20, pady=10)
reset_button.pack(pady=20)

root.mainloop()

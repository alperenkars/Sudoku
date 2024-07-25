import tkinter as tk
from tkinter import messagebox, font
import random

class SudokuGame:
    def __init__(self, difficulty=30):
        self.board = self.generate_board()
        self.original_board = [row[:] for row in self.board]
        self.remove_numbers(difficulty)

    def generate_board(self):
        board = [[0 for _ in range(9)] for _ in range(9)]
        self.solve_board(board)
        return board

    def solve_board(self, board):
        find = self.find_empty(board)
        if not find:
            return True
        else:
            row, col = find

        for i in range(1, 10):
            if self.valid(board, i, (row, col)):
                board[row][col] = i

                if self.solve_board(board):
                    return True

                board[row][col] = 0

        return False

    def valid(self, board, num, pos):
        # Check row
        for i in range(len(board[0])):
            if board[pos[0]][i] == num and pos[1] != i:
                return False

        # Check column
        for i in range(len(board)):
            if board[i][pos[1]] == num and pos[0] != i:
                return False

        # Check box
        box_x = pos[1] // 3
        box_y = pos[0] // 3

        for i in range(box_y*3, box_y*3 + 3):
            for j in range(box_x * 3, box_x*3 + 3):
                if board[i][j] == num and (i,j) != pos:
                    return False

        return True

    def find_empty(self, board):
        for i in range(len(board)):
            for j in range(len(board[0])):
                if board[i][j] == 0:
                    return (i, j)  # row, col
        return None

    def remove_numbers(self, difficulty):
        count = 0
        while count < difficulty:
            row = random.randint(0, 8)
            col = random.randint(0, 8)
            if self.board[row][col] != 0:
                self.board[row][col] = 0
                count += 1

    def is_valid_move(self, row, col, num):
        return self.valid(self.board, num, (row, col))

    def is_solved(self):
        return self.board == self.original_board

class SudokuUI:
    def __init__(self, game):
        self.game = game
        self.root = tk.Tk()
        self.root.title("Sudoku")
        self.root.configure(bg='#F0F0F0')
        self.cells = {}
        self.create_board()

    def create_board(self):
        main_frame = tk.Frame(self.root, bg='#F0F0F0', padx=20, pady=20)
        main_frame.pack()

        board_frame = tk.Frame(main_frame, bg='black', padx=3, pady=3)
        board_frame.grid(row=0, column=0)

        cell_font = font.Font(family="Arial", size=16, weight="bold")

        for i in range(9):
            for j in range(9):
                cell_frame = tk.Frame(board_frame, borderwidth=1, relief="raised", bg='black')
                cell_frame.grid(row=i, column=j)
                
                cell = tk.Entry(cell_frame, width=2, font=cell_font, justify='center', 
                                bg='white', fg='black', insertbackground='black')
                cell.pack(expand=True, fill='both', ipady=8)
                
                self.cells[(i, j)] = cell
                
                if self.game.board[i][j] != 0:
                    cell.insert(0, str(self.game.board[i][j]))
                    cell.config(state="readonly", disabledbackground='#E0E0E0', disabledforeground='black')
                else:
                    cell.bind('<KeyRelease>', lambda e, row=i, col=j: self.key_pressed(e, row, col))

            # Add thicker lines between 3x3 squares
            if i % 3 == 2 and i < 8:
                separator = tk.Frame(board_frame, height=2, bg='black')
                separator.grid(row=i+1, column=0, columnspan=9, sticky='ew')

        # for j in range(3, 9, 3):
        #     separator = tk.Frame(board_frame, width=2, bg='black')
        #     separator.grid(row=0, column=j, rowspan=9, sticky='ns')

        check_button = tk.Button(main_frame, text="Check Solution", command=self.check_solution,
                                 bg='#4CAF50', fg='white', font=('Arial', 12, 'bold'),
                                 padx=10, pady=5)
        check_button.grid(row=1, column=0, pady=20)

    # ... (rest of the methods remain the same)

    def key_pressed(self, event, row, col):
        if event.char.isdigit() and 1 <= int(event.char) <= 9:
            self.cells[(row, col)].delete(0, tk.END)
            self.cells[(row, col)].insert(0, event.char)
            self.game.board[row][col] = int(event.char)
        elif event.keysym == 'BackSpace':
            self.cells[(row, col)].delete(0, tk.END)
            self.game.board[row][col] = 0

    def check_solution(self):
        if self.game.is_solved():
            messagebox.showinfo("Congratulations!", "You've solved the Sudoku!")
        else:
            messagebox.showinfo("Not Quite", "The solution is not correct yet. Keep trying!")

    def run(self):
        self.root.mainloop()

def main():
    game = SudokuGame(difficulty=30)  # Adjust difficulty here (higher number = more empty cells)
    ui = SudokuUI(game)
    ui.run()

if __name__ == "__main__":
    main()
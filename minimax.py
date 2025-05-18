import tkinter as tk
import copy

class MinimaxNode:
    def __init__(self, board, is_maximizing, move=None):
        self.board = board
        self.is_maximizing = is_maximizing
        self.move = move
        self.children = []
        self.score = None

class TicTacToe:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("Gato con Minimax")

        self.canvas = tk.Canvas(self.window, width=300, height=300)
        self.canvas.grid(row=0, column=1)
        self.canvas.bind("<Button-1>", self.click)

        self.tree_text = tk.Text(self.window, width=50, height=35)
        self.tree_text.grid(row=0, column=0, padx=5, pady=5)

        self.board = [["" for _ in range(3)] for _ in range(3)]
        self.draw_board()

    def draw_board(self):
        self.canvas.delete("all")
        for i in range(1, 3):
            self.canvas.create_line(0, 100 * i, 300, 100 * i)
            self.canvas.create_line(100 * i, 0, 100 * i, 300)

        for r in range(3):
            for c in range(3):
                if self.board[r][c] == "X":
                    self.canvas.create_line(c * 100 + 20, r * 100 + 20,
                                             c * 100 + 80, r * 100 + 80, width=2)
                    self.canvas.create_line(c * 100 + 80, r * 100 + 20,
                                             c * 100 + 20, r * 100 + 80, width=2)
                elif self.board[r][c] == "O":
                    self.canvas.create_oval(c * 100 + 20, r * 100 + 20,
                                            c * 100 + 80, r * 100 + 80, width=2)

    def click(self, event):
        if self.check_winner(self.board) or self.is_full(self.board):
            return

        col = event.x // 100
        row = event.y // 100

        if self.board[row][col] == "":
            self.board[row][col] = "X"
            self.draw_board()

            if not self.check_winner(self.board) and not self.is_full(self.board):
                _, move, tree = self.minimax(self.board, False)
                if move:
                    r, c = move
                    self.board[r][c] = "O"
                    self.draw_board()
                self.tree_text.delete("1.0", tk.END)
                self.display_tree(tree)

    def minimax(self, board, is_maximizing):
        winner = self.check_winner(board)
        if winner == "X":
            return 1, None, MinimaxNode(board, is_maximizing, None)
        elif winner == "O":
            return -1, None, MinimaxNode(board, is_maximizing, None)
        elif self.is_full(board):
            return 0, None, MinimaxNode(board, is_maximizing, None)

        best_score = float("-inf") if is_maximizing else float("inf")
        best_move = None
        root = MinimaxNode(copy.deepcopy(board), is_maximizing)

        for r in range(3):
            for c in range(3):
                if board[r][c] == "":
                    board[r][c] = "X" if is_maximizing else "O"
                    score, _, child_node = self.minimax(board, not is_maximizing)
                    board[r][c] = ""
                    child_node.move = (r, c)
                    root.children.append(child_node)

                    if is_maximizing and score > best_score:
                        best_score = score
                        best_move = (r, c)
                    elif not is_maximizing and score < best_score:
                        best_score = score
                        best_move = (r, c)

        root.score = best_score
        return best_score, best_move, root

    def is_full(self, board):
        return all(board[r][c] != "" for r in range(3) for c in range(3))

    def check_winner(self, board):
        lines = [
            # Horizontales
            [(0, 0), (0, 1), (0, 2)],
            [(1, 0), (1, 1), (1, 2)],
            [(2, 0), (2, 1), (2, 2)],
            # Verticales
            [(0, 0), (1, 0), (2, 0)],
            [(0, 1), (1, 1), (2, 1)],
            [(0, 2), (1, 2), (2, 2)],
            # Diagonales
            [(0, 0), (1, 1), (2, 2)],
            [(0, 2), (1, 1), (2, 0)]
        ]
        for line in lines:
            values = [board[r][c] for r, c in line]
            if values[0] != "" and all(val == values[0] for val in values):
                return values[0]
        return None

    def display_tree(self, node, depth=0):
        indent = "  " * depth
        move_str = f"Move: {node.move}, Score: {node.score}"
        board_str = " | ".join(" ".join(row) for row in node.board)
        self.tree_text.insert(tk.END, f"{indent}{move_str} | {board_str}\n")
        for child in node.children:
            self.display_tree(child, depth + 1)

    def run(self):
        self.window.mainloop()

def MinimaxVisualizer():
    TicTacToe().run()

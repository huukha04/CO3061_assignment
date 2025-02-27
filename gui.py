import tkinter as tk
from pipe import Pipe
from solve import Game


class GameGUI:
    def __init__(self, game: "Game"):
        self.game = game
        self.cell_size = 50  # Kích thước ô vuông
        self.root = tk.Tk()
        self.root.title("Pipe Game")

        self.canvas = tk.Canvas(self.root, width=game.cols * self.cell_size, height=game.rows * self.cell_size)
        self.canvas.pack()

        self.draw_grid()

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                self.draw_pipe(x, y, self.game.grid[y][x])

    def draw_pipe(self, x, y, pipe: Pipe):
        """ Vẽ ống nước tại tọa độ (x, y) """
        x1, y1 = x * self.cell_size, y * self.cell_size
        x2, y2 = x1 + self.cell_size, y1 + self.cell_size

        color = "red" if pipe.is_source() else "blue" if pipe.contains_water() else  "black"

        self.canvas.create_rectangle(x1, y1, x2, y2, outline="gray", width=2)

        if pipe.up():
            self.canvas.create_line((x1 + x2) // 2, y1, (x1 + x2) // 2, (y1 + y2) // 2, fill=color, width=5)
        if pipe.right():
            self.canvas.create_line(x2, (y1 + y2) // 2, (x1 + x2) // 2, (y1 + y2) // 2, fill=color, width=5)
        if pipe.down():
            self.canvas.create_line((x1 + x2) // 2, y2, (x1 + x2) // 2, (y1 + y2) // 2, fill=color, width=5)
        if pipe.left():
            self.canvas.create_line(x1, (y1 + y2) // 2, (x1 + x2) // 2, (y1 + y2) // 2, fill=color, width=5)

    def update(self, game):
        """ Cập nhật GUI khi có thay đổi """
        self.game = game
        self.draw_grid()
        self.root.update_idletasks()
        self.root.update()

    def run(self):
        self.root.mainloop()
    

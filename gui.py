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

        self.pipe_images = {
            "empty": self.resize_image(tk.PhotoImage(file="images/Empty_Tile.png"), 3),
            "U": self.resize_image(tk.PhotoImage(file="images/U.png"), 3),
            "D": self.resize_image(tk.PhotoImage(file="images/D.png"), 3),
            "L": self.resize_image(tk.PhotoImage(file="images/L.png"), 3),
            "R": self.resize_image(tk.PhotoImage(file="images/R.png"), 3),
            "UD": self.resize_image(tk.PhotoImage(file="images/UD.png"), 3),
            "RL": self.resize_image(tk.PhotoImage(file="images/RL.png"), 3),
            "UL": self.resize_image(tk.PhotoImage(file="images/UL.png"), 3),
            "UR": self.resize_image(tk.PhotoImage(file="images/UR.png"), 3),
            "DL": self.resize_image(tk.PhotoImage(file="images/DL.png"), 3),
            "RD": self.resize_image(tk.PhotoImage(file="images/RD.png"), 3),
            "RDL": self.resize_image(tk.PhotoImage(file="images/RDL.png"), 3),
            "URD": self.resize_image(tk.PhotoImage(file="images/URD.png"), 3),
            "URL": self.resize_image(tk.PhotoImage(file="images/URL.png"), 3),
            "UDL": self.resize_image(tk.PhotoImage(file="images/UDL.png"), 3),
            "URDL": self.resize_image(tk.PhotoImage(file="images/URDL.png"), 3),
            "U_Lit": self.resize_image(tk.PhotoImage(file="images/U_Lit.png"), 3),
            "D_Lit": self.resize_image(tk.PhotoImage(file="images/D_Lit.png"), 3),
            "L_Lit": self.resize_image(tk.PhotoImage(file="images/L_Lit.png"), 3),
            "R_Lit": self.resize_image(tk.PhotoImage(file="images/R_Lit.png"), 3),
            "UD_Lit": self.resize_image(tk.PhotoImage(file="images/UD_Lit.png"), 3),
            "RL_Lit": self.resize_image(tk.PhotoImage(file="images/RL_Lit.png"), 3),
            "UL_Lit": self.resize_image(tk.PhotoImage(file="images/UL_Lit.png"), 3),
            "UR_Lit": self.resize_image(tk.PhotoImage(file="images/UR_Lit.png"), 3),
            "DL_Lit": self.resize_image(tk.PhotoImage(file="images/DL_Lit.png"), 3),
            "RD_Lit": self.resize_image(tk.PhotoImage(file="images/RD_Lit.png"), 3),
            "RDL_Lit": self.resize_image(tk.PhotoImage(file="images/RDL_Lit.png"), 3),
            "URD_Lit": self.resize_image(tk.PhotoImage(file="images/URD_Lit.png"), 3),
            "URL_Lit": self.resize_image(tk.PhotoImage(file="images/URL_Lit.png"), 3),
            "UDL_Lit": self.resize_image(tk.PhotoImage(file="images/UDL_Lit.png"), 3),
            "URDL_Lit": self.resize_image(tk.PhotoImage(file="images/URDL_Lit.png"), 3),
        }


        self.draw_grid()

    def resize_image(self, image, factor):
        """ Phóng to hình ảnh bằng hệ số factor """
        return image.zoom(factor, factor)

    def draw_grid(self):
        self.canvas.delete("all")
        for y in range(self.game.rows):
            for x in range(self.game.cols):
                self.draw_pipe(x, y, self.game.grid[y][x])

    def draw_pipe(self, x, y, pipe: Pipe):
        """ Chèn hình ảnh ống nước vào tọa độ (x, y) """
        x1, y1 = x * self.cell_size, y * self.cell_size

        # Xác định hướng của pipe
        directions = ""
        if pipe.up():
            directions += "U"
        if pipe.right():
            directions += "R"
        if pipe.down():
            directions += "D"
        if pipe.left():
            directions += "L"

        # Nếu chứa nước thì thêm hậu tố "_Lit"
        if pipe.contains_water():
            directions += "_Lit"

        # Nếu không có hướng nào, đặt thành "empty"
        image_key = directions if directions else "empty"

        # Chèn hình ảnh vào Canvas
        self.canvas.create_image(x1 + self.cell_size // 2, y1 + self.cell_size // 2, image=self.pipe_images[image_key])

    def update(self, game):
        """ Cập nhật GUI khi có thay đổi """
        self.game = game
        self.draw_grid()
        self.root.update_idletasks()
        self.root.update()

    def run(self):
        self.root.mainloop()

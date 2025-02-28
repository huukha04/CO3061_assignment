from pipe import Pipe 
from solve import Game
import time
import tracemalloc 
import matplotlib.pyplot as plt
import numpy as np

class Puzzle:
    def __init__(self, input = None):
        self.row = None
        self.col = None
        if not input:  
            self.puzzle = []
        else:
            self.puzzle = self.hex2puzzle(input)
    
    def hex2puzzle(self, hex_value):
        """Chuyển số hex thành lưới puzzle"""
        hex_value = hex_value[2:]
        if len(hex_value) < 4:
            raise ValueError("Chuỗi quá ngắn để chứa thông tin hàng và cột!")

        self.row = int(hex_value[:2], 16)
        self.col = int(hex_value[2:4], 16)
        pipes = [Pipe.set(int(hex_value[i:i+2], 16)) for i in range(4, len(hex_value), 2)]


        if len(pipes) != self.row * self.col:
            raise ValueError("Thông tin row col và số phần tử không khớp!")

        return [[pipes[r * self.col + c] for c in range(self.col)] for r in range(self.row)]

    def puzzle2hex(self):
        if self.puzzle is None or not self.puzzle:
            return ""
        row_hex = f"{self.row:02X}"
        col_hex = f"{self.col:02X}"
        result = []
        for c in range(self.col):
            for r in range(self.row):
                result.append(str(self.puzzle[r][c]))  # Duyệt theo cột trước, hàng sau
        
        return "0x" + row_hex + col_hex + "".join(result)
    
    def print_puzzle(self):
        for row in self.puzzle:
            row_symbols = []
            for pipe in row:
                if pipe.is_source():
                    row_symbols.append(f'\033[91m{str(pipe)}\033[0m')  # Đỏ
                elif pipe.contains_water():
                    row_symbols.append(f'\033[94m{str(pipe)}\033[0m')  # Xanh dương
                else:
                    row_symbols.append(str(pipe))  # Mặc định

            print("".join(row_symbols))  # In từng dòng của puzzle

    def print_line(self):
        print(self.puzzle2hex())

    def solve_dfs(self):
        print("Initial state: ")
        self.print_puzzle()
        game = Game(self.puzzle)

        print("Solution: ")
        
        tracemalloc.start()
        start_time = time.perf_counter()

        solution = game.solve_dfs() 

        end_time = time.perf_counter()
        current = tracemalloc.get_traced_memory()
        tracemalloc.stop()

        print(solution)
        print("Time elapsed:", end_time - start_time)
        print("Memory", current)

        from gui import GameGUI
        
        self.gui = GameGUI(game) 
        time.sleep(100)


            

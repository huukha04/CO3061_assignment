from puzzle import Puzzle
if __name__ == "__main__":
    puzzle = Puzzle("0x040480C0C080C0E0E0C080E0C1A080C080C0")  # Tạo đối tượng với hex_value
    puzzle = Puzzle("0x0303C0E0C0A0A08080C180")
    
    #puzzle = Puzzle("0x020260308081")
    solution = puzzle.solve_dfs()  # Gọi hàm không cần truyền lại hex_value

    
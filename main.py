from puzzle import Puzzle
if __name__ == "__main__":
    puzzle = Puzzle("0x040480C0C080C0E0E0C080E0C1A080C080C0")  # Tạo đối tượng với hex_value
    solution = puzzle.solve_dfs()  # Gọi hàm không cần truyền lại hex_value

    
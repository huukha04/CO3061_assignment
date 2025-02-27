import random as rd

class Pipe(int):
    """
    Dùng 2 byte = 8 bit mã hóa 1 ống
    Bit 0: Có chứa nước
    Bit 1: Là nguồn nước
    Bit 2-3: Không dùng
    Bit 4 - 5 - 6 - 7: Left - down - right - up
    
    """
    def is_source(self):
        return self & 0x01 == 0x01
    def contains_water(self):
        return self & 0x02 == 0x02
    def is_sink(self):
        return int.bit_count(self >> 4) == 1
    def up(self):
        return self & 0x80 != 0 
    def right(self):
        return self & 0x40 != 0
    def down(self):
        return self & 0x20 != 0
    def left(self):
        return self & 0x10 != 0
    """_________________________________"""
    def set_water(self):
        return Pipe(self | 0x02)
    def unset_water(self):
        return Pipe(self & 0xFD)  
    def rotate_clockwise(self, times=1):
        pipe = self
        for _ in range(times):
            pipe = Pipe((pipe >> 1 | ((pipe & 0x10) << 3)) & 0xF0 | (pipe & 0x0F)
                    )
        return pipe
    def _random_rotate(self):
        a = self
        for _ in range(rd.randint(0, 3)):
            a = a.rotate_clockwise()
        return a
    def get_offset(self):
        li = []
        if self.up():
            li.append((-1, 0))
        if self.right():
            li.append((0, 1))
        if self.down():
            li.append((1, 0))
        if self.left():
            li.append((0, -1))
        return li
    """_________________________________"""
    def __repr__(self):
        if self.is_source():
            return f'\033[91m{self:02X}\033[0m'
        elif self.contains_water():
            return f'\033[94m{self:02X}\033[0m'  
        return f'{self:02X}' 
    """_________________________________"""
    @classmethod
    def set(cls, pipe):
        return cls(pipe)._random_rotate()
    

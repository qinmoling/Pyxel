import pygame
from constants import *


class Grid:
    def __init__(self, window):
        self.window = window
        self.tile_positioned_color = {}
        self.pressed_color = ()
        self.init_draw()

    def init_draw(self):#先画上灰色
        for column in range(COLUMNS):
            for row in range(ROWS):
                self.draw_to_screen(COLOR0, column, row)
                self.tile_positioned_color[(column, row)] = COLOR0

    def draw_to_screen(self, color, column_x, row_y):#根据颜色不同的参数分类
        pygame.draw.rect(self.window, color, (column_x * TILESIZE, row_y * TILESIZE, TILESIZE, TILESIZE))
        self.tile_positioned_color[(column_x, row_y)] = color

    def draw_with_mouse(self, column_x, row_y):#根据鼠标进行上色，判断是不是原来的颜色，若不是，上其他的颜色，同时也把坐标赋值给press_color,进行记录
        if self.tile_positioned_color[(column_x, row_y)] == COLOR0 and self.pressed_color != (column_x, row_y):
            self.draw_to_screen(COLOR1, column_x, row_y)
            self.pressed_color = (column_x, row_y)

        elif self.tile_positioned_color[(column_x, row_y)] == COLOR1 and self.pressed_color != (column_x, row_y):
            self.draw_to_screen(COLOR2, column_x, row_y)
            self.pressed_color = (column_x, row_y)

        elif self.tile_positioned_color[(column_x, row_y)] == COLOR2 and self.pressed_color != (column_x, row_y):
            self.draw_to_screen(COLOR3, column_x, row_y)
            self.pressed_color = (column_x, row_y)

        elif self.tile_positioned_color[(column_x, row_y)] == COLOR3 and self.pressed_color != (column_x, row_y):
            self.draw_to_screen(COLOR0, column_x, row_y)
            self.pressed_color = (column_x, row_y)

    def reset_pressed_color(self):#设置最开始的状态
        self.pressed_color = 0

    # 将颜色调整为该有的顺序
    def to_hex(self):
        binary_upper = ""
        binary_lower = ""
        for row in range(ROWS):#对于每个不同的方块进行赋值
            for column in range(COLUMNS):
                if self.tile_positioned_color[(column, row)] == COLOR0:
                    binary_upper += '0'
                    binary_lower += '0'
                elif self.tile_positioned_color[(column, row)] == COLOR1:
                    binary_upper += '1'
                    binary_lower += '0'
                elif self.tile_positioned_color[(column, row)] == COLOR2:
                    binary_upper += '0'
                    binary_lower += '1'
                elif self.tile_positioned_color[(column, row)] == COLOR3:
                    binary_upper += '1'
                    binary_lower += '1'
        binary_upper_list = [binary_upper[i: (i+8)] for i in range(0, len(binary_upper), 8)]#切分字符
        binary_lower_list = [binary_lower[i: (i+8)] for i in range(0, len(binary_lower), 8)]
        hex_code_upper = [hex(int(binary, 2)) for binary in binary_upper_list]#将二进制变为十六进制
        hex_code_lower = [hex(int(binary, 2)) for binary in binary_lower_list]
        file = open('hex.txt', 'w')
        for u, l in zip(hex_code_upper, hex_code_lower):
            u = u.replace("0x", "")#删除'0x'
            l = l.replace("0x", "")
            if len(u) == 1:#转化为大写字母
                u = u.zfill(2)
            if len(l) == 1:
                l = l.zfill(2)
            file.write(f" {u.upper()} {l.upper()}")
        file.close()#关闭

    def from_hex(self):
        hex_low = []
        hex_high = []
        increment = 0
        increment_final = 2
        which_color = {}
        try:
            with open('hex.txt', 'r') as hex_file:#去掉空格和换行符
                hex_codes = hex_file.readline()
                hex_codes = "".join(hex_codes.split())
            for i in range(8):
                hex_high.append(bin(int(hex_codes[increment:increment_final], 16))[2:].zfill(8))
                increment += 2
                increment_final += 2
                hex_low.append(bin(int(hex_codes[increment:increment_final], 16))[2:].zfill(8))
                increment += 2
                increment_final += 2

            for a in range(0, len(hex_high)):
                for i in range(0, 8):
                    which_color[(a, i)] = hex_high[a][i] + hex_low[a][i]

            for color_pos in which_color:#根据文件记录的字符，进行颜色的转变
                if which_color[color_pos] == '00':
                    self.draw_to_screen(COLOR0, color_pos[1], color_pos[0])
                elif which_color[color_pos] == '10':
                    self.draw_to_screen(COLOR1, color_pos[1], color_pos[0])
                elif which_color[color_pos] == '01':
                    self.draw_to_screen(COLOR2, color_pos[1], color_pos[0])
                elif which_color[color_pos] == '11':
                    self.draw_to_screen(COLOR3, color_pos[1], color_pos[0])
        except:
            print("File not found")
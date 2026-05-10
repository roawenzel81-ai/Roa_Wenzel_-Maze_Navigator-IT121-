import tkinter as tk
import pygame

class Player:
    def __init__(self, x, y):
        self.x = int(x)
        self.y = int(y)
        self.player_size = 20
        self.circle = pygame.draw.circle(screen, self.color, (self.x, self.y), self.player_size)
        self.color = "peachpuff"
        self.velocity_x = 0
        self.velocity_y = 0
        self.left_arrow = False
        self.right_arrow = False
        self.up_arrow = False
        self.down_arrow = False
        self.w_key = self.up_arrow
        self.a_key = self.left_arrow
        self.s_key = self.down_arrow
        self.d_key = self.right_arrow
        self.movement = ""
        self.speed = 5
    
    def player_movement(self):
        pass
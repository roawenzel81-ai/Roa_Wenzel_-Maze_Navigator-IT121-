import tkinter as tk
import random as r

class Cell:
    # Initialize the variable of walls in maze
    def __init__(self, root, x, y, size):
        self.x, self.y = x, y
        self.size = size
        self.walls_line_position = {self.root, "top" == True, "bottom" == True, "left" == True, "right" == True}
        self.visited = False

    # Draw a walls
    def walls(self, root, tile):
        x, y = self.x * tile, self.y * tile
        for i in range(1, 40):
            if self.walls_line_position[self.root, "top"]:
                top_line_walls = tk.Canvas(self.root, create_line = ("150, 0, 150, 250"), fill = "White")
    
    Cell(tk.Tk()).root.mainloop()

import tkinter as tk
from tkinter import messagebox
import pygame

class GameTitle:
    # Main game title
    def __init__(self, root):
        self.root = root
        self.root.title("Forgotten Labyrinth")
        self.root.geometry("1200x500")
        self.root.configure(bg = "black")

        self.label = tk.Label(self.root, text = "Welcome to the Forgotten Labyrinth!", fg = "white", bg = "black", font = ("Arial", "25"))
        self.label.grid(row = 0, column = 0, sticky = "w", padx = 332, pady = 150)

        self.start = tk.Button(self.root, text = "Play", font = ("Arial", "18"), command = self.instruction)
        self.start.grid(row = 1, column = 0, sticky = "n", padx = 30, pady = 10)

        self.exit = tk.Button(self.root, text = "Exit", font = ("Arial", "18"), command = self.exit_game)
        self.exit.grid(row = 2, column = 0, sticky = "n", padx = 30, pady = 10)
    
    # Going back to main menu when you press "Back" button
    def main_menu(self):
        self.label.grid(row = 0, column = 0, sticky = "w", padx = 332, pady = 150)
        self.start.grid(row = 1, column = 0, sticky = "n", padx = 30, pady = 10)
        self.exit.grid(row = 2, column = 0, sticky = "n", padx = 30, pady = 10)

        self.instruction_title.grid_forget()
        self.movement_ins.grid_forget()
        self.start_game.grid_forget()
        self.back.grid_forget()
        self.save_and_quittomenu_button.grid_forget()
        self.game_menu_button.grid_forget()

    # Exit the game
    def exit_game(self):
        if tk.messagebox.askyesno(title = "Exit", message = "Are you sure you want to go exit?"):
            self.root.destroy()

    # Game instructions for player's movement
    def instruction(self):
        self.instruction_title = tk.Label(self.root, text = "Instructions", fg = "white", bg = "black", font = ("Arial", "45"))
        self.instruction_title.grid(row = 0, column = 0, padx = 438, pady = 75)

        self.movement_ins = tk.Label(self.root, text = "All control movements from the player are:\n\nW - Move Up\nA - Move Left\nS - Move Down\nD - Move Right\n\nArrow Keys - Move in the respective direction", fg = "white", bg = "black", font = ("Arial", "14"))
        self.movement_ins.grid(row = 1, column = 0, sticky = "w", padx = 400, pady = 0)

        self.label.grid_forget()
        self.start.grid_forget()
        self.exit.grid_forget()

        self.start_game_button()
        self.back_button()
        
    # Start the game after instructions
    def start_game_button(self):
        self.start_game = tk.Button(self.root, text = "Start", font = ("Arial", "18"), command = self.start_messagebox)
        self.start_game.grid(row = 4, column = 0, sticky = "w", padx = 500, pady = 10)

    def start_messagebox(self):
        if tk.messagebox.askyesno(title = "Start Game", message = "Are you sure you want to start the game?"):
            self.maze_gameplay()

    # Back to the main menu from main game title
    def back_button(self):
        self.back = tk.Button(self.root, text = "Back", font = ("Arial", "18"), command = self.main_menu)
        self.back.grid(row = 4, column = 0, sticky = "e", padx = 500, pady = 10)

    # Game menu button (main)
    def game_menu(self):
        self.game_menu_button = tk.Button(self.root, text = "Game Menu", font = ("Arial", "18"), command = self.game_menu_show_n_hide)
        self.game_menu_button.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = 0)

        self.save_and_quittomenu_button = tk.Button(self.root, text = "Save & Quit", font = ("Arial", "18"), command = self.save_and_quit_messagebox)
        self.save_and_quittomenu_button.grid(row = 0, column = 1, sticky = "n", padx = 345, pady = 0)

        self.save_and_quittomenu_button.grid_forget()

    # Game menu button with options (show & hide)
    def game_menu_show_n_hide(self):
        # Show a button if it's not viewable
        if not self.save_and_quittomenu_button.winfo_viewable():
            self.save_and_quittomenu_button.grid(row = 0, column = 1, sticky = "n", padx = 345, pady = 0)
            self.maze_gameplay_label.grid_forget()  
        # Hide the button if it's viewable
        if self.save_and_quittomenu_button.winfo_viewable():
            self.save_and_quittomenu_button.grid_forget()
            self.maze_gameplay_label.grid(row = 6, column = 0, sticky = "n", padx = 550, pady = 30)
        
    def save_and_quit_messagebox(self):
        if tk.messagebox.askyesno(title = "Save & Quit", message = "Are you sure you want to save the file & quit the game?"):
            self.main_menu()

    # Level 1
    def maze_gameplay(self):
        self.instruction_title.grid_forget()
        self.movement_ins.grid_forget()
        self.start_game.grid_forget()

        self.maze_gameplay_label = tk.Label(self.root, text = "Level 1", fg = "white", bg = "black", font = ("Arial", "20"))
        self.maze_gameplay_label.grid(row = 6, column = 0, sticky = "n", padx = 550, pady = 30)

        self.game_menu()

        self.back.grid_forget()

# Main game
GameTitle(tk.Tk()).root.mainloop()
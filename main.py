import tkinter as tk
from tkinter import messagebox
import random

CELL_SIZE = 20
ROWS, COLUMNS = 18, 18

class Game:
    def __init__(self, root):
        self.root = root
        self.seed = None
        self.saved_row = 0
        self.saved_column = 0
        self.saved_time_remaining = 120

        self.menu = Main_Menu(self)
        self.save_system = SaveSystem(self)

    def start_gameplay(self):
        self.gameplay = Gameplay(self)

class Main_Menu:
    # Main game title
    def __init__(self, game):
        self.game = game
        self.root = game.root
        self.root.title("Forgotten Labyrinth")
        self.root.geometry("1200x500")
        self.root.configure(bg = "black")
        self.root.resizable(False, False)

        self.label = tk.Label(self.root, text = "Welcome to the Forgotten Labyrinth!", fg = "white", bg = "black", font = ("Arial", "25"))
        self.label.grid(row = 0, column = 0, sticky = "w", padx = 332, pady = 120)

        self.start = tk.Button(self.root, text = "Play", font = ("Arial", "18"), command = self.instruction)
        self.start.grid(row = 1, column = 0, sticky = "n", padx = 30, pady = 10)

        self.exit = tk.Button(self.root, text = "Exit", font = ("Arial", "18"), command = self.exit_game)
        self.exit.grid(row = 2, column = 0, sticky = "n", padx = 30, pady = 10)
    
    # Going back to main menu when you press "Back" button
    def main_menu(self):
        self.label.grid(row = 0, column = 0, sticky = "w", padx = 332, pady = 150)
        self.start.grid(row = 1, column = 0, sticky = "n", padx = 30, pady = 10)
        self.exit.grid(row = 2, column = 0, sticky = "n", padx = 30, pady = 10)

        # Forget the gameplay widgets
        if hasattr(self.game, "gameplay"):
            if hasattr(self.game.gameplay, "canvas"):
                self.game.gameplay.canvas.destroy()

        if hasattr(self, "instruction_title"):
            self.instruction_title.grid_forget()

        if hasattr(self, "movement_ins"):
            self.movement_ins.grid_forget()

        if hasattr(self, "start_game"):
            self.start_game.grid_forget()

        if hasattr(self, "back"):
            self.back.grid_forget()

        if hasattr(self, "save_and_quittomenu_button"):
            self.save_and_quittomenu_button.grid_forget()

        if hasattr(self, "game_menu_button"):
            self.game_menu_button.grid_forget()

        if hasattr(self.game, "gameplay") and hasattr(self.game.gameplay, "player"):
            if hasattr(self.game.gameplay, "clock"):
                self.game.gameplay.clock.timer_label.destroy()
                self.game.gameplay.clock.running = False

                if self.game.gameplay.clock.after_id:
                    self.root.after_cancel(self.game.gameplay.clock.after_id)

                self.player = self.game.gameplay.player

            self.widgets = [getattr(self.player, name, None) for name in ["victory_label", "lost_label", "play_again_button", "retry_button", "back_to_menu_button"]]
            for widget in self.widgets:
                if widget:
                    widget.destroy()

    # Exit the game
    def exit_game(self):
        if messagebox.askyesno(title = "Exit", message = "Are you sure you want to go exit?"):
            self.root.destroy()

    # Game instructions for player's movement
    def instruction(self):
        self.instruction_title = tk.Label(self.root, text = "Instructions", fg = "white", bg = "black", font = ("Arial", "45"))
        self.instruction_title.grid(row = 0, column = 0, padx = 438, pady = 75)

        self.movement_ins = tk.Label(self.root, text = "All control movements from the player are:\n\nW - Move Up\nA - Move Left\nS - Move Down\nD - Move Right\n\nArrow Keys - Move in the respective direction", fg = "white", bg = "black", font = ("Arial", "14"))
        self.movement_ins.grid(row = 1, column = 0, sticky = "w", padx = 400, pady = 0)
        self.root.after(3000, self.instruction_buttonsafter)
        
        self.label.grid_forget()
        self.start.grid_forget()
        self.exit.grid_forget()

    def instruction_buttonsafter(self):
        self.start_game_button()
        self.back_button()

    # Start the game after instructions
    def start_game_button(self):
        self.start_game = tk.Button(self.root, text = "Start", font = ("Arial", "18"), command = self.start_messagebox)
        self.start_game.grid(row = 4, column = 0, sticky = "w", padx = 500, pady = 10)

    def start_messagebox(self):
        self.choice = messagebox.askyesnocancel(title = "Start Game", message = "Are you sure you want to start the game?\nYes - Load Game\nNo - New Game")
        
        if self.choice is True:
            self.game.save_system.load_game()
        elif self.choice is False:
            self.game.save_system.new_game()

    # Back to the main menu from main game title
    def back_button(self):
        self.back = tk.Button(self.root, text = "Back", font = ("Arial", "18"), command = self.game.menu.main_menu)
        self.back.grid(row = 4, column = 0, sticky = "e", padx = 500, pady = 10)

    # Game menu button (main)
    def game_menu(self):
        self.game_menu_button = tk.Button(self.root, text = "Game Menu", font = ("Arial", "18"), command = self.game_menu_show_n_hide)
        self.game_menu_button.grid(row = 0, column = 0, sticky = "w", padx = 10, pady = 0)

        self.resume_button = tk.Button(self.root, text = "Resume", font = ("Arial", "18"), command = self.resume_command)
        self.resume_button.grid(row = 0, column = 1, sticky = "n", padx = 345, pady = 0)

        self.restart_button = tk.Button(self.root, text = "Restart", font = ("Arial", "18"), command = self.restart_command)
        self.restart_button.grid(row = 1, column = 2, sticky = "n", padx = 345, pady = 0)

        self.save_and_quittomenu_button = tk.Button(self.root, text = "Save & Quit", font = ("Arial", "18"), command = self.save_and_quit_messagebox)
        self.save_and_quittomenu_button.grid(row = 2, column = 3, sticky = "n", padx = 345, pady = 0)

        self.resume_button.grid_forget()
        self.restart_button.grid_forget()
        self.save_and_quittomenu_button.grid_forget()

    def resume_command(self):
        self.clock = self.game.gameplay.clock

        if not self.clock.running:
            self.clock.running = True
            self.clock.countdown()

    def restart_command(self):
        self.game.seed = random.randint(1, 999999)
        self.game.gameplay.clock.running = False

        if self.game.gameplay.clock.after_id:
            self.root.after_cancel(self.game.gameplay.clock.after_id)

        for widget in [self.resume_button, self.restart_button, self.save_and_quittomenu_button]:
            widget.destroy()

        self.game.gameplay.clock.timer_label.destroy()
        self.game.gameplay.canvas.destroy()

        self.game.start_gameplay()

    # Game menu button with options (show & hide)
    def game_menu_show_n_hide(self):
        self.clock = self.game.gameplay.clock

        if self.clock.running:
            self.clock.running = False
            if self.clock.after_id:
                self.root.after_cancel(self.clock.after_id)

        self.widgets = [self.resume_button, self.restart_button, self.save_and_quittomenu_button]

        for widget in self.widgets:
            if widget.winfo_ismapped():
                widget.grid_forget()
            else:
                widget.grid(row = 0, column = 0, padx = 325, pady = 10, bg = "Black")

    def save_and_quit_messagebox(self):
        try:
            if messagebox.askyesno(title = "Save & Quit", message = "Are you sure you want to save the file & quit the game?"):
                with open("save_game.txt", "w") as file:
                    self.player = self.game.gameplay.player
                    self.clock = self.game.gameplay.clock

                    self.save_data = f"{self.player.row},{self.player.column},{self.clock.time_remaining},{self.game.seed}"
                    file.write(self.save_data)
                    self.main_menu()
        except FileNotFoundError:
            messagebox.showerror(title = "File Not Exist", message = "The file doesn't exist. Create file first before reading.")
        else:
            messagebox.showinfo(title = "Game Saved", message = "Your game file has been saved.")
        finally:
            print("System completed.")

class Gameplay:
    def __init__(self, game):
        self.game = game
        self.root = game.root
        self.menu = self.game.menu

        self.menu.instruction_title.grid_forget()
        self.menu.movement_ins.grid_forget()
        self.menu.start_game.grid_forget()

        self.menu.game_menu()

        self.canvas = tk.Canvas(self.root, width = COLUMNS * CELL_SIZE, height = ROWS * CELL_SIZE, bg = "Black")
        self.canvas.grid(row = 5, column = 0)

        self.maze = Maze(self.game.seed)
        self.maze.draw_maze(self.canvas)
        
        self.player = Player(self.root, self.canvas, self.maze, self)

        self.clock = Clock(self.root, 2, 0, self.player)

        if self.game.saved_row is not None:
            self.player.row = self.game.saved_row
            self.player.column = self.game.saved_column

            self.x = self.game.saved_column * CELL_SIZE
            self.y = self.game.saved_row * CELL_SIZE

            self.canvas.coords(self.player.player_design, self.x + 4, self.y + 4, self.x + CELL_SIZE - 4, self.y + CELL_SIZE -4)

            self.clock.time_remaining = self.game.saved_time_remaining

        self.menu.back.grid_forget()

class SaveSystem:
    def __init__(self, game):
        self.game = game

    def new_game(self):
        self.game.seed = random.randint(1, 999999)
        random.seed(self.game.seed)

        self.game.saved_row = 0
        self.game.saved_column = 0
        self.game.saved_time_remaining = 120

        self.game.start_gameplay()

    def load_game(self):
        try:
            with open("save_game.txt", "r") as file:
                self.row, self.col, self.time_left, self.game.seed = map(int, file.read().split(","))

                self.game.saved_row = self.row
                self.game.saved_column = self.col
                self.game.saved_time_remaining = self.time_left

                random.seed(self.game.seed)
        except FileNotFoundError:
            messagebox.showerror(title = "File Not Exist", message = "The file doesn't exist. Create file first before reading.")
        except ValueError:
            messagebox.showerror(title = "File Not Save", message = "Invalid save file data.")
        else:
            messagebox.showinfo(title = "File Read Successfully", message = "Proceed.")
            self.game.start_gameplay()
        finally:
            print("System completed.")

class Cell():
    def __init__(self, row, column):
        self.row = row
        self.column = column
        self.walls = {
            "Top": True,
            "Bottom": True,
            "Left": True,
            "Right": True
        }
        self.visited = False

    def draw_cells(self, canvas):
        x = self.column * CELL_SIZE
        y = self.row * CELL_SIZE

        if self.walls["Top"]:
            canvas.create_line(x, y, x + CELL_SIZE, y, fill = "White")
        if self.walls["Bottom"]:
            canvas.create_line(x, y + CELL_SIZE, x + CELL_SIZE, y + CELL_SIZE, fill = "White")
        if self.walls["Left"]:
            canvas.create_line(x, y, x, y + CELL_SIZE, fill = "White")
        if self.walls["Right"]:
            canvas.create_line(x + CELL_SIZE, y, x + CELL_SIZE, y + CELL_SIZE, fill = "White")

class Maze():
    def __init__(self, seed):
        self.grid = [[Cell(row, column) for column in range(COLUMNS)] for row in range(ROWS)]
        self.stack = []
        self.current = self.grid[0][0]
        self.current.visited = True
        random.seed(seed)

    # Generate a maze
    def generate_maze(self):
        while True:
            self.neighbors = []
            for direction_row, direction_column, wall, opp in [(-1, 0, "Top", "Bottom"), (1, 0, "Bottom", "Top"), (0, 1, "Right", "Left"), (0, -1, "Left", "Right")]:
                self.n_row = self.current.row + direction_row
                self.n_column = self.current.column + direction_column
                if 0 <= self.n_row < ROWS and 0 <= self.n_column < COLUMNS and not self.grid[self.n_row][self.n_column].visited:
                    self.neighbors.append((self.grid[self.n_row][self.n_column], wall, opp))
            
            if self.neighbors:
                self.next_cell, wall, opp = random.choice(self.neighbors)
                self.current.walls[wall] = False
                self.next_cell.walls[opp] = False
                self.stack.append(self.current)
                self.current = self.next_cell
                self.current.visited = True
            elif self.stack:
                self.current = self.stack.pop()
            else:
                break
        return self.grid

    # Build a maze
    def draw_maze(self, canvas):
        canvas.delete("all")
        self.grid = self.generate_maze()
        for row in self.grid:
            for cell in row:
                cell.draw_cells(canvas)

class Player():
    def __init__(self, root, canvas, maze, gameplay):
        self.color = "Peachpuff"
        self.root = root
        self.canvas = canvas
        self.maze = maze
        self.gameplay = gameplay
        self.game_finished = False

        self.row = 0
        self.column = 0

        # Designing a player
        self.padding = 4
        self.x1 = self.column * CELL_SIZE + self.padding
        self.y1 = self.row * CELL_SIZE + self.padding
        self.x2 = self.x1 + CELL_SIZE - self.padding * 2
        self.y2 = self.y1 + CELL_SIZE - self.padding * 2

        self.player_design = self.canvas.create_oval(self.x1, self.y1, self.x2, self.y2, fill = self.color, width = 2)

        self.win_goal = self.canvas.create_rectangle((COLUMNS - 1) * CELL_SIZE + 5, (ROWS - 1) * CELL_SIZE + 5, COLUMNS * CELL_SIZE - 5, ROWS * CELL_SIZE - 5, fill = "Green")

        for key in ["<Left>", "<Right>", "<Up>", "<Down>", "<a>", "<d>", "<w>", "<s>"]:
            self.root.unbind(key)

        ## Player's movement controls
        # For arrows
        self.root.bind("<Left>", lambda e: self.old_player_movement("Left"))
        self.root.bind("<Right>", lambda e: self.old_player_movement("Right"))
        self.root.bind("<Up>", lambda e: self.old_player_movement("Top"))
        self.root.bind("<Down>", lambda e: self.old_player_movement("Bottom"))

        # For keys (letters)
        self.root.bind("<a>", lambda e: self.old_player_movement("Left"))
        self.root.bind("<d>", lambda e: self.old_player_movement("Right"))
        self.root.bind("<w>", lambda e: self.old_player_movement("Top"))
        self.root.bind("<s>", lambda e: self.old_player_movement("Bottom"))

    # Check movement through the player
    def check_player_movement(self, direction):
        if self.game_finished:
            return

        self.current_cell = self.maze.grid[self.row][self.column]

        if self.current_cell.walls[direction]:
            return

        self.direction_x = 0
        self.direction_y = 0

        if direction == "Left":
            self.column -= 1
            self.direction_x = -CELL_SIZE
        elif direction == "Right":
            self.column += 1
            self.direction_x = CELL_SIZE
        elif direction == "Top":
            self.row -= 1
            self.direction_y = -CELL_SIZE
        elif direction == "Bottom":
            self.row += 1
            self.direction_y = CELL_SIZE

        self.canvas.move(self.player_design, self.direction_x, self.direction_y)

        if self.row == ROWS - 1 and self.column == COLUMNS - 1:
            self.victory_screen()
            
        if self.row == 10 and self.column == 10:
            self.game_over_screen()

    def old_player_movement(self, direction):
        self.old_row = self.row
        self.old_col = self.column

        self.old_x = self.column * CELL_SIZE + CELL_SIZE // 2
        self.old_y = self.row * CELL_SIZE + CELL_SIZE // 2

        self.check_player_movement(direction)

        if self.old_row != self.row or self.old_col != self.column:
            self.new_x = self.column * CELL_SIZE + CELL_SIZE // 2
            self.new_y = self.row * CELL_SIZE + CELL_SIZE // 2

            self.canvas.create_line(self.old_x, self.old_y, self.new_x, self.new_y, fill = "Red", width = 2, dash = (4, 4))

    def victory_screen(self):
        if self.game_finished:
            return
        
        self.game_finished = True
        self.gameplay.clock.running = False

        if self.gameplay.clock.after_id:
            self.root.after_cancel(self.gameplay.clock.after_id)

        self.canvas.grid_forget()
        
        self.victory_label = tk.Label(self.root, text = "You escaped the labyrinth.", fg = "White", bg = "Black", font = ("Helvetica", "40"))
        self.victory_label.grid(row = 3, column = 0, pady = 10)
        self.root.after(3000, self.victory_back_to_menu_buttons)

    def victory_back_to_menu_buttons(self):
        self.play_again_button = tk.Button(self.root, text = "Play Again", font = ("Arial", "18"), command = self.play_again_command)
        self.play_again_button.grid(row = 7, column = 0, pady = 10)

        self.save_n_back_to_main_menu = tk.Button(self.root, text = "Save & Back", font = ("Arial", "18"), command = self.save_and_return)
        self.save_n_back_to_main_menu.grid(row = 8, column = 0, pady = 10)

    def save_and_return(self):
        try:
            self.choice = messagebox.askyesnocancel(title = "Save & Back to Main Menu", message = "Would you like to save it?")
            if self.choice:
                with open("save_game.txt", "w") as file:
                    self.save_data = f"{self.row},{self.column},{self.gameplay.clock.time_remaining},{self.gameplay.game.seed}"
                    file.write(self.save_data)

                messagebox.showinfo(title = "Game Saved", message = "Your game file has been saved.")
            self.gameplay.game.menu.main_menu()
        except FileNotFoundError:
            messagebox.showerror(title = "File Not Exist", message = "The file doesn't exist. Create file first before reading.")
        finally:
            print("System completed.")

    def play_again_command(self):
        self.victory_label.destroy()
        self.play_again_button.destroy()
        self.save_n_back_to_main_menu.destroy()

        self.canvas.destroy()

        self.gameplay.game.start_gameplay()

    def game_over_screen(self):
        if self.game_finished:
            return
        
        self.game_finished = True
        self.gameplay.clock.running = False

        self.gameplay.clock.running = False

        if self.gameplay.clock.after_id:
            self.root.after_cancel(self.gameplay.clock.after_id)

        self.canvas.grid_forget()

        self.lost_label = tk.Label(self.root, text = "YOU LOST.", fg = "Red", bg = "Black", font = ("Helvetica", "40"))
        self.lost_label.grid(row = 3, column = 0, pady = 20)
        self.root.after(3000, self.loss_back_to_menu_buttons)

    def loss_back_to_menu_buttons(self):
        self.retry_button = tk.Button(self.root, text = "Retry", font = ("Arial", "18"), command = self.try_again_command)
        self.retry_button.grid(row = 7, column = 0, pady = 10)

        self.back_to_menu_button = tk.Button(self.root, text = "Back to Main Menu", font = ("Arial", "18"), command = self.back_to_main_menu)
        self.back_to_menu_button.grid(row = 8, column = 0, pady = 10)

    def back_to_main_menu(self):
        self.game.menu.main_menu()
        self.game.menu.game_menu.grid_forget()
        self.clock.timer_label.grid_forget()

    def try_again_command(self):
        self.lost_label.destroy()
        self.retry_button.destroy()
        self.back_to_menu_button.destroy()

        self.canvas.destroy()

        self.gameplay.game.start_gameplay()

class Clock():
    def __init__(self, root, minutes, seconds, player):
        self.root = root
        self.player = player
        self.time_remaining = minutes * 60 + seconds
        self.running = True
        self.after_id = None

        self.timer_label = tk.Label(self.root, text = "00:00", fg = "White", bg = "Black", font = ("Arial", "18"))
        self.timer_label.grid(row = 2, column = 0, pady = 10)

        self.countdown()

    def countdown(self):
        if not self.running or self.player.game_finished:
            return
        
        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60

        self.timer_label.config(text = f"{minutes:02d}:{seconds:02d}")

        if self.time_remaining > 0:
            self.time_remaining -= 1
            self.after_id = self.root.after(1000, self.countdown)
        else:
            self.running = False
            self.player.game_over_screen()

# Main game
if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()
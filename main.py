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
        self.saved_time_remaining = 60

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
        self.instruction_after_id = None

        self.label = tk.Label(self.root, text = "Welcome to the Forgotten Labyrinth!", fg = "white", bg = "black", font = ("Arial", "25"))
        self.label.grid(row = 0, column = 0, sticky = "w", padx = 332, pady = 120)

        self.start = tk.Button(self.root, text = "Play", font = ("Arial", "18"), command = self.instruction)
        self.start.grid(row = 1, column = 0, sticky = "n", padx = 30, pady = 10)

        self.exit = tk.Button(self.root, text = "Exit", font = ("Arial", "18"), command = self.exit_game)
        self.exit.grid(row = 2, column = 0, sticky = "n", padx = 30, pady = 10)

        self.root.grid_columnconfigure(0, weight = 1)
        self.root.grid_columnconfigure(1, weight = 1)
        self.root.grid_columnconfigure(2, weight = 1)
    
    # Going back to main menu when you press "Back" button
    def main_menu(self):
        self.label.grid(row = 0, column = 0, sticky = "w", padx = 332, pady = 150)
        self.start.grid(row = 1, column = 0, sticky = "n", padx = 30, pady = 10)
        self.exit.grid(row = 2, column = 0, sticky = "n", padx = 30, pady = 10)

        self.gameplay = getattr(self.game, "gameplay", None)

        if self.gameplay:
            # Stop clock
            if hasattr(self.gameplay, "clock"):
                self.gameplay.clock.running = False

                if self.gameplay.clock.after_id:
                    try:
                        self.root.after_cancel(self.gameplay.clock.after_id)
                    except:
                        pass

                try:
                    if self.gameplay.clock.timer_label.winfo_exists():
                        self.gameplay.clock.timer_label.destroy()
                except:
                    pass

            # Destroy canvas
            if hasattr(self.gameplay, "canvas"):
                try:
                    if self.gameplay.canvas.winfo_exists():
                        self.gameplay.canvas.destroy()
                except:
                    pass

            # Destroy player frames
            if hasattr(self.gameplay, "player"):
                player = self.gameplay.player

                if hasattr(player, "screen_after_id") and player.screen_after_id:
                    try:
                        self.root.after_cancel(player.screen_after_id)
                    except:
                        pass

                for frame_name in ["victory_frame", "lost_frame"]:
                    frame = getattr(player, frame_name, None)

                    if frame:
                        try:
                            if frame.winfo_exists():
                                frame.destroy()
                        except:
                            pass

        # Remove instruction U.I.
        for widget_name in ["instruction_title", "movement_ins", "start_game", "back"]:
            widget = getattr(self, widget_name, None)

            if widget:
                try:
                    widget.grid_forget()
                except:
                    pass

        # Remove game menu buttons
        for widget_name in ["pause_resume_button", "restart_button", "save_and_quittomenu_button"]:
            widget = getattr(self, widget_name, None)

            if widget:
                try:
                    if widget.winfo_exists():
                        widget.grid_forget()
                except tk.TclError:
                    pass

        if self.instruction_after_id:
            try:
                self.root.after_cancel(self.instruction_after_id)
            except tk.TclError:
                pass

            self.instruction_after_id = None

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

        if self.instruction_after_id:
            try:
                self.root.after_cancel(self.instruction_after_id)
            except tk.TclError:
                pass

        self.instruction_after_id = self.root.after(3000, self.instruction_buttonsafter)
        
        self.label.grid_forget()
        self.start.grid_forget()
        self.exit.grid_forget()

    def instruction_buttonsafter(self):
        if not self.root.winfo_exists():
            return
        if not hasattr(self, "movement_ins"):
            return
        
        try:
            if not self.movement_ins.winfo_exists():
                return
        except:
            return

        self.start_game_button()
        self.back_button()

    # Start the game after instructions
    def start_game_button(self):
        self.start_game = tk.Button(self.root, text = "Start", font = ("Arial", "18"), command = self.start_messagebox)
        self.start_game.grid(row = 4, column = 0, sticky = "w", padx = 500, pady = 10)

    def start_messagebox(self):
        self.choice = messagebox.askyesnocancel(title = "Start Game", message = "Are you sure you want to start a new game?\nYes - New Game\nNo - Load Game")
        
        if self.choice is True:
            self.game.save_system.new_game()
        elif self.choice is False:
            self.game.save_system.load_game()

    # Back to the main menu from main game title
    def back_button(self):
        self.back = tk.Button(self.root, text = "Back", font = ("Arial", "18"), command = self.game.menu.main_menu)
        self.back.grid(row = 4, column = 0, sticky = "e", padx = 500, pady = 10)

    # Game menu button (main)
    def game_menu(self):
        if not hasattr(self, "pause_resume_button"):
            self.pause_resume_button = tk.Button(self.root, text = "Stop", font = ("Arial", 18), command = self.pause_resume_command)
            self.restart_button = tk.Button(self.root, text = "Restart", font = ("Arial", 18), command = self.restart_command)
            self.save_and_quittomenu_button = tk.Button(self.root, text = "Save & Quit", font = ("Arial", 18), command = self.save_and_quit_messagebox)

        self.pause_resume_button.config(text = "Stop")

        self.pause_resume_button.grid(row = 0, column = 0, pady = 10)
        self.restart_button.grid(row = 0, column = 1, pady = 10)
        self.save_and_quittomenu_button.grid(row = 0, column = 2, pady = 10)

    def pause_resume_command(self):
        gameplay = self.game.gameplay
        clock = gameplay.clock

        # Pause/stop button
        if not gameplay.paused:
            gameplay.paused = True
            clock.running = False

            if clock.after_id:
                self.root.after_cancel(clock.after_id)
                clock.after_id = None
            self.pause_resume_button.config(text = "Play")

        # Resume/play button
        else:
            gameplay.paused = False
            clock.running = True

            self.pause_resume_button.config(text = "Stop")

            clock.countdown()

    def restart_command(self):
        gameplay = self.game.gameplay

        gameplay.clock.running = False

        if gameplay.clock.after_id:
            self.root.after_cancel(gameplay.clock.after_id)
            gameplay.clock.after_id = None

        try:
            if gameplay.clock.timer_label.winfo_exists():
                gameplay.clock.timer_label.destroy()
        except tk.TclError:
            pass

        gameplay.canvas.destroy()

        self.hide_game_menu()

        self.game.saved_row = 0
        self.game.saved_column = 0
        self.game.saved_time_remaining = 60

        self.game.seed = random.randint(1, 999999)

        del self.game.gameplay

        self.game.start_gameplay()

    def save_and_quit_messagebox(self):
        try:
            if messagebox.askyesno(title = "Save & Quit", message = "Are you sure you want to quit by saving a file?"):
                with open("save_game.txt", "w") as file:
                    self.player = self.game.gameplay.player
                    self.clock = self.game.gameplay.clock

                    self.save_data = f"{self.player.row},{self.player.column},{self.clock.time_remaining},{self.game.seed}"
                    file.write(self.save_data)
                    self.game.menu.main_menu()
        except FileNotFoundError:
            messagebox.showerror(title = "File Not Exist", message = "The file doesn't exist. Create file first before reading.")
        else:
            messagebox.showinfo(title = "Game Saved", message = "Your game file has been saved.")
        finally:
            print("System completed.")

    def hide_game_menu(self):
        if hasattr(self, "pause_resume_button"):
            self.pause_resume_button.grid_forget()

        if hasattr(self, "restart_button"):
            self.restart_button.grid_forget()

        if hasattr(self, "save_and_quittomenu_button"):
            self.save_and_quittomenu_button.grid_forget()

class Gameplay:
    def __init__(self, game):
        self.game = game
        self.root = game.root
        self.menu = self.game.menu

        self.paused = False

        self.menu.instruction_title.grid_forget()
        self.menu.movement_ins.grid_forget()
        self.menu.start_game.grid_forget()

        self.menu.game_menu()

        self.canvas = tk.Canvas(self.root, width = COLUMNS * CELL_SIZE, height = ROWS * CELL_SIZE, bg = "Black")
        self.canvas.grid(row = 2, column = 1, pady = 10)

        self.maze = Maze(self.game.seed)
        self.maze.draw_maze(self.canvas)
        
        self.player = Player(self.root, self.canvas, self.maze, self)

        self.clock = Clock(self.root, 1, 0, self.player)

        if (self.game.saved_row > 0 or self.game.saved_column > 0 or self.game.saved_time_remaining < 120):
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
        self.game.saved_time_remaining = 60

        self.game.start_gameplay()

    def load_game(self):
        try:
            with open("save_game.txt", "r") as file:
                row, column, time_remaining, seed = map(int, file.read().split(","))

                self.game.saved_row = row
                self.game.saved_column = column
                self.game.saved_time_remaining = time_remaining
                self.game.seed = seed

                random.seed(seed)
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
        self.random = random.Random(seed)

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
                self.next_cell, wall, opp = self.random.choice(self.neighbors)
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
        self.can_move = True
        self.move_after_id = None
        self.screen_after_id = None

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
        try:
            if not self.canvas.winfo_exists():
                return
        except tk.TclError:
            return

        if self.gameplay.paused:
            return
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

    def old_player_movement(self, direction):
        if self.game_finished:
            return

        try:
            if not self.canvas.winfo_exists():
                return
        except tk.TclError:
            return

        if self.gameplay.paused:
            return
        if not self.can_move:
            return

        self.can_move = False

        self.old_row = self.row
        self.old_col = self.column

        self.old_x = self.column * CELL_SIZE + CELL_SIZE // 2
        self.old_y = self.row * CELL_SIZE + CELL_SIZE // 2

        self.check_player_movement(direction)

        try:
            if (self.canvas.winfo_exists()) and (self.old_row != self.row or self.old_col != self.column):
                self.new_x = self.column * CELL_SIZE + CELL_SIZE // 2
                self.new_y = self.row * CELL_SIZE + CELL_SIZE // 2

                self.canvas.create_line(self.old_x, self.old_y, self.new_x, self.new_y, fill = "Red", width = 2, dash = (4, 4))
        except tk.TclError:
            return

        self.move_after_id = self.root.after(220, self.reset_move)

    def reset_move(self):
        if self.game_finished:
            return
        self.can_move = True

    def victory_screen(self):
        if self.game_finished:
            return
        
        self.game_finished = True
        self.gameplay.game.menu.hide_game_menu()

        self.gameplay.clock.running = False

        if self.gameplay.clock.after_id:
            self.root.after_cancel(self.gameplay.clock.after_id)

        try:
            if self.gameplay.clock.timer_label.winfo_exists():
                self.gameplay.clock.timer_label.destroy()
        except tk.TclError:
            pass

        for key in ["<Left>", "<Right>", "<Up>", "<Down>", "<a>", "<d>", "<w>", "<s>"]:
            self.root.unbind(key)
        
        if self.move_after_id:
            self.root.after_cancel(self.move_after_id)
            self.move_after_id = None

        if self.canvas.winfo_exists():
            self.canvas.destroy()
        
        self.victory_frame = tk.Frame(self.root, bg = "Black")
        self.victory_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.victory_label = tk.Label(self.victory_frame, text = "You escaped the labyrinth.", fg = "White", bg = "Black", font = ("Helvetica", "40"))
        self.victory_label.pack(pady = 20)

        self.screen_after_id = self.root.after(3000, self.victory_back_to_menu_buttons)

    def victory_back_to_menu_buttons(self):
        if not hasattr(self, "victory_frame"):
            return
        if not self.victory_frame.winfo_exists():
            return

        self.play_again_button = tk.Button(self.victory_frame, text = "Play Again", font = ("Arial", "18"), command = self.play_again_command)
        self.play_again_button.pack(pady = 10)

        self.back_to_menu_button = tk.Button(self.victory_frame, text = "Back to Main Menu", font = ("Arial", "18"), command = self.back_to_main_menu)
        self.back_to_menu_button.pack(pady = 10)

    def play_again_command(self):
        if self.screen_after_id:
            self.root.after_cancel(self.screen_after_id)
            self.screen_after_id = None

        self.victory_frame.destroy()

        self.gameplay.game.saved_row = 0
        self.gameplay.game.saved_column = 0
        self.gameplay.game.saved_time_remaining = 60

        self.gameplay.game.seed = random.randint(1, 999999)

        self.gameplay.game.start_gameplay()

    def game_over_screen(self):
        if self.game_finished:
            return
        
        self.game_finished = True
        self.gameplay.game.menu.hide_game_menu()

        self.gameplay.clock.running = False

        if self.gameplay.clock.after_id:
            self.root.after_cancel(self.gameplay.clock.after_id)

        try:
            if self.gameplay.clock.timer_label.winfo_exists():
                self.gameplay.clock.timer_label.destroy()
        except tk.TclError:
            pass

        for key in ["<Left>", "<Right>", "<Up>", "<Down>", "<a>", "<d>", "<w>", "<s>"]:
            self.root.unbind(key)

        if self.move_after_id:
            self.root.after_cancel(self.move_after_id)
            self.move_after_id = None

        if self.canvas.winfo_exists():
            self.canvas.destroy()

        self.lost_frame = tk.Frame(self.root, bg = "Black")
        self.lost_frame.place(relx = 0.5, rely = 0.5, anchor = "center")

        self.lost_label = tk.Label(self.lost_frame, text = "YOU LOST.", fg = "Red", bg = "Black", font = ("Helvetica", "40"))
        self.lost_label.pack(pady = 20)

        self.screen_after_id = self.root.after(3000, self.loss_back_to_menu_buttons)

    def loss_back_to_menu_buttons(self):
        if not hasattr(self, "lost_frame"):
            return
        if not self.loss_frame.winfo_exists():
            return

        self.retry_button = tk.Button(self.lost_frame, text = "Retry", font = ("Arial", "18"), command = self.try_again_command)
        self.retry_button.pack(pady = 10)

        self.back_to_menu_button = tk.Button(self.lost_frame, text = "Back to Main Menu", font = ("Arial", "18"), command = self.back_to_main_menu)
        self.back_to_menu_button.pack(pady = 10)

    def back_to_main_menu(self):
        self.gameplay.game.menu.main_menu()

    def try_again_command(self):
        if self.screen_after_id:
            self.root.after_cancel(self.screen_after_id)
            self.screen_after_id = None

        self.lost_frame.destroy()

        self.gameplay.game.saved_row = 0
        self.gameplay.game.saved_column = 0
        self.gameplay.game.saved_time_remaining = 60

        self.gameplay.game.seed = random.randint(1, 999999)

        self.gameplay.game.start_gameplay()

class Clock():
    def __init__(self, root, minutes, seconds, player):
        self.root = root
        self.player = player
        self.time_remaining = minutes * 60 + seconds
        self.running = True
        self.after_id = None

        self.timer_label = tk.Label(self.root, text = "00:00", fg = "White", bg = "Black", font = ("Arial", "18"))
        self.timer_label.grid(row = 1, column = 1, pady = 10)

        self.countdown()

    def countdown(self):
        if not self.running:
            self.after_id = None
            return

        if self.player.game_finished:
            self.after_id = None
            return

        minutes = self.time_remaining // 60
        seconds = self.time_remaining % 60

        self.timer_label.config(text=f"{minutes:02d}:{seconds:02d}")

        if self.time_remaining <= 0:
            self.running = False

            if self.after_id:
                self.root.after_cancel(self.after_id)
                self.after_id = None
            if not self.player.game_finished:
                self.player.game_over_screen()
                return

        self.time_remaining -= 1

        self.after_id = self.root.after(1000, self.countdown)

# Main game
if __name__ == "__main__":
    root = tk.Tk()
    Game(root)
    root.mainloop()
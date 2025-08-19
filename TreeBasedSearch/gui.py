import tkinter as tk


class MazeGUI:
    def __init__(self, maze, cell_size=40):
        self.maze = maze
        self.cell_size = cell_size

        self.window = tk.Tk()
        self.window.title("Maze Solver Visualization")

        w = maze.cols * self.cell_size
        h = maze.rows * self.cell_size
        self.canvas = tk.Canvas(self.window, width=w, height=h, bg="white")
        self.canvas.pack()

        # Draw background
        for row in range(self.maze.rows):
            for col in range(self.maze.cols):
                x1, y1 = col * self.cell_size, row * self.cell_size
                x2, y2 = (col + 1) * self.cell_size, (row + 1) * self.cell_size

                if (col, row) in self.maze.walls:
                    color = "gray"
                elif (col, row) == self.maze.start:
                    color = "red"
                elif (col, row) in self.maze.goal:
                    color = "green"
                else:
                    color = "white"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=color, outline="black")

    def update_cell(self, state, color):
        x, y = state
        x1, y1 = x * self.cell_size, y * self.cell_size
        x2, y2 = (x + 1) * self.cell_size, (y + 1) * self.cell_size
        self.canvas.create_rectangle(
            x1, y1, x2, y2, fill=color, outline="black")

    def start(self, method="dfs", max_depth=9999):
        self.window.after(100, lambda: self.maze.solve(method=method,
                                                       gui=self,
                                                       max_depth=max_depth))
        self.window.mainloop()

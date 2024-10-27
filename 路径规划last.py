import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
import numpy as np

class DFSPathPlanner:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.grid = np.zeros((height, width))

    def add_random_obstacles(self, num_obstacles):
        obstacles = np.random.randint(1, min(self.width, self.height) - 1, size=(num_obstacles, 2))
        for obstacle in obstacles:
            x, y = obstacle
            self.grid[y][x] = 1

    def is_obstacle(self, x, y):
        return self.grid[y][x] == 1

    def is_valid_position(self, x, y):
        return 0 <= x < self.width and 0 <= y < self.height

    def plan_path(self, start):
        visited = np.zeros((self.height, self.width))
        path = []
        self.dfs(start[0], start[1], visited, path)
        return path

    def dfs(self, x, y, visited, path):
        if not self.is_valid_position(x, y) or visited[y][x] == 1 or self.is_obstacle(x, y):
            return

        visited[y][x] = 1
        path.append((x, y))

        self.dfs(x + 1, y, visited, path)  # 向右移动
        self.dfs(x, y + 1, visited, path)  # 向下移动
        self.dfs(x - 1, y, visited, path)  # 向左移动
        self.dfs(x, y - 1, visited, path)  # 向上移动

    def animate_path(self, start, filename):
        fig, ax = plt.subplots()
        ax.set_xlim(-0.5, self.width - 0.5)
        ax.set_ylim(-0.5, self.height - 0.5)
        ax.set_xticks(np.arange(0, self.width, 1))
        ax.set_yticks(np.arange(0, self.height, 1))
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.grid(color='k', linestyle='-', linewidth=1)

        obstacles = np.where(self.grid == 1)
        ax.scatter(obstacles[1], obstacles[0], color='red', marker='s')

        visited = np.zeros((self.height, self.width))
        path = self.plan_path(start)

        for x, y in path:
            visited[y][x] = 1

        line, = ax.plot([], [], color='blue')

        def update(frame):
            x_values = []
            y_values = []

            for y in range(self.height):
                for x in range(self.width):
                    if visited[y][x] == 1 and not self.is_obstacle(x, y):
                        x_values.append(x)
                        y_values.append(y)

            line.set_data(x_values, y_values)
            return line,

        anim = FuncAnimation(fig, update, frames=len(path), blit=True)

        anim.save(filename, writer='pillow')

path_planner = DFSPathPlanner(width=10, height=10)

num_obstacles = 10
path_planner.add_random_obstacles(num_obstacles)

start = (0, 0)
filename = r'C:\d盘\大学\学习study\大一\土木机器人检测课题\zuixin\动图15.gif'
path_planner.animate_path(start, filename)
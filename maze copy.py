import pygame
import random
from collections import deque

# Initialize Pygame
pygame.init()

class Maze:
    def __init__(self, maze_size, num_treasures, block_size):
        self.maze_size = maze_size
        self.block_size = block_size
        self.grid = [[0] * maze_size for _ in range(maze_size)]  # Initialize empty grid
        self.player_pos = [random.randint(0, maze_size - 1), random.randint(0, maze_size - 1)]
        self.treasures = self.generate_treasures(num_treasures)
        self.water = self.generate_water()
        self.walls = self.generate_walls()


    def generate_treasures(self, num_treasures):
        treasures = []
        for _ in range(num_treasures):
            while True:
                treasure = [random.randint(0, self.maze_size - 1), random.randint(0, self.maze_size - 1)]
                if treasure not in treasures and treasure != self.player_pos:
                    treasures.append(treasure)
                    break
        return treasures

    def generate_walls(self):
        walls = []
        for i in range(1, self.maze_size - 1):
            for j in range(1, self.maze_size - 1):
                if [i, j] != self.player_pos and [i, j] not in self.treasures and random.choice([True, False, False]):
                    walls.append([i, j])
                    self.grid[i][j] = 1  # Mark the wall in the grid
        return walls

    def generate_water(self):
        water = []
        water_size = min(self.maze_size, self.maze_size) // 4
        start_x = random.randint(0, self.maze_size - water_size)
        start_y = random.randint(0, self.maze_size - water_size)

        for i in range(start_x, start_x + water_size):
            for j in range(start_y, start_y + water_size):
                water.append([i, j])
                self.grid[i][j] = 2  # Mark the water in the grid
        return water

    def is_valid_move(self, pos):
        return 0 <= pos[0] < self.maze_size and 0 <= pos[1] < self.maze_size and self.grid[pos[0]][pos[1]] != 1

    def bfs(self, start, goal):
        queue = deque([(start, [])])
        visited = set()

        while queue:
            current, path = queue.popleft()

            if current == goal:
                return path

            if current in visited:
                continue

            visited.add(current)

            for neighbor in self.get_neighbors(current):
                queue.append((neighbor, path + [neighbor]))

        return []

    def get_neighbors(self, pos):
        neighbors = [(pos[0] + 1, pos[1]), (pos[0] - 1, pos[1]), (pos[0], pos[1] + 1), (pos[0], pos[1] - 1)]
        return [neighbor for neighbor in neighbors if self.is_valid_move(neighbor)]

def move_player(maze):
    global player_pos
    if random.randint(0, 5500) == 0:
        return 'GIVEUP'

    # Utilize o algoritmo BFS para encontrar o tesouro mais próximo
    nearest_treasure, path_to_treasure = find_nearest_treasure_with_path(maze)
    #path_to_treasure = maze.bfs(tuple(maze.player_pos), tuple(nearest_treasure)) if nearest_treasure else []
    print(steps)   
    if path_to_treasure:
        
        next_pos = path_to_treasure[0]
        return 'UP' if next_pos[1] < maze.player_pos[1] else 'DOWN' if next_pos[1] > maze.player_pos[1] else \
               'LEFT' if next_pos[0] < maze.player_pos[0] else 'RIGHT'
    else:
        return random.choice(['UP', 'DOWN', 'LEFT', 'RIGHT'])

def find_nearest_treasure_with_path(maze):
    nearest_treasure = None
    nearest_path = None
    nearest_distance = float('inf')

    for treasure in maze.treasures:
        path_to_treasure = maze.bfs(tuple(maze.player_pos), tuple(treasure))
        if path_to_treasure and len(path_to_treasure) < nearest_distance:
            nearest_treasure = treasure
            nearest_path = path_to_treasure
            nearest_distance = len(path_to_treasure)

    return nearest_treasure, nearest_path

# Maze dimensions
width, height = 800, 800
maze_size = 20  # Adjust for a more complex maze
block_size = width // maze_size

# Define colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

NUM_TREASURES = 10

# Set up the display
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption('Maze Treasure Hunt')

# Load treasure image
treasure_image = pygame.image.load('treasure.png')
treasure_image = pygame.transform.scale(treasure_image, (block_size, block_size))

# Inicialize o objeto do labirinto
maze = Maze(maze_size, NUM_TREASURES, block_size)

# Game loop
running = True
score = 0
steps = 0
while running:
    direction = move_player(maze)
    score -= 1
    
    next_pos = maze.player_pos
    if direction == 'UP':
        next_pos = (maze.player_pos[0], maze.player_pos[1] - 1) 
    elif direction == 'DOWN':
        next_pos = (maze.player_pos[0], maze.player_pos[1] + 1) 
    elif direction == 'LEFT':
        next_pos = (maze.player_pos[0] - 1, maze.player_pos[1]) 
    elif direction == 'RIGHT':
        next_pos = (maze.player_pos[0] + 1, maze.player_pos[1]) 
    elif direction == "NONE":
        score += 1
        steps -= 1
    else:
        print("Giving up")
        running = False;   
    
    px, py = next_pos
    if maze.is_valid_move(next_pos) and next_pos not in maze.walls:
        maze.player_pos = next_pos
    else:
        print("Invalid move!", next_pos)
        continue 

    if [px,py] in maze.water:
        score -=5
        print("Passou pela agua")       

    screen.fill(BLACK)
    for row in range(maze.maze_size):
        for col in range(maze.maze_size):
            rect = pygame.Rect(col * block_size, row * block_size, block_size, block_size)
            if [col, row] in maze.walls:
                pygame.draw.rect(screen, BLACK, rect)
            elif [col, row] in maze.water:
                pygame.draw.rect(screen, BLUE, rect)
            else:
                pygame.draw.rect(screen, WHITE, rect)
            if [col, row] == [px, py]:
                pygame.draw.rect(screen, RED, rect)
            elif [col, row] in maze.treasures:
                pygame.draw.rect(screen, WHITE, rect)
                screen.blit(treasure_image, (col * block_size, row * block_size))

    if [px, py] in maze.treasures:
        maze.treasures.remove([px, py])
        print("Treasure found! Treasures left:", len(maze.treasures))

    if not maze.treasures:
        print("All treasures collected!")
        running = False

    if steps >= 80:
        print(f"Maximum number of steps {steps}")
        running = False

    pygame.display.flip()
    pygame.time.wait(100)
    steps += 1

found_treasures = NUM_TREASURES - len(maze.treasures)
print(f"Found {found_treasures} treasures")
final_score = (found_treasures * 500) + score
print(f"Final score: {final_score}")
pygame.quit()

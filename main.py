import pygame
import random

pygame.init()

done = False
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

cols = 20
rows = 20

# Calculate base width and height of each cell
base_wr = 15
base_hr = 15

# Calculate width and height based on cols and rows
width = cols * base_wr
height = rows * base_hr

screen = pygame.display.set_mode([width, height])
pygame.display.set_caption("Maze")
clock = pygame.time.Clock()


class Spot:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.f = 0
        self.g = 0
        self.h = 0
        self.neighbors = []
        self.visited = False
        self.walls = [True, True, True, True]

    def show(self, color=BLACK):
        zoomed_wr = base_wr * zoom_factor
        zoomed_hr = base_hr * zoom_factor
        
        screen_x = self.x * zoomed_wr + screen_x_offset
        screen_y = self.y * zoomed_hr + screen_y_offset
        
        if self.walls[0]:
            pygame.draw.line(screen, color, [screen_x, screen_y], [screen_x + zoomed_wr, screen_y], 2)
        if self.walls[1]:
            pygame.draw.line(screen, color, [screen_x + zoomed_wr, screen_y], [screen_x + zoomed_wr, screen_y + zoomed_hr], 2)
        if self.walls[2]:
            pygame.draw.line(screen, color, [screen_x + zoomed_wr, screen_y + zoomed_hr], [screen_x, screen_y + zoomed_hr], 2)
        if self.walls[3]:
            pygame.draw.line(screen, color, [screen_x, screen_y + zoomed_hr], [screen_x, screen_y], 2)

    def show_block(self, color):
        if self.visited:
            zoomed_wr = base_wr * zoom_factor
            zoomed_hr = base_hr * zoom_factor
            
            screen_x = self.x * zoomed_wr + screen_x_offset
            screen_y = self.y * zoomed_hr + screen_y_offset
            
            pygame.draw.rect(screen, color, [screen_x + 2, screen_y + 2, zoomed_wr - 2, zoomed_hr - 2])

    def add_neighbors(self):
        if self.x > 0:
            self.neighbors.append(grid[self.x - 1][self.y])
        if self.y > 0:
            self.neighbors.append(grid[self.x][self.y - 1])
        if self.x < rows - 1:
            self.neighbors.append(grid[self.x + 1][self.y])
        if self.y < cols - 1:
            self.neighbors.append(grid[self.x][self.y + 1])


grid = [[Spot(i, j) for j in range(cols)] for i in range(rows)]

for i in range(rows):
    for j in range(cols):
        grid[i][j].add_neighbors()

current = grid[0][0]
visited = [current]
completed = False

zoom_factor = 1.0  # Zoom factor, 1.0 is default (no zoom)
screen_x_offset = 0  # Horizontal screen offset
screen_y_offset = 0  # Vertical screen offset

def break_walls(a, b):
    if a.y == b.y and a.x > b.x:
        grid[b.x][b.y].walls[1] = False
        grid[a.x][a.y].walls[3] = False
    if a.y == b.y and a.x < b.x:
        grid[a.x][a.y].walls[1] = False
        grid[b.x][b.y].walls[3] = False
    if a.x == b.x and a.y < b.y:
        grid[b.x][b.y].walls[0] = False
        grid[a.x][a.y].walls[2] = False
    if a.x == b.x and a.y > b.y:
        grid[a.x][a.y].walls[0] = False
        grid[b.x][b.y].walls[2] = False


while not done:
    clock.tick(15)
    screen.fill(BLACK)
    
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_i:
                zoom_factor += 0.1  # Zoom in
            elif event.key == pygame.K_o:
                if zoom_factor > 0.2:  # Limit minimum zoom factor to avoid too small cells
                    zoom_factor -= 0.1  # Zoom out
            elif event.key == pygame.K_UP:
                screen_y_offset += base_hr * zoom_factor  # Move screen up
            elif event.key == pygame.K_DOWN:
                screen_y_offset -= base_hr * zoom_factor  # Move screen down
            elif event.key == pygame.K_LEFT:
                screen_x_offset += base_wr * zoom_factor  # Move screen left
            elif event.key == pygame.K_RIGHT:
                screen_x_offset -= base_wr * zoom_factor  # Move screen right

    if not completed:
        grid[current.x][current.y].visited = True
        got_new = False
        temp = 10

        while not got_new and not completed:
            r = random.randint(0, len(current.neighbors) - 1)
            temp_current = current.neighbors[r]
            if not temp_current.visited:
                visited.append(current)
                current = temp_current
                got_new = True
            if temp == 0:
                temp = 10
                if len(visited) == 0:
                    completed = True
                    break
                else:
                    current = visited.pop()
            temp -= 1

        if not completed:
            break_walls(current, visited[len(visited) - 1])

        for i in range(rows):
            for j in range(cols):
                grid[i][j].show(GREEN)
                # grid[i][j].show_block(RED)

        current.visited = True
        current.show_block(RED)
        pygame.display.flip()

pygame.quit()

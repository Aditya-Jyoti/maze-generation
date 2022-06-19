import pygame 
import random
from typing import Tuple, List


pygame.init()
CELL_SIZE = 25
NUM_ROWCOLS = 25

BLACK = (  0,   0,   0)
WHITE = (255, 255, 255)
BLUE =  (  0,   0, 255)

class Node:
    def __init__(self, position: Tuple[int, int]) -> None:
        self.x_pos, self.y_pos = position
        self.node_state = "unvisited"

        self.walls_coordinates = {
            "top":      ((self.x_pos    , self.y_pos    ), (self.x_pos + 1, self.y_pos    )),
            "bottom":   ((self.x_pos    , self.y_pos + 1), (self.x_pos + 1, self.y_pos + 1)),
            "left":     ((self.x_pos    , self.y_pos    ), (self.x_pos    , self.y_pos + 1)),
            "right":    ((self.x_pos + 1, self.y_pos    ), (self.x_pos + 1, self.y_pos + 1))
        }
        self.active_walls = ["top", "bottom", "left", "right"]
    
def draw_screen(screen: pygame.Surface, grid: List[List[Node]]) -> None:
    for row in grid:
        for node in row:
            if node.node_state == "unvisited":
                rect = pygame.Rect(node.x_pos * CELL_SIZE, node.y_pos * CELL_SIZE, float(CELL_SIZE), float(CELL_SIZE))
                pygame.draw.rect(screen, BLACK, rect) 

            if node.node_state == "visited":
                rect = pygame.Rect(node.x_pos * CELL_SIZE, node.y_pos * CELL_SIZE, float(CELL_SIZE), float(CELL_SIZE))
                pygame.draw.rect(screen, WHITE, rect) 

            for active_wall in node.active_walls:
                left_coord, right_coord = node.walls_coordinates[active_wall]
                x1, y1 = left_coord
                x2, y2 = right_coord
                pygame.draw.line(screen, BLACK, (x1 * CELL_SIZE, y1 * CELL_SIZE), (x2 * CELL_SIZE, y2 * CELL_SIZE), width= 3)

def main(initial_node_position: Tuple[int, int]) -> None:
    grid = [[Node((x, y)) for x in range(NUM_ROWCOLS)] for y in range(NUM_ROWCOLS)]

    window_size = (NUM_ROWCOLS*CELL_SIZE, NUM_ROWCOLS*CELL_SIZE)
    screen = pygame.display.set_mode(window_size)
    screen.fill((0, 0, 0))
    clock = pygame.time.Clock()
    
    initial_node = grid[initial_node_position[1]][initial_node_position[0]]
    initial_node.node_state = "visited"
    grid[initial_node_position[1]][initial_node_position[0]] = initial_node

    stack = [initial_node]

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False 
            
        while stack: 
            draw_screen(screen, grid)
            pygame.display.update()

            chosen_node = stack.pop()
            coords = [
                ((chosen_node.x_pos - 1, chosen_node.y_pos    ), "left"), 
                ((chosen_node.x_pos    , chosen_node.y_pos - 1), "top"),
                ((chosen_node.x_pos + 1, chosen_node.y_pos    ), "right"),
                ((chosen_node.x_pos    , chosen_node.y_pos + 1), "bottom")
            ]
            neighbours = []

            for pos, name in coords:
                x, y = pos
                if not (0 <= x < len(grid) and 0 <= y < len(grid)):
                    continue

                if grid[y][x].node_state == "unvisited":
                    neighbours.append((grid[y][x], name))

            if neighbours:
                opposites = {
                    "left": "right",
                    "right": "left",
                    "top": "bottom",
                    "bottom": "top"
                }
                stack.append(chosen_node)
                neighbour = random.choice(neighbours)
                neighbour_node = neighbour[0]
                chosen_node.active_walls.pop(chosen_node.active_walls.index(neighbour[1]))
                neighbour_node.active_walls.pop(neighbour_node.active_walls.index(opposites[neighbour[1]]))
                neighbour_node.node_state = "visited"
                stack.append(neighbour_node)
                
                grid[neighbour_node.y_pos][neighbour_node.x_pos] = neighbour_node
            
            grid[chosen_node.y_pos][chosen_node.y_pos] = chosen_node

        clock.tick(60)
        pygame.display.update()

if __name__ == "__main__":
    main((0, 0))


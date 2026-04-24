import pygame
import random
import sys

TILE_SIZE = 32
SCREEN_WIDTH = 20 * TILE_SIZE  
SCREEN_HEIGHT = 20 * TILE_SIZE
COLORS = {
    "wall": (40, 40, 40),
    "player": (0, 200, 100),
    "bg": (20, 20, 20)
}

class GameObject:
    def __init__(self, x, y, color):
        self.rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Wall(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, COLORS["wall"])

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, COLORS["player"])
        self._speed = 1 

    def move(self, dx, dy, walls):
        new_rect = self.rect.move(dx * TILE_SIZE, dy * TILE_SIZE)
        if not any(wall.rect.colliderect(new_rect) for wall in walls):
            self.rect = new_rect

class GameObjectFactory:
    @staticmethod
    def create_object(char, x, y):
        if char == '1':
            return Wall(x, y)
        elif char == 'P':
            return Player(x, y)
        return None

class DungeonManager:
    def __init__(self):
        self.walls = []
        self.player = None

    def combine_segments(self, segment_files, output_file):
        chosen = [random.choice(segment_files) for _ in range(4)]
        segments = []
        for f_name in chosen:
            with open(f_name, 'r') as f:
                segments.append([line.strip() for line in f.readlines()])

        with open(output_file, 'w') as out:
            for i in range(10):
                out.write(segments[0][i] + segments[1][i] + "\n")
            for i in range(10):
                line = segments[2][i] + segments[3][i] 
                if i == 5 and "P" not in "".join(segments[0]):
                    line = line[:5] + "P" + line[6:]
                out.write(line + "\n")

    def load_map(self, filename):
        self.walls = []
        with open(filename, 'r') as f:
            for y, line in enumerate(f):
                for x, char in enumerate(line.strip()):
                    obj = GameObjectFactory.create_object(char, x, y)
                    if isinstance(obj, Wall):
                        self.walls.append(obj)
                    elif isinstance(obj, Player):
                        self.player = obj

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("OOP Coursework 2026 - Dungeon Crawler")
        self.clock = pygame.time.Clock()
        
        self.manager = DungeonManager()
        self.setup_game()

    def setup_game(self):
        seg_files = ["seg1.txt", "seg2.txt", "seg3.txt", "seg4.txt"]
        self.manager.combine_segments(seg_files, "final_map.txt")
        self.manager.load_map("final_map.txt")
        
        if not self.manager.player:
            self.manager.player = Player(1, 1)

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                if event.type == pygame.KEYDOWN:
                    dx, dy = 0, 0
                    if event.key == pygame.K_UP: dy = -1
                    elif event.key == pygame.K_DOWN: dy = 1
                    elif event.key == pygame.K_LEFT: dx = -1
                    elif event.key == pygame.K_RIGHT: dx = 1
                    
                    self.manager.player.move(dx, dy, self.manager.walls)

            self.screen.fill(COLORS["bg"])
            for wall in self.manager.walls:
                wall.draw(self.screen)
            self.manager.player.draw(self.screen)
            
            pygame.display.flip()
            self.clock.tick(60)
        
        pygame.quit()

if __name__ == "__main__":
    Game().run()
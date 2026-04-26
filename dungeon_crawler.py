import pygame
import random
import sys

#Konstantos
TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = 20, 20
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

COLORS = {
    "bg": (15, 15, 25),
    "hp_bar": (0, 255, 0),
    "hp_bg": (100, 0, 0),
    "text": (255, 255, 255),
    "dash_indicator": (255, 255, 0)
}

# Bazinė klasė
class GameObject:
    def __init__(self, x, y, image_file=None):
        self.rect = pygame.Rect(x * TILE_SIZE + 6, y * TILE_SIZE + 6, TILE_SIZE - 12, TILE_SIZE - 12)
        
        if image_file:
            try:
                self.image = pygame.image.load(image_file).convert_alpha()
                self.image = pygame.transform.scale(self.image, (TILE_SIZE, TILE_SIZE))
            except:
                self.image = None
        else:
            self.image = None
        self.fallback_color = (200, 200, 200)

    def draw(self, surface):
        if self.image:
            surface.blit(self.image, (self.rect.x - 6, self.rect.y - 6))
        else:
            pygame.draw.rect(surface, self.fallback_color, self.rect)

# Subklasės
class Wall(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "wall.png")
        self.fallback_color = (50, 50, 70)

class DashItem(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "dash.png")
        self.rect = pygame.Rect(x * TILE_SIZE + 10, y * TILE_SIZE + 10, 12, 12)
        self.fallback_color = (255, 255, 0)

class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "enemy.png")
        self.fallback_color = (255, 50, 50)
        self._speed = 1.3
        self.move_delay = 2
        self.move_counter = 0

    def chase_player(self, player_rect, walls):
        self.move_counter += 1
        if self.move_counter < self.move_delay: return
        self.move_counter = 0

        dx = self._speed if self.rect.x < player_rect.x else -self._speed if self.rect.x > player_rect.x else 0
        dy = self._speed if self.rect.y < player_rect.y else -self._speed if self.rect.y > player_rect.y else 0

        if dx != 0:
            target_x = self.rect.move(dx, 0)
            if not any(w.rect.colliderect(target_x) for w in walls):
                self.rect.x += dx
        if dy != 0:
            target_y = self.rect.move(0, dy)
            if not any(w.rect.colliderect(target_y) for w in walls):
                self.rect.y += dy

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, "player.png")
        self.fallback_color = (0, 255, 150)
        self.hp = 100
        self.is_dashing = False
        self.dash_timer = 0
        self.has_dash = True 

    def start_dash(self):
        if self.has_dash and not self.is_dashing:
            self.is_dashing = True
            self.dash_timer = 12
            self.has_dash = False 

    def update(self, dx, dy, walls):
        speed = 12 if self.is_dashing else 3
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0: self.is_dashing = False

        # Teleportacija
        if dx != 0:
            new_x = self.rect.x + dx * speed
            if new_x < 0: 
                new_x = SCREEN_WIDTH - self.rect.width - 2
            elif new_x > SCREEN_WIDTH - self.rect.width:
                new_x = 2
                
            test_rect = pygame.Rect(new_x, self.rect.y, self.rect.width, self.rect.height)
            if not any(w.rect.colliderect(test_rect) for w in walls):
                self.rect.x = new_x

        if dy != 0:
            new_y = self.rect.y + dy * speed
            if new_y < 0:
                new_y = SCREEN_HEIGHT - self.rect.height - 2
            elif new_y > SCREEN_HEIGHT - self.rect.height:
                new_y = 2
                
            test_rect = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)
            if not any(w.rect.colliderect(test_rect) for w in walls):
                self.rect.y = new_y

# Valdymas
class DungeonManager:
    def __init__(self):
        self.walls, self.enemies, self.items, self.empty_slots = [], [], [], []
        self.player = None

    def load_map(self, segment_files, extra_enemies=0):
        old_player = self.player
        chosen = [random.choice(segment_files) for _ in range(4)]
        segments = []
        for f in chosen:
            with open(f, 'r') as file: segments.append([line.strip() for line in file.readlines()])
        
        self.walls, self.enemies, self.items, self.empty_slots = [], [], [], []
        found_p = None
        for row in range(20):
            line = segments[0][row] + segments[1][row] if row < 10 else segments[2][row-10] + segments[3][row-10]
            for col, char in enumerate(line):
                if char == '1': self.walls.append(Wall(col, row))
                elif char == 'E': self.enemies.append(Enemy(col, row))
                elif char == 'P': found_p = (col, row)
                elif char == '0': self.empty_slots.append((col, row))

        if found_p:
            if old_player:
                self.player = old_player
                self.player.rect.x, self.player.rect.y = found_p[0]*TILE_SIZE+6, found_p[1]*TILE_SIZE+6
            else: self.player = Player(found_p[0], found_p[1])
        elif not self.player: self.player = Player(1, 1)

        # Ištriname bet kokias sienas po žaidėju
        self.walls = [w for w in self.walls if not w.rect.colliderect(self.player.rect)]

        random.shuffle(self.empty_slots)
        for _ in range(min(extra_enemies, len(self.empty_slots))):
            ex, ey = self.empty_slots.pop()
            e = Enemy(ex, ey)
            if not e.rect.colliderect(self.player.rect):
                self.enemies.append(e)

    def spawn_item(self):
        if self.empty_slots:
            x, y = random.choice(self.empty_slots)
            self.items.append(DashItem(x, y))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Dungeon Crawler 2026")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.manager = DungeonManager()
        self.segments = ["seg1.txt", "seg2.txt", "seg3.txt", "seg4.txt"]
        self.level, self.state, self.spawn_timer = 1, "PLAYING", 0
        self.manager.load_map(self.segments)

    def draw_ui(self):
        p = self.manager.player
        pygame.draw.rect(self.screen, COLORS["hp_bg"], (10, 10, 200, 15))
        if p.hp > 0: pygame.draw.rect(self.screen, COLORS["hp_bar"], (10, 10, 200*(p.hp/100), 15))
        dot_c = COLORS["dash_indicator"] if p.has_dash else (50, 50, 50)
        pygame.draw.circle(self.screen, dot_c, (230, 17), 8)
        txt = self.font.render(f"Lvl: {self.level} | Enemies: {len(self.manager.enemies)}", True, COLORS["text"])
        self.screen.blit(txt, (SCREEN_WIDTH-150, 10))

    def run(self):
        while True:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "PLAYING": self.manager.player.start_dash()
                    if event.key == pygame.K_r and self.state == "GAMEOVER":
                        self.__init__()

            if self.state == "PLAYING" and self.manager.player:
                self.spawn_timer += dt
                if self.spawn_timer > 5000:
                    self.manager.spawn_item()
                    self.spawn_timer = 0

                keys = pygame.key.get_pressed()
                dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
                dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
                self.manager.player.update(dx, dy, self.manager.walls)

                for item in self.manager.items[:]:
                    if self.manager.player.rect.colliderect(item.rect):
                        self.manager.player.has_dash = True
                        self.manager.items.remove(item)

                for enemy in self.manager.enemies[:]:
                    enemy.chase_player(self.manager.player.rect, self.manager.walls)
                    if self.manager.player.rect.colliderect(enemy.rect):
                        if self.manager.player.is_dashing:
                            self.manager.enemies.remove(enemy)
                            if not self.manager.enemies:
                                self.level += 1
                                self.manager.player.hp = min(100, self.manager.player.hp + 25)
                                self.manager.load_map(self.segments, (self.level-1)*2)
                        else:
                            self.manager.player.hp -= 0.8
                            if self.manager.player.hp <= 0: self.state = "GAMEOVER"

            self.screen.fill(COLORS["bg"])
            for obj in self.manager.walls + self.manager.items + self.manager.enemies:
                obj.draw(self.screen)
            if self.manager.player: self.manager.player.draw(self.screen)
            self.draw_ui()
            if self.state == "GAMEOVER":
                msg = self.font.render("GAME OVER! Press R to Restart", True, COLORS["text"])
                self.screen.blit(msg, (SCREEN_WIDTH//2-140, SCREEN_HEIGHT//2))
            pygame.display.flip()

if __name__ == "__main__":
    Game().run()
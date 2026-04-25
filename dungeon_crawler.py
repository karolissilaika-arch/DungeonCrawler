import pygame
import random
import sys

# --- KONSTANTOS ---
TILE_SIZE = 32
GRID_WIDTH, GRID_HEIGHT = 20, 20
SCREEN_WIDTH = GRID_WIDTH * TILE_SIZE
SCREEN_HEIGHT = GRID_HEIGHT * TILE_SIZE

COLORS = {
    "wall": (50, 50, 70),
    "player": (0, 255, 150),
    "dash": (255, 255, 0),
    "enemy": (255, 50, 50),
    "bg": (15, 15, 25),
    "hp_bar": (0, 255, 0),
    "hp_bg": (100, 0, 0),
    "text": (255, 255, 255)
}

# ---  BAZINĖS KLASĖS ---
class GameObject:
    def __init__(self, x, y, color):
        # Kolizijos stačiakampis
        self.rect = pygame.Rect(x * TILE_SIZE + 6, y * TILE_SIZE + 6, TILE_SIZE - 12, TILE_SIZE - 12)
        self.color = color

    def draw(self, surface):
        pygame.draw.rect(surface, self.color, self.rect)

class Wall(GameObject):
    def __init__(self, x, y): super().__init__(x, y, COLORS["wall"])

class DashItem(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, COLORS["dash"])
        self.rect = pygame.Rect(x * TILE_SIZE + 10, y * TILE_SIZE + 10, 12, 12)

# ---  PRIEŠŲ AI ---
class Enemy(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, COLORS["enemy"])
        self._speed = 1.3
        self.move_delay = 2
        self.move_counter = 0

    def chase_player(self, player_rect, walls):
        self.move_counter += 1
        if self.move_counter < self.move_delay: return
        self.move_counter = 0

        # Nustatome kryptį
        dx = 0
        if self.rect.x < player_rect.x: dx = self._speed
        elif self.rect.x > player_rect.x: dx = -self._speed

        dy = 0
        if self.rect.y < player_rect.y: dy = self._speed
        elif self.rect.y > player_rect.y: dy = -self._speed

        # --- SKAIDYTAS JUDĖJIMAS ---
        # Bandom judėti X ašimi
        if dx != 0:
            target_x = self.rect.move(dx, 0)
            if not any(w.rect.colliderect(target_x) for w in walls):
                self.rect.x += dx

        # Bandom judėti Y ašimi
        if dy != 0:
            target_y = self.rect.move(0, dy)
            if not any(w.rect.colliderect(target_y) for w in walls):
                self.rect.y += dy

class Player(GameObject):
    def __init__(self, x, y):
        super().__init__(x, y, COLORS["player"])
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
        speed = 12 if self.is_dashing else 4
        if self.is_dashing:
            self.dash_timer -= 1
            if self.dash_timer <= 0: self.is_dashing = False

        # Judėjimas išskaidytas ašimis, kad veiktų įstrižas judėjimas
        if dx != 0:
            new_x = (self.rect.x + dx * speed) % SCREEN_WIDTH
            test_rect = pygame.Rect(new_x, self.rect.y, self.rect.width, self.rect.height)
            if not any(w.rect.colliderect(test_rect) for w in walls):
                self.rect.x = new_x

        if dy != 0:
            new_y = (self.rect.y + dy * speed) % SCREEN_HEIGHT
            test_rect = pygame.Rect(self.rect.x, new_y, self.rect.width, self.rect.height)
            if not any(w.rect.colliderect(test_rect) for w in walls):
                self.rect.y = new_y

# --- PASAULIO VALDYMAS ---
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
        elif not self.player: # Saugiklis prieš AttributeError
            self.player = Player(1, 1)

        random.shuffle(self.empty_slots)
        for _ in range(min(extra_enemies, len(self.empty_slots))):
            ex, ey = self.empty_slots.pop()
            self.enemies.append(Enemy(ex, ey))

    def spawn_item(self):
        if self.empty_slots:
            x, y = random.choice(self.empty_slots)
            self.items.append(DashItem(x, y))

# --- PAGRINDINĖ ŽAIDIMO KLASĖ ---
class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("OOP Dungeon Crawler 2026")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.SysFont("Arial", 20)
        self.manager = DungeonManager()
        self.segments = ["seg1.txt", "seg2.txt", "seg3.txt", "seg4.txt"]
        self.level, self.state, self.spawn_timer = 1, "PLAYING", 0
        self.manager.load_map(self.segments)

    def draw_ui(self):
        p = self.manager.player
        # HP Juosta
        pygame.draw.rect(self.screen, COLORS["hp_bg"], (10, 10, 200, 15))
        if p.hp > 0: pygame.draw.rect(self.screen, COLORS["hp_bar"], (10, 10, 200*(p.hp/100), 15))
        # Dash indikatorius
        dot_c = COLORS["dash"] if p.has_dash else (50, 50, 50)
        pygame.draw.circle(self.screen, dot_c, (230, 17), 8)
        # Level informacija
        txt = self.font.render(f"Level: {self.level}  Enemies: {len(self.manager.enemies)}", True, COLORS["text"])
        self.screen.blit(txt, (SCREEN_WIDTH-200, 10))

    def run(self):
        while True:
            dt = self.clock.tick(60)
            for event in pygame.event.get():
                if event.type == pygame.QUIT: pygame.quit(); sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE and self.state == "PLAYING":
                        self.manager.player.start_dash()
                    if event.key == pygame.K_r and self.state == "GAMEOVER":
                        self.level, self.manager.player, self.state = 1, None, "PLAYING"
                        self.manager.load_map(self.segments)

            if self.state == "PLAYING" and self.manager.player:
                # Item spawn sistema
                self.spawn_timer += dt
                if self.spawn_timer > 5000:
                    self.manager.spawn_item()
                    self.spawn_timer = 0

                # Įvestis 
                keys = pygame.key.get_pressed()
                dx = (keys[pygame.K_RIGHT] - keys[pygame.K_LEFT])
                dy = (keys[pygame.K_DOWN] - keys[pygame.K_UP])
                self.manager.player.update(dx, dy, self.manager.walls)

                # Surinkimas
                for item in self.manager.items[:]:
                    if self.manager.player.rect.colliderect(item.rect):
                        self.manager.player.has_dash = True
                        self.manager.items.remove(item)

                # Priešų AI
                for enemy in self.manager.enemies[:]:
                    enemy.chase_player(self.manager.player.rect, self.manager.walls)
                    if self.manager.player.rect.colliderect(enemy.rect):
                        if self.manager.player.is_dashing:
                            self.manager.enemies.remove(enemy)
                            if not self.manager.enemies: # Pereinam į kitą lygį
                                self.level += 1
                                self.manager.player.hp = min(100, self.manager.player.hp + 25)
                                self.manager.load_map(self.segments, (self.level-1)*3)
                        else:
                            self.manager.player.hp -= 0.8
                            if self.manager.player.hp <= 0: self.state = "GAMEOVER"

            # Renderinimas
            self.screen.fill(COLORS["bg"])
            for w in self.manager.walls: w.draw(self.screen)
            for i in self.manager.items: i.draw(self.screen)
            for e in self.manager.enemies: e.draw(self.screen)
            if self.manager.player: self.manager.player.draw(self.screen)
            self.draw_ui()
            
            if self.state == "GAMEOVER":
                msg = self.font.render("GAME OVER! Press R to Restart", True, COLORS["text"])
                self.screen.blit(msg, (SCREEN_WIDTH//2-140, SCREEN_HEIGHT//2))
            
            pygame.display.flip()

if __name__ == "__main__":
    Game().run()
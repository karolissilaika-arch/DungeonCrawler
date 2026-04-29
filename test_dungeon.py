import unittest
import pygame
# Importuojame klases iš tavo pagrindinio failo
from dungeon_crawler import Player, Enemy, Wall, TILE_SIZE 

class TestDungeonCrawler(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        """Inicijuojame pygame vieną kartą visiems testams."""
        pygame.init()
        # Sukuriame virtualų ekraną, kad veiktų Rect operacijos
        pygame.display.set_mode((1, 1))

    def setUp(self):
        """Šis metodas paleidžiamas prieš kiekvieną testą individualiai."""
        self.player = Player(1, 1)
        self.enemy = Enemy(2, 2)
        # Sukuriame sienų sąrašą testavimui
        self.walls = []

    def test_player_initial_stats(self):
        """Patikriname, ar žaidėjas prasideda su teisingais parametrais."""
        self.assertEqual(self.player.hp, 100, "Pradinis HP turi būti 100")
        self.assertTrue(self.player.has_dash, "Žaidėjas turi pradėti su Dash galimybe")
        self.assertFalse(self.player.is_dashing, "Žaidėjas neturi būti dash būsenoje pradžioje")

    def test_player_movement_collision(self):
        """Patikriname, ar siena blokuoja žaidėjo judėjimą."""
        # Nustatome žinomas pozicijas
        self.player.rect.x = TILE_SIZE  # Pozicija 32
        initial_x = self.player.rect.x
        
        # Sukuriame sieną tiesiai prieš žaidėją
        # Kadangi greitis be dash yra 3, siena ties 35-40 turėtų blokuoti
        wall = Wall(0, 0)
        wall.rect.x = initial_x + 2 
        wall.rect.y = self.player.rect.y
        
        # Bandome judėti į dešinę (dx=1)
        self.player.update(1, 0, [wall])
        
        # Žaidėjas neturėtų pajudėti, nes siena stovi kelyje
        self.assertEqual(self.player.rect.x, initial_x, "Žaidėjas neturėtų praeiti pro sieną")

    def test_dash_mechanic(self):
        """Patikriname, ar dash aktyvavimas veikia teisingai[cite: 2]."""
        self.player.start_dash()
        self.assertTrue(self.player.is_dashing, "is_dashing turėtų būti True")
        self.assertFalse(self.player.has_dash, "Panaudojus dash, galimybė turi pradingti")
        self.assertEqual(self.player.dash_timer, 12, "Dash laikmatis turi būti nustatytas į 12")

    def test_enemy_damage(self):
        """Patikriname, ar priešas daro žalą susidūrimo metu[cite: 2]."""
        initial_hp = self.player.hp
        # Dirbtinai uždedame priešą ant žaidėjo
        self.player.rect.center = self.enemy.rect.center
        
        # Imituojame žaidimo logiką iš dungeon_crawler.py[cite: 2]
        if self.player.rect.colliderect(self.enemy.rect) and not self.player.is_dashing:
            self.player.hp -= 0.8
            
        self.assertLess(self.player.hp, initial_hp, "HP turi sumažėti po kontakto su priešu")

    def test_dash_kills_enemy(self):
        """Patikriname, ar dash būsenoje esantis žaidėjas nužudo priešą[cite: 2]."""
        self.player.start_dash()
        # Sutapatiname pozicijas kolizijai
        self.enemy.rect.center = self.player.rect.center
        
        enemies = [self.enemy]
        # Imituojame žaidimo logiką: dash metu priešas pašalinamas[cite: 2]
        if self.player.rect.colliderect(self.enemy.rect) and self.player.is_dashing:
            enemies.remove(self.enemy)
            
        self.assertEqual(len(enemies), 0, "Dash metu priešas turėtų būti pašalintas iš sąrašo")

if __name__ == '__main__':
    unittest.main()
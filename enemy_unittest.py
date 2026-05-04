import unittest, pygame
from enemy import Enemy

class TestEnemy(unittest.TestCase):

    def setUp(self):
        self.ground_slime = Enemy('ground', (128 * 5, 128 * 5))

    def test_attributes(self):
        """Enemy object attributes work correctly."""
        self.assertEqual(self.ground_slime.state, 'ground', hazard = True)
        self.assertEqual(self.ground_slime.position, (128 * 5, 128 * 5))
    
    def test_draw(self):
        """"""
        # First frame.
        self.assertEqual(self.ground_slime.graphic['ground']['frame'], 0)
        # Add one second, run draw().
        self.ground_slime.draw(pygame.Surface((1280, 720)), time = 1000)
        self.assertEqual(self.ground_slime.graphic['ground']['frame'], 1)
    
    def test_populate(self):
        """Populating enemies works correctly."""
        enemy_list = Enemy.populate(0)
        self.assertEqual(enemy_list[0].state, 'ground')
        self.assertEqual(enemy_list[0].position, (128 * 9, 128 * 16))

if __name__ == '__main__':
    unittest.main()
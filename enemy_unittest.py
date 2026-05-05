import unittest, pygame
from enemy import *

"""
TODO :: Rewrite unittest to match new project structure.
        Verify animation and population correctly.
"""

class TestEnemy(unittest.TestCase):

    def setUp(self):
        self.ground_slime = EnemyGround((128 * 5, 128 * 5))

    def test_attributes(self):
        """Enemy object attributes work correctly."""
        self.assertEqual(self.ground_slime.state, 'alive')
        self.assertEqual(self.ground_slime.hazard, True)
        self.assertEqual(self.ground_slime.hitbox, (128 * 5, 128 * 5))
    
    def test_draw(self):
        """"""
        # First frame.
        self.assertEqual(self.ground_slime.graphic['alive']['frame'], 0)
        # Add one second, run draw().
        self.ground_slime.draw(pygame.Surface((1280, 720)), time = 1000)
        self.assertEqual(self.ground_slime.graphic['ground']['frame'], 1)
    
    def test_populate(self):
        """If level one populating enemies works correctly."""
        enemy_list = Enemy.populate(0)
        self.assertEqual(enemy_list[0].state, 'ground')
        self.assertEqual(enemy_list[0].position, (128 * 9, 128 * 16))

if __name__ == '__main__':
    unittest.main()
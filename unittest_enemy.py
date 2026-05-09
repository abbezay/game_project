import unittest
from enemy import *
import player

pygame.mixer.init() # Player class holds pygame Sound attributes.


class TestEnemy(unittest.TestCase):
    """Test Enemy class."""

    def setUp(self):
        self.ground_slime = EnemyGround((128, 128))
        self.player = player.Player()

    def test_spawn(self):
        """Enemy object attributes are set correctly."""
        # Enemy spawns alive.
        self.assertEqual(self.ground_slime.state, 'alive')
        # Enemy anchor correct position set.
        self.assertEqual(self.ground_slime.anchor[0], 128)
        self.assertEqual(self.ground_slime.anchor[1], 128)
        # Hitbox and weakpoint are both Rect objects.
        self.assertEqual(type(self.ground_slime.hitbox),
                         type(self.ground_slime.weakpoint))


if __name__ == '__main__':
    unittest.main()
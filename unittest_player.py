import unittest, pygame
from player import Player
pygame.mixer.init() # The player holds sounds.

class TestPlayer(unittest.TestCase):
    """Test Player class."""

    def setUp(self):
        self.player = Player()

    def test_spawn(self):
        """Test that the player spawns with the correct attributes."""
        self.assertEqual(self.player.health, 4)
        self.assertEqual(self.player.speed, 4)
        self.assertEqual(self.player.state, 'idle')
        self.assertEqual(self.player.landed, False)
        self.assertEqual(self.player.key_aquired, False)

    def test_jump(self):
        """Test that jumps sets state to falling after cooldowns.
        Time isn't given, so jump is set as finished."""
        self.player.jump([])
        self.assertEqual(self.player.state, 'falling')
        self.assertEqual(self.player.landed, False)

if __name__ == '__main__':
    unittest.main()
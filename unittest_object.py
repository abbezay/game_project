import unittest
from object import *
import player

pygame.mixer.init() # Player class holds pygame Sound attributes. 


class TestObject(unittest.TestCase):
    """Test Object class."""

    def setUp(self):
        self.door = Door((128, 128))
        self.key = Key((128, 128))
        self.player = player.Player()

    def test_spawn(self):
        """Test that attributes are correctly spawned."""
        self.assertEqual(self.door.position, (128, 128))
        self.assertEqual(self.key.hitbox.width, 128)
        # Test if door is doubled in size.
        self.assertEqual(self.door.hitbox.width, 256)
        self.assertEqual(self.door.hitbox.height, 256)
        self.assertEqual(self.door.sprite_size,
                         self.key.sprite_size)
        self.assertEqual(self.key.visible, True)
    
    def test_collide(self):
        """Test if collision works."""
        # Set hitboxes overlapping.
        self.player.hitbox = pygame.Rect(128, 128, 128, 128)
        self.key.hitbox = pygame.Rect(0, 0, 128, 128)
        # Test collide.
        self.key.collide(self.player)
        self.assertEqual(self.key.visible, False)
        self.assertEqual(self.player.key_aquired, True)

        # Reset player flag.
        self.player.key_aquired = False

        # Test if collision is possible if key isn't visible.
        self.assertEqual(self.key.visible, False)
        self.key.collide(self.player)
        self.assertEqual(self.player.key_aquired, False)


if __name__ == '__main__':
    unittest.main()
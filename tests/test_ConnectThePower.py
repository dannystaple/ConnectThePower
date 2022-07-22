from unittest import TestCase, mock
from connect_the_power import MainGameUI
from pygame.math import Vector2


class TestGameUI(TestCase):
    """Test Game UI features"""

    def test_testGridCoordsShouldMapToScreenCoords(self):
        """
        Given a set of grid coordinates, it should be able to map them
        to sensible screen coordinates.
        """
        grid_coord = Vector2(0, 0)
        expected_coords = Vector2(MainGameUI.grid_left, MainGameUI.grid_top)
        fakeDisplay = mock.Mock()
        ui = MainGameUI(fakeDisplay)
        self.assertEqual(expected_coords, ui.from_core_grid(grid_coord))

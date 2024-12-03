import unittest
from unittest.mock import patch, MagicMock
import pygame
from src.zenithview.display import Display


class TestDisplay(unittest.TestCase):
    @patch('pygame.display.set_mode')
    @patch('pygame.font.Font')
    def test_initialization(self, MockFont, MockSetMode):
        # Mock the pygame functionalities
        MockSetMode.return_value = MagicMock()
        MockFont.return_value = MagicMock()

        # Create an instance of Display
        display = Display(width=800, height=600, caption="Test Display")

        # Test that the display is initialized correctly
        self.assertEqual(display.width, 800)
        self.assertEqual(display.height, 600)
        self.assertEqual(display.screen, MockSetMode.return_value)
        self.assertEqual(display.font, MockFont.return_value)
        self.assertEqual(display.clock, None)  # Since clock initialization can fail
        self.assertIsNotNone(display.audioObject)
        self.assertIsNotNone(display.output)

    @patch('pygame.display.set_mode')
    def test_invalid_width_and_height(self, MockSetMode):
        # Test initialization with invalid width and height
        MockSetMode.return_value = MagicMock()

        # Create an instance of Display with invalid size
        display = Display(width=5, height=5)

        # Check that width and height are adjusted to the minimum size
        self.assertEqual(display.width, 10)
        self.assertEqual(display.height, 10)

    @patch('pygame.display.set_mode')
    @patch('pygame.time.Clock')
    def test_update(self, MockClock, MockSetMode):
        MockSetMode.return_value = MagicMock()
        MockClock.return_value = MagicMock()

        # Create an instance of Display
        display = Display(width=800, height=600)

        # Test update method with a simple array
        test_array = [10, 20, 30, 40, 50]
        display.update(test_array)

        # Ensure update-related operations are called
        self.assertEqual(display.it, display.updateFactor)
        self.assertTrue(display.cache)
        MockClock.return_value.tick.assert_called_once()

    @patch('pygame.display.set_mode')
    def test_update_array_length_warning(self, MockSetMode):
        MockSetMode.return_value = MagicMock()

        # Create an instance of Display with a small width to trigger the warning
        display = Display(width=50, height=50)
        test_array = [10, 20, 30, 40, 50, 60, 70]

        # Mock logging to capture warnings
        with self.assertLogs('root', level='WARNING') as log:
            display.update(test_array)

        # Check for the warning in the logs
        self.assertIn('Array lenght is greater than display width', log.output[0])

    @patch('pygame.display.set_mode')
    @patch('pygame.time.Clock')
    def test_pause(self, MockClock, MockSetMode):
        MockSetMode.return_value = MagicMock()
        MockClock.return_value = MagicMock()

        # Create an instance of Display
        display = Display(width=800, height=600)

        # Test pause functionality
        with patch('pygame.event.get', return_value=[pygame.event.Event(pygame.KEYDOWN, key=pygame.K_SPACE)]):
            display.pause()

        # Ensure the pause method was called and unpaused
        self.assertTrue(MockClock.return_value.tick.called)

    @patch('pygame.display.set_mode')
    @patch('pyaudio.PyAudio')
    def test_sinewave(self, MockPyAudio, MockSetMode):
        MockSetMode.return_value = MagicMock()
        MockPyAudio.return_value = MagicMock()

        # Create an instance of Display
        display = Display(width=800, height=600)

        # Test sinewave generation
        sine_wave = display.sinewave(duration=0.1, frequency=440)

        # Assert the sinewave output is not empty and has correct data type
        self.assertTrue(sine_wave)
        self.assertIsInstance(sine_wave, bytes)

    @patch('pygame.display.set_mode')
    @patch('pyaudio.PyAudio')
    def test_preprocess(self, MockPyAudio, MockSetMode):
        MockSetMode.return_value = MagicMock()
        MockPyAudio.return_value = MagicMock()

        # Create an instance of Display
        display = Display(width=800, height=600)

        # Test preprocess with a sample array
        array = [100, 200, 300]
        processed_data = display.preprocess(array)

        # Assert that the preprocessing returns the expected dictionary
        self.assertEqual(len(processed_data), 3)
        self.assertTrue(all(isinstance(value, bytes) for value in processed_data.values()))

    @patch('pygame.display.set_mode')
    def test_thickness(self, MockSetMode):
        MockSetMode.return_value = MagicMock()

        # Create an instance of Display
        display = Display(width=800, height=600)

        # Test thickness calculation
        thickness = display.thickness(arrayLen=4)

        # Assert the thickness is calculated correctly
        self.assertEqual(thickness, 200)

    @patch('pygame.display.set_mode')
    @patch('pygame.time.Clock')
    def test_release(self, MockClock, MockSetMode):
        MockSetMode.return_value = MagicMock()
        MockClock.return_value = MagicMock()

        # Create an instance of Display
        display = Display(width=800, height=600)

        # Test release method
        display.release(lastArray=[10, 20, 30])

        # Ensure resources are released
        self.assertTrue(display.null)
        self.assertIsNotNone(display.finishTime)


if __name__ == "__main__":
    unittest.main()

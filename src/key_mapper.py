"""
Keyboard simulation module using pynput.
Provides safe key press/release operations with error handling.
"""

from pynput.keyboard import Controller
import config

class KeyMapper:
    """Maps gestures to keyboard inputs."""
    
    def __init__(self):
        """Initialize the keyboard controller."""
        self.keyboard = Controller()
        self.pressed_keys = set()
    
    def press_key(self, key: str) -> None:
        """
        Press a key if not already pressed.
        
        Args:
            key: The key to press (e.g., 'w', 'a', 's', 'd')
        """
        try:
            if key not in self.pressed_keys:
                self.keyboard.press(key)
                self.pressed_keys.add(key)
        except Exception as e:
            print(f"Error pressing key '{key}': {e}")
    
    def release_key(self, key: str) -> None:
        """
        Release a key if currently pressed.
        
        Args:
            key: The key to release (e.g., 'w', 'a', 's', 'd')
        """
        try:
            if key in self.pressed_keys:
                self.keyboard.release(key)
                self.pressed_keys.discard(key)
        except Exception as e:
            print(f"Error releasing key '{key}': {e}")
    
    def release_all(self) -> None:
        """Release all currently pressed keys."""
        for key in list(self.pressed_keys):
            self.release_key(key)
    
    def steer_left(self) -> None:
        """Press left, release right and backward."""
        self.release_key(config.KEY_RIGHT)
        self.release_key(config.KEY_BACKWARD)
        self.press_key(config.KEY_LEFT)
    
    def steer_right(self) -> None:
        """Press right, release left and backward."""
        self.release_key(config.KEY_LEFT)
        self.release_key(config.KEY_BACKWARD)
        self.press_key(config.KEY_RIGHT)
    
    def go_straight(self) -> None:
        """Press forward, release left, right, and backward."""
        self.release_key(config.KEY_LEFT)
        self.release_key(config.KEY_RIGHT)
        self.release_key(config.KEY_BACKWARD)
        self.press_key(config.KEY_FORWARD)
    
    def go_backward(self) -> None:
        """Press backward, release left, right, and forward."""
        self.release_key(config.KEY_LEFT)
        self.release_key(config.KEY_RIGHT)
        self.release_key(config.KEY_FORWARD)
        self.press_key(config.KEY_BACKWARD)
    
    def accelerate(self) -> None:
        """Press forward, release backward."""
        self.release_key(config.KEY_BACKWARD)
        self.press_key(config.KEY_FORWARD)
    
    def brake(self) -> None:
        """Press backward, release forward."""
        self.release_key(config.KEY_FORWARD)
        self.press_key(config.KEY_BACKWARD)

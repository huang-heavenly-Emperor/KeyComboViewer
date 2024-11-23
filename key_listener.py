from pynput import keyboard
from collections import deque
import threading

class KeyListener:
    def __init__(self, callback):
        self.current_keys = set()
        self.callback = callback
        self.listener = None
        self.lock = threading.Lock()
        
    def start(self):
        self.listener = keyboard.Listener(
            on_press=self._on_press,
            on_release=self._on_release
        )
        self.listener.start()
        
    def stop(self):
        if self.listener:
            self.listener.stop()
            
    def _on_press(self, key):
        with self.lock:
            try:
                if hasattr(key, 'char'):
                    key_str = key.char
                else:
                    key_str = key.name
                self.current_keys.add(key_str)
                self._update_display()
            except AttributeError:
                pass
                
    def _on_release(self, key):
        with self.lock:
            try:
                if hasattr(key, 'char'):
                    key_str = key.char
                else:
                    key_str = key.name
                self.current_keys.discard(key_str)
            except AttributeError:
                pass
                
    def _update_display(self):
        key_combination = ' + '.join(sorted(self.current_keys))
        if key_combination:
            self.callback(key_combination) 
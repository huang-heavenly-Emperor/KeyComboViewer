import json
from functools import wraps
import time
import threading

def load_config():
    try:
        with open('config.json', 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return {}

def debounce(wait):
    def decorator(fn):
        last_time = [0]
        timer = [None]
        
        @wraps(fn)
        def debounced(*args, **kwargs):
            def call_function():
                fn(*args, **kwargs)
                
            current_time = time.time()
            if current_time - last_time[0] > wait:
                if timer[0]:
                    timer[0].cancel()
                timer[0] = None
                call_function()
            else:
                if timer[0]:
                    timer[0].cancel()
                timer[0] = threading.Timer(wait, call_function)
                timer[0].start()
            
            last_time[0] = current_time
            
        return debounced
    return decorator 
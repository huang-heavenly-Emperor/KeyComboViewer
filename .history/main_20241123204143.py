from key_listener import KeyListener
from ui_manager import KeyDisplayWindow
from utils import load_config, debounce
import threading

def main():
    config = load_config()
    
    # 创建UI窗口
    window = KeyDisplayWindow(config)
    
    # 创建防抖显示函数
    @debounce(config['debounce_time'])
    def display_keys(key_combination):
        window.display_message(key_combination)
    
    # 创建并启动键盘监听器
    listener = KeyListener(display_keys)
    listener.start()
    
    # 启动UI
    window.start()

if __name__ == "__main__":
    main() 
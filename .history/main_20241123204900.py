import tkinter as tk
from tkinter import ttk
from pynput import keyboard
from datetime import datetime, timedelta
import threading

class KeyboardListener:
    def __init__(self, root):
        self.root = root
        self.root.title("键盘监听器")
        self.root.geometry("400x150")  # 设置初始窗口大小
        
        # 设置窗口样式
        self.root.configure(bg='#2c2c2c')
        self.style = ttk.Style()
        self.style.configure('Custom.TFrame', background='#2c2c2c')
        self.style.configure('Custom.TLabel', 
                           background='#2c2c2c', 
                           foreground='#ffffff',
                           font=('Arial', 12))
        
        # 创建主框架
        self.main_frame = ttk.Frame(root, style='Custom.TFrame')
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 创建显示标签
        self.key_label = ttk.Label(
            self.main_frame, 
            text="等待按键...", 
            style='Custom.TLabel'
        )
        self.key_label.pack(pady=20)
        
        # 存储按键状态
        self.current_keys = set()
        self.last_press_time = datetime.now()
        self.COMBINATION_TIMEOUT = 0.5  # 组合键超时时间（秒）
        
        # 启动键盘监听
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        
        # 定期更新显示
        self.update_display()
        
    def on_press(self, key):
        try:
            # 获取按键名称
            key_name = key.char
        except AttributeError:
            key_name = str(key).replace('Key.', '')
            
        # 更新时间戳
        current_time = datetime.now()
        if (current_time - self.last_press_time).total_seconds() > self.COMBINATION_TIMEOUT:
            self.current_keys.clear()
        self.last_press_time = current_time
        
        # 添加按键到集合
        self.current_keys.add(key_name)
        
    def on_release(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key).replace('Key.', '')
        
        # 从集合中移除按键
        self.current_keys.discard(key_name)
        
    def update_display(self):
        # 检查组合键是否超时
        current_time = datetime.now()
        if (current_time - self.last_press_time).total_seconds() > self.COMBINATION_TIMEOUT:
            self.current_keys.clear()
        
        # 更新显示
        if self.current_keys:
            keys_text = " + ".join(sorted(self.current_keys))
            self.key_label.configure(text=f"当前按键: {keys_text}")
        else:
            self.key_label.configure(text="等待按键...")
        
        # 定期更新
        self.root.after(100, self.update_display)
        
    def cleanup(self):
        self.listener.stop()

def main():
    root = tk.Tk()
    root.resizable(True, True)  # 允许调整窗口大小
    
    # 设置最小窗口大小
    root.minsize(300, 100)
    
    app = KeyboardListener(root)
    
    # 关闭窗口时清理资源
    root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
    root.mainloop()

if __name__ == '__main__':
    main() 
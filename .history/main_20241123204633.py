from key_listener import KeyListener
from ui_manager import KeyDisplayWindow
from utils import load_config, debounce
import threading
import tkinter as tk
from tkinter import ttk

class DraggableResizableWindow:
    def __init__(self, root):
        self.root = root
        # 移除默认的标题栏
        self.root.overrideredirect(True)
        # 设置窗口初始大小
        self.root.geometry('400x300')
        
        # 创建自定义标题栏
        self.title_bar = ttk.Frame(self.root)
        self.title_bar.pack(fill='x')
        
        # 标题文本
        self.title_label = ttk.Label(self.title_bar, text='My Window')
        self.title_label.pack(side='left', pady=5, padx=5)
        
        # 关闭按钮
        self.close_button = ttk.Button(self.title_bar, text='X', command=self.root.quit)
        self.close_button.pack(side='right', pady=5, padx=5)
        
        # 主内容区域
        self.content = ttk.Frame(self.root, relief='raised')
        self.content.pack(fill='both', expand=True)
        
        # 调整大小的角落
        self.resize_corner = ttk.Label(self.content, text='⟂')
        self.resize_corner.pack(side='right', anchor='se')
        
        # 绑定事件
        self.title_bar.bind('<Button-1>', self.start_drag)
        self.title_bar.bind('<B1-Motion>', self.drag)
        self.resize_corner.bind('<Button-1>', self.start_resize)
        self.resize_corner.bind('<B1-Motion>', self.resize)
        
        # 保存初始位置
        self.x = 0
        self.y = 0
        
    def start_drag(self, event):
        self.x = event.x
        self.y = event.y
        
    def drag(self, event):
        deltax = event.x - self.x
        deltay = event.y - self.y
        x = self.root.winfo_x() + deltax
        y = self.root.winfo_y() + deltay
        self.root.geometry(f'+{x}+{y}')
        
    def start_resize(self, event):
        self.x = event.x
        self.y = event.y
        
    def resize(self, event):
        width = self.root.winfo_width() + (event.x - self.x)
        height = self.root.winfo_height() + (event.y - self.y)
        # 设置最小窗口大小
        width = max(width, 200)
        height = max(height, 150)
        self.root.geometry(f'{width}x{height}')

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
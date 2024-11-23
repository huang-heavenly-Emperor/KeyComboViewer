import tkinter as tk
from tkinter import ttk
import threading

class KeyDisplayWindow:
    def __init__(self, config):
        self.config = config
        self.root = tk.Tk()
        self.setup_window()
        self.messages = []
        self.message_locks = []
        
    def setup_window(self):
        self.root.overrideredirect(True)
        self.root.attributes('-topmost', True)
        self.root.attributes('-alpha', self.config['ui']['opacity'])
        
        # 设置窗口位置（左下角）
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        window_width = self.config['ui']['window_width']
        offset = self.config['ui']['position_offset']
        
        self.root.geometry(f"{window_width}x50+{offset}+{screen_height-100-offset}")
        
        self.frame = ttk.Frame(self.root)
        self.frame.pack(fill=tk.BOTH, expand=True)
        
        style = ttk.Style()
        style.configure('Custom.TLabel',
                       background=self.config['ui']['background_color'],
                       foreground=self.config['ui']['text_color'],
                       font=(self.config['ui']['font'], 
                             self.config['ui']['font_size']))
                             
    def display_message(self, message):
        if len(self.messages) >= self.config['max_lines']:
            oldest = self.messages.pop(0)
            oldest.destroy()
            
        label = ttk.Label(self.frame, text=message, style='Custom.TLabel')
        label.pack(pady=2)
        self.messages.append(label)
        
        # 设置自动消失
        threading.Timer(
            self.config['display_duration'],
            lambda: self.remove_message(label)
        ).start()
        
    def remove_message(self, label):
        if label in self.messages:
            self.messages.remove(label)
            label.destroy()
            
    def start(self):
        self.root.mainloop() 
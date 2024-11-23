import tkinter as tk
from tkinter import ttk, colorchooser
from pynput import keyboard
from datetime import datetime, timedelta
import json
import os

class Settings:
    def __init__(self):
        # 默认设置
        self.default_settings = {
            "max_lines": 3,
            "display_time": 5,
            "font_size": 12,
            "bg_color": "#2c2c2c",
            "text_color": "#ffffff"
        }
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                with open('settings.json', 'r') as f:
                    return json.load(f)
        except:
            pass
        return self.default_settings.copy()

    def save_settings(self):
        with open('settings.json', 'w') as f:
            json.dump(self.settings, f)

class SettingsWindow:
    def __init__(self, parent, settings, apply_callback):
        self.window = tk.Toplevel(parent)
        self.window.title("设置")
        self.window.geometry("300x400")
        self.settings = settings
        self.apply_callback = apply_callback
        
        # 创建设置控件
        self.create_widgets()
        
        # 使设置窗口模态
        self.window.transient(parent)
        self.window.grab_set()

    def create_widgets(self):
        # 显示行数设置
        ttk.Label(self.window, text="显示行数:").pack(pady=5)
        self.lines_var = tk.StringVar(value=str(self.settings.settings["max_lines"]))
        ttk.Entry(self.window, textvariable=self.lines_var).pack()

        # 显示时间设置
        ttk.Label(self.window, text="显示时间(秒):").pack(pady=5)
        self.time_var = tk.StringVar(value=str(self.settings.settings["display_time"]))
        ttk.Entry(self.window, textvariable=self.time_var).pack()

        # 字体大小设置
        ttk.Label(self.window, text="字体大小:").pack(pady=5)
        self.font_var = tk.StringVar(value=str(self.settings.settings["font_size"]))
        ttk.Entry(self.window, textvariable=self.font_var).pack()

        # 颜色选择按钮
        ttk.Button(self.window, text="选择背景颜色", 
                  command=self.choose_bg_color).pack(pady=5)
        ttk.Button(self.window, text="选择文字颜色", 
                  command=self.choose_text_color).pack(pady=5)

        # 保存按钮
        ttk.Button(self.window, text="保存设置", 
                  command=self.save_settings).pack(pady=20)

    def choose_bg_color(self):
        color = colorchooser.askcolor(self.settings.settings["bg_color"])[1]
        if color:
            self.settings.settings["bg_color"] = color

    def choose_text_color(self):
        color = colorchooser.askcolor(self.settings.settings["text_color"])[1]
        if color:
            self.settings.settings["text_color"] = color

    def save_settings(self):
        try:
            self.settings.settings["max_lines"] = int(self.lines_var.get())
            self.settings.settings["display_time"] = float(self.time_var.get())
            self.settings.settings["font_size"] = int(self.font_var.get())
            self.settings.save_settings()
            self.apply_callback()
            self.window.destroy()
        except ValueError:
            tk.messagebox.showerror("错误", "请输入有效的数值")

class KeyboardListener:
    def __init__(self, root):
        self.root = root
        self.settings = Settings()
        self.setup_ui()
        self.setup_keyboard_listener()
        
        # 键盘历史记录
        self.key_history = []
        self.current_keys = set()
        self.last_press_time = datetime.now()

    def setup_ui(self):
        # 设置窗口置顶
        self.root.wm_attributes('-topmost', True)
        
        # 主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill='both', expand=True, padx=10, pady=10)
        
        # 设置按钮
        self.settings_button = ttk.Button(
            self.main_frame, 
            text="⚙", 
            command=self.open_settings,
            width=3
        )
        self.settings_button.pack(anchor='ne')
        
        # 创建多行显示标签
        self.key_labels = []
        for _ in range(self.settings.settings["max_lines"]):
            label = ttk.Label(
                self.main_frame,
                text="",
                font=('Arial', self.settings.settings["font_size"])
            )
            label.pack(pady=2)
            self.key_labels.append(label)
        
        self.apply_settings()

    def setup_keyboard_listener(self):
        self.listener = keyboard.Listener(
            on_press=self.on_press,
            on_release=self.on_release
        )
        self.listener.start()
        self.update_display()

    def open_settings(self):
        SettingsWindow(self.root, self.settings, self.apply_settings)

    def apply_settings(self):
        # 应用新设置
        self.root.configure(bg=self.settings.settings["bg_color"])
        
        # 更新标签数量
        while len(self.key_labels) < self.settings.settings["max_lines"]:
            label = ttk.Label(
                self.main_frame,
                text="",
                font=('Arial', self.settings.settings["font_size"])
            )
            label.pack(pady=2)
            self.key_labels.append(label)
        
        while len(self.key_labels) > self.settings.settings["max_lines"]:
            self.key_labels[-1].destroy()
            self.key_labels.pop()
        
        # 更新所有标签的样式
        style = ttk.Style()
        style.configure(
            'Custom.TLabel',
            background=self.settings.settings["bg_color"],
            foreground=self.settings.settings["text_color"],
            font=('Arial', self.settings.settings["font_size"])
        )
        
        for label in self.key_labels:
            label.configure(
                style='Custom.TLabel',
                font=('Arial', self.settings.settings["font_size"])
            )

    def on_press(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key).replace('Key.', '')
        
        current_time = datetime.now()
        self.current_keys.add(key_name)
        
        # 记录新的按键组合
        if self.current_keys:
            keys_text = " + ".join(sorted(self.current_keys))
            self.key_history.append({
                'text': keys_text,
                'time': current_time
            })

    def on_release(self, key):
        try:
            key_name = key.char
        except AttributeError:
            key_name = str(key).replace('Key.', '')
        self.current_keys.discard(key_name)

    def update_display(self):
        current_time = datetime.now()
        
        # 清理过期的历史记录
        self.key_history = [
            h for h in self.key_history 
            if (current_time - h['time']).total_seconds() < self.settings.settings["display_time"]
        ]
        
        # 更新显示
        for i, label in enumerate(self.key_labels):
            if i < len(self.key_history):
                label.configure(text=self.key_history[-(i+1)]['text'])
            else:
                label.configure(text="")
        
        # 继续更新
        self.root.after(100, self.update_display)

    def cleanup(self):
        self.listener.stop()

def main():
    root = tk.Tk()
    root.title("键盘监听器")
    root.geometry("400x200")
    root.resizable(True, True)
    root.minsize(300, 100)
    
    app = KeyboardListener(root)
    root.protocol("WM_DELETE_WINDOW", lambda: [app.cleanup(), root.destroy()])
    
    root.mainloop()

if __name__ == '__main__':
    main() 
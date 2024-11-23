import tkinter as tk
from tkinter import ttk, colorchooser
from tkinter import messagebox
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
            "text_color": "#ffffff",
            "combination_timeout": 1.0  # 新增：组合键超时时间（秒）
        }
        self.settings = self.load_settings()

    def load_settings(self):
        try:
            if os.path.exists('settings.json'):
                loaded_settings = json.load(open('settings.json', 'r'))
                # 确保所有默认设置都存在
                for key in self.default_settings:
                    if key not in loaded_settings:
                        loaded_settings[key] = self.default_settings[key]
                return loaded_settings
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
        # 设置窗口样式
        self.window.configure(bg='#2B2B2B')
        self.window.title("设置")
        self.window.geometry("300x400")
        
        style = ttk.Style()
        
        # 设置框架样式
        main_frame = ttk.Frame(self.window, style='Dark.TFrame')
        main_frame.pack(fill='both', expand=True, padx=20, pady=20)
        
        # 设置标签和输入框样式
        style.configure('Settings.TLabel',
            background='#2B2B2B',
            foreground='#FFFFFF',
            font=('Segoe UI', 10),
            padding=(0, 5)
        )
        
        style.configure('Settings.TEntry',
            background='#3C3F41',
            foreground='#FFFFFF',
            fieldbackground='#3C3F41',
            insertcolor='#FFFFFF'
        )
        
        # 创建设置项
        self.create_setting_item(main_frame, "显示行数:", self.lines_var)
        self.create_setting_item(main_frame, "显示时间(秒):", self.time_var)
        self.create_setting_item(main_frame, "字体大小:", self.font_var)
        self.create_setting_item(main_frame, "组合键超时(秒):", self.timeout_var)
        
        # 颜色选择按钮
        ttk.Button(main_frame, 
                  text="选择背景颜色",
                  style='Settings.TButton',
                  command=self.choose_bg_color).pack(pady=10)
                  
        ttk.Button(main_frame,
                  text="选择文字颜色",
                  style='Settings.TButton',
                  command=self.choose_text_color).pack(pady=10)
        
        # 保存按钮
        ttk.Button(main_frame,
                  text="保存设置",
                  style='Save.TButton',
                  command=self.save_settings).pack(pady=20)

    def create_setting_item(self, parent, label_text, variable):
        frame = ttk.Frame(parent, style='Dark.TFrame')
        frame.pack(fill='x', pady=5)
        
        ttk.Label(frame,
                 text=label_text,
                 style='Settings.TLabel').pack(side='left')
                 
        ttk.Entry(frame,
                 textvariable=variable,
                 style='Settings.TEntry',
                 width=10).pack(side='right')

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
            self.settings.settings["combination_timeout"] = float(self.timeout_var.get())
            self.settings.save_settings()
            self.apply_callback()
            self.window.destroy()
        except ValueError:
            messagebox.showerror("错误", "请输入有效的数值")

class KeyboardListener:
    def __init__(self, root):
        self.root = root
        self.settings = Settings()
        
        # 初始化所有需要的属性
        self.key_history = []  # 已完成的组合键历史
        self.current_line_keys = []  # 存储当前行的按键
        self.key_counts = {}  # 新增：用于存储当前行中每个按键的计数
        self.last_key_time = datetime.now()  # 最后一次按键时间
        self.key_labels = []  # 显示标签列表
        self.main_frame = None
        self.settings_button = None
        
        try:
            self.setup_ui()
            self.setup_keyboard_listener()
        except Exception as e:
            messagebox.showerror("初始化错误", f"程序初始化失败: {str(e)}")
            raise

    def setup_ui(self):
        try:
            # 设置窗口样式
            self.root.configure(bg='#2B2B2B')
            self.root.title('键盘监听器')
            self.root.wm_attributes('-topmost', True)
            
            # 设置窗口圆角和边框（仅支持Windows）
            try:
                from ctypes import windll, byref, sizeof, c_int
                style = windll.user32.GetWindowLongW(self.root.winfo_id(), -20)
                style = style & ~0x80000000  # 移除WS_POPUP
                windll.user32.SetWindowLongW(self.root.winfo_id(), -20, style)
            except:
                pass

            # 主框架
            self.main_frame = ttk.Frame(self.root, style='Dark.TFrame')
            self.main_frame.pack(fill='both', expand=True, padx=15, pady=15)
            
            # 创建标题栏框架
            title_frame = ttk.Frame(self.main_frame, style='Dark.TFrame')
            title_frame.pack(fill='x', pady=(0, 10))
            
            # 标题
            title_label = ttk.Label(
                title_frame, 
                text="键盘监听", 
                style='Title.TLabel'
            )
            title_label.pack(side='left')
            
            # 设置按钮
            self.settings_button = ttk.Button(
                title_frame,
                text="⚙",
                style='Settings.TButton',
                width=3,
                command=self.open_settings
            )
            self.settings_button.pack(side='right')
            
            # 创建显示框架
            display_frame = ttk.Frame(self.main_frame, style='Display.TFrame')
            display_frame.pack(fill='both', expand=True)
            
            # 创建标签
            self.key_labels = []
            for i in range(self.settings.settings["max_lines"]):
                label_frame = ttk.Frame(display_frame, style='Dark.TFrame')
                label_frame.pack(fill='x', pady=3)
                
                label = ttk.Label(
                    label_frame,
                    text="",
                    style='KeyDisplay.TLabel'
                )
                label.pack(fill='x', padx=10, pady=5)
                self.key_labels.append(label)
            
            # 设置自定义样式
            self.setup_styles()
            
        except Exception as e:
            messagebox.showerror("UI错误", f"UI初始化失败: {str(e)}")
            raise

    def setup_styles(self):
        style = ttk.Style()
        
        # 配置颜色方案
        style.configure('Dark.TFrame', background='#2B2B2B')
        
        # 标题样式
        style.configure('Title.TLabel',
            background='#2B2B2B',
            foreground='#FFFFFF',
            font=('Segoe UI', 14, 'bold'),
            padding=(5, 5)
        )
        
        # 设置按钮样式
        style.configure('Settings.TButton',
            background='#3C3F41',
            foreground='#FFFFFF',
            font=('Segoe UI', 12),
            padding=(5, 5)
        )
        
        # 显示框架样式
        style.configure('Display.TFrame',
            background='#323232',
            relief='flat'
        )
        
        # 按键显示标签样式
        style.configure('KeyDisplay.TLabel',
            background='#323232',
            foreground='#A9B7C6',
            font=('Consolas', self.settings.settings["font_size"]),
            padding=(10, 5)
        )

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
            # 获取按键名称
            if hasattr(key, 'char') and key.char is not None:
                key_name = key.char
            else:
                # 处理特殊按键
                key_str = str(key).replace('Key.', '')
                
                # 处理数字键盘按键
                numpad_map = {
                    'num_lock': 'NumLock',
                    'numeric_0': '0',
                    'numeric_1': '1',
                    'numeric_2': '2',
                    'numeric_3': '3',
                    'numeric_4': '4',
                    'numeric_5': '5',
                    'numeric_6': '6',
                    'numeric_7': '7',
                    'numeric_8': '8',
                    'numeric_9': '9',
                    'decimal': '.',
                    'divide': '/',
                    'multiply': '*',
                    'subtract': '-',
                    'add': '+',
                    'num_decimal': '.',
                    'num_divide': '/',
                    'num_multiply': '*',
                    'num_subtract': '-',
                    'num_add': '+',
                    'num_enter': 'Enter'
                }
                
                # 如果是数字键盘按键，使映射后的值
                if key_str in numpad_map:
                    key_name = numpad_map[key_str]
                else:
                    key_name = key_str
            
            # 确保 key_name 不为 None 且是字符串
            if key_name is None or not isinstance(key_name, str):
                return
            
            current_time = datetime.now()
            time_diff = (current_time - self.last_key_time).total_seconds()
            
            # 如果超过超时时间，重置当前行
            if time_diff > self.settings.settings["combination_timeout"]:
                if self.current_line_keys:
                    self.add_to_history(self.format_current_keys())
                self.current_line_keys = []
                self.key_counts = {}
            
            # 更新按键计数
            if key_name in self.key_counts:
                self.key_counts[key_name] += 1
            else:
                self.key_counts[key_name] = 1
                self.current_line_keys.append(key_name)
            
            self.last_key_time = current_time
            self.update_display()
        except Exception as e:
            print(f"Error in on_press: {e}")

    def format_current_keys(self):
        # 格式化当前行的按键，包含计数信息
        formatted_keys = []
        for key in self.current_line_keys:
            count = self.key_counts.get(key, 1)
            if count > 1:
                formatted_keys.append(f"{key}×{count}")
            else:
                formatted_keys.append(key)
        return " + ".join(formatted_keys)

    def on_release(self, key):
        # 按键释放时不做特殊处理
        pass

    def update_display(self):
        try:
            current_time = datetime.now()
            time_diff = (current_time - self.last_key_time).total_seconds()
            
            # 如果超过超时时间，将当前行添加到历史
            if time_diff > self.settings.settings["combination_timeout"] and self.current_line_keys:
                self.add_to_history(self.format_current_keys())
                self.current_line_keys = []
                self.key_counts = {}
            
            # 清理过期的历史记录
            self.key_history = [
                h for h in self.key_history 
                if (current_time - h['time']).total_seconds() < self.settings.settings["display_time"]
            ]
            
            # 更新显示
            for i, label in enumerate(self.key_labels):
                if i == 0:  # 第一行显示当前正在输入的内容
                    current_text = self.format_current_keys() if self.current_line_keys else ""
                    label.configure(text=current_text)
                elif i <= len(self.key_history):
                    label.configure(text=self.key_history[-(i-1)]['text'])
                else:
                    label.configure(text="")
            
            # 继续更新
            self.root.after(50, self.update_display)
        except Exception as e:
            print(f"Error in update_display: {e}")

    def add_to_history(self, combination_text):
        if combination_text.strip():  # 只有非空组合才添加到历史记录
            self.key_history.append({
                'text': combination_text,
                'time': datetime.now()
            })

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
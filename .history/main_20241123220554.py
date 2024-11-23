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
        self.window.geometry("500x800")
        self.window.configure(bg='#2B2B2B')
        
        # 设置最小窗口大小
        self.window.minsize(450, 700)
        
        self.settings = settings
        self.apply_callback = apply_callback
        
        # 初始化变量
        self.lines_var = tk.StringVar(value=str(self.settings.settings["max_lines"]))
        self.time_var = tk.StringVar(value=str(self.settings.settings["display_time"]))
        self.font_var = tk.StringVar(value=str(self.settings.settings["font_size"]))
        self.timeout_var = tk.StringVar(value=str(self.settings.settings["combination_timeout"]))
        
        # 创建样式
        self.setup_styles()
        self.create_widgets()
        
        # 使设置窗口模态
        self.window.transient(parent)
        self.window.grab_set()
        
        # 窗口居中
        self.center_window(parent)

    def center_window(self, parent):
        # 获取父窗口位置和大小
        parent_x = parent.winfo_x()
        parent_y = parent.winfo_y()
        parent_width = parent.winfo_width()
        parent_height = parent.winfo_height()
        
        # 计算居中位置
        width = self.window.winfo_width()
        height = self.window.winfo_height()
        x = parent_x + (parent_width - width) // 2
        y = parent_y + (parent_height - height) // 2
        
        # 设置窗口位置
        self.window.geometry(f"+{x}+{y}")

    def setup_styles(self):
        style = ttk.Style()
        
        # 基本样式
        style.configure('Settings.TFrame',
            background='#2B2B2B'
        )
        
        # 标题样式
        style.configure('SettingsTitle.TLabel',
            background='#2B2B2B',
            foreground='#FFFFFF',
            font=('Segoe UI', 24, 'bold'),
            padding=(0, 15, 0, 25)
        )
        
        # 增加输入框和标签的大小
        style.configure('Settings.TLabel',
            background='#2B2B2B',
            foreground='#E8E8E8',
            font=('Segoe UI', 18),  # 增大字体
            padding=(5, 5)  # 增加内边距
        )
        
        # 提示文字样式
        style.configure('Tooltip.TLabel',
            background='#2B2B2B',
            foreground='#B0B0B0',
            font=('Segoe UI', 14),
            padding=(5, 5)
        )
        
        # 按钮样式
        style.configure('Settings.TButton',
            padding=(20, 12),
            font=('Segoe UI', 14, 'bold'),
            background='#404040',
            foreground='#FFFFFF'
        )
        
        # 保存按钮特殊样式
        style.configure('Save.TButton',
            padding=(25, 15),
            font=('Segoe UI', 16, 'bold'),
            background='#4CAF50',  # 绿色背景
            foreground='#FFFFFF'   # 白色文字
        )
        style.map('Save.TButton',
            background=[('active', '#45a049')],  # 鼠标悬停时的颜色
            foreground=[('active', '#FFFFFF')]
        )
        
        # 分组框样式
        style.configure('Settings.TLabelframe',
            background='#2B2B2B',
            foreground='#FFFFFF',
            padding=(25, 20)  # 增加内边距
        )
        style.configure('Settings.TLabelframe.Label',
            background='#2B2B2B',
            foreground='#A0A0A0',
            font=('Segoe UI', 18, 'bold')
        )

    def create_widgets(self):
        # 创建主滚动框架
        canvas = tk.Canvas(self.window, bg='#2B2B2B', highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.window, orient="vertical", command=canvas.yview)
        
        # 创建可滚动的框架
        scrollable_frame = ttk.Frame(canvas, style='Settings.TFrame')
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        # 在画布上创建窗口
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw", width=canvas.winfo_width())
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # 配置画布大小随窗口变化
        def configure_canvas(event):
            canvas.itemconfig(canvas.find_all()[0], width=event.width)
        canvas.bind('<Configure>', configure_canvas)
        
        # 配置鼠标滚轮
        def _on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        canvas.bind_all("<MouseWheel>", _on_mousewheel)
        
        # 放置滚动组件
        canvas.pack(side="left", fill="both", expand=True, padx=(20, 0))
        scrollbar.pack(side="right", fill="y", padx=(0, 5))

        # 主容器
        main_frame = ttk.Frame(scrollable_frame, style='Settings.TFrame')
        main_frame.pack(fill='both', expand=True, padx=25, pady=20)
        
        # 标题
        title_label = ttk.Label(
            main_frame,
            text="设置",
            style='SettingsTitle.TLabel'
        )
        title_label.pack(fill='x', pady=(0, 15))

        # 基本设置组
        basic_frame = ttk.LabelFrame(
            main_frame,
            text="基本设置",
            style='Settings.TLabelframe'
        )
        basic_frame.pack(fill='x', pady=(0, 15), padx=5)

        # 创建设置项
        settings = [
            ("显示行数", self.lines_var, "行", "设置显示的历史记录行数"),
            ("显示时间", self.time_var, "秒", "设置每条记录的显示持续时间"),
            ("字体大小", self.font_var, "px", "设置显示文字的大小"),
            ("组合键超时", self.timeout_var, "秒", "设置判断为新组合键的时间间隔")
        ]

        for text, var, unit, tooltip in settings:
            frame = ttk.Frame(basic_frame, style='Settings.TFrame')
            frame.pack(fill='x', pady=12)
            
            # 标签和提示
            label_frame = ttk.Frame(frame, style='Settings.TFrame')
            label_frame.pack(fill='x')
            
            ttk.Label(
                label_frame,
                text=text,
                style='Settings.TLabel'
            ).pack(side='left')
            
            ttk.Label(
                label_frame,
                text=tooltip,
                style='Tooltip.TLabel'
            ).pack(side='left', padx=(15, 0))
            
            # 输入框和单位
            entry_frame = ttk.Frame(frame, style='Settings.TFrame')
            entry_frame.pack(fill='x', pady=(8, 0))
            
            # 创建自定义输入框
            entry = tk.Entry(
                entry_frame,
                textvariable=var,
                width=8,
                font=('Segoe UI', 16),
                bg='#3C3F41',
                fg='#FFFFFF',
                insertbackground='white',
                selectbackground='#4B6EAF',
                selectforeground='#FFFFFF',
                relief='flat',
                bd=2
            )
            entry.pack(side='left')
            
            # 添加输入框的悬停效果
            def on_enter(e):
                e.widget.config(bg='#454545')
            
            def on_leave(e):
                e.widget.config(bg='#3C3F41')
            
            entry.bind('<Enter>', on_enter)
            entry.bind('<Leave>', on_leave)
            
            # 添加输入框获取焦点时的边框效果
            def on_focus_in(e):
                e.widget.config(bd=2)
            
            def on_focus_out(e):
                e.widget.config(bd=1)
            
            entry.bind('<FocusIn>', on_focus_in)
            entry.bind('<FocusOut>', on_focus_out)
            
            ttk.Label(
                entry_frame,
                text=unit,
                style='Settings.TLabel'
            ).pack(side='left', padx=(10, 0))

            # 添加输入验证
            def validate_input(action, value_if_allowed):
                if action == '1':  # 插入操作
                    if unit == "px":  # 字体大小只允许整数
                        return value_if_allowed.isdigit()
                    try:
                        if value_if_allowed:
                            float(value_if_allowed)
                        return True
                    except ValueError:
                        return False
                return True
            
            vcmd = (entry.register(validate_input), '%d', '%P')
            entry.config(validate='key', validatecommand=vcmd)

        # 颜色设置组
        color_frame = ttk.LabelFrame(
            main_frame,
            text="颜色设置",
            style='Settings.TLabelframe'
        )
        color_frame.pack(fill='x', pady=(0, 20), padx=5)

        # 颜色预览框架
        preview_frame = ttk.Frame(color_frame, style='Settings.TFrame')
        preview_frame.pack(fill='x', pady=(0, 10))
        
        # 背景色预览
        self.bg_preview = tk.Label(
            preview_frame,
            text="背景色",
            width=15,
            height=2,
            bg=self.settings.settings["bg_color"],
            fg=self.settings.settings["text_color"]
        )
        self.bg_preview.pack(side='left', padx=5)
        
        # 文字色预览
        self.text_preview = tk.Label(
            preview_frame,
            text="文字色",
            width=15,
            height=2,
            bg=self.settings.settings["text_color"],
            fg=self.settings.settings["bg_color"]
        )
        self.text_preview.pack(side='right', padx=5)

        # 颜色选择按钮
        ttk.Button(
            color_frame,
            text="选择背景颜色",
            command=self.choose_bg_color,
            style='Settings.TButton'
        ).pack(fill='x', pady=(0, 5), padx=5)
        
        ttk.Button(
            color_frame,
            text="选择文字颜色",
            command=self.choose_text_color,
            style='Settings.TButton'
        ).pack(fill='x', pady=(0, 5), padx=5)

        # 修改底部按钮框架的样式和布局
        button_frame = ttk.Frame(self.window, style='Settings.TFrame')
        button_frame.pack(side='bottom', fill='x', padx=25, pady=20)
        
        # 创建一个内部框架来容纳按钮
        buttons_container = ttk.Frame(button_frame, style='Settings.TFrame')
        buttons_container.pack(expand=True)
        
        # 保存按钮 - 使用更醒目的样式
        save_button = tk.Button(  # 使用 tk.Button 而不是 ttk.Button 以获得更好的样式控制
            buttons_container,
            text="保存设置",
            command=self.save_settings,
            font=('Segoe UI', 16, 'bold'),
            bg='#4CAF50',
            fg='#FFFFFF',
            activebackground='#45a049',
            activeforeground='#FFFFFF',
            relief='flat',
            padx=30,
            pady=15,
            cursor='hand2'  # 鼠标悬停时显示手型光标
        )
        save_button.pack(side='right', padx=10)
        
        # 取消按钮 - 使用较低调的样式
        cancel_button = tk.Button(
            buttons_container,
            text="取消",
            command=self.window.destroy,
            font=('Segoe UI', 14),
            bg='#404040',
            fg='#FFFFFF',
            activebackground='#4d4d4d',
            activeforeground='#FFFFFF',
            relief='flat',
            padx=20,
            pady=15,
            cursor='hand2'
        )
        cancel_button.pack(side='right', padx=10)

        # 添加按钮悬停效果
        def on_enter(e):
            e.widget['background'] = e.widget['activebackground']
        
        def on_leave(e):
            e.widget['background'] = e.widget.default_bg
        
        for button in (save_button, cancel_button):
            button.default_bg = button['background']
            button.bind('<Enter>', on_enter)
            button.bind('<Leave>', on_leave)

    def choose_bg_color(self):
        color = colorchooser.askcolor(self.settings.settings["bg_color"])[1]
        if color:
            self.settings.settings["bg_color"] = color
            self.bg_preview.configure(bg=color)
            self.text_preview.configure(fg=color)

    def choose_text_color(self):
        color = colorchooser.askcolor(self.settings.settings["text_color"])[1]
        if color:
            self.settings.settings["text_color"] = color
            self.text_preview.configure(bg=color)
            self.bg_preview.configure(fg=color)

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
        # 按键释放时不做特处理
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
    root.geometry("400x300")  # 设置初始窗口大小
    
    # Windows系统下设置DPI感知
    try:
        from ctypes import windll
        windll.shcore.SetProcessDpiAwareness(1)
    except:
        pass
    
    app = KeyboardListener(root)
    root.mainloop()

if __name__ == '__main__':
    main() 
import tkinter as tk
from tkinter import ttk, messagebox
import queue
import platform
import webbrowser

# 全局配置
MAIN_BG = "#ffffff"  # 主程序背景白色
MAIN_FG = "#000000"  # 主程序字体黑色
ACCENT_COLOR = "#569cd6"
# FONT_NAME = "微软雅黑" if platform.system() == "Windows" else "PingFang SC"
FONT_NAME = "Segoe UI"  # 现代字体

# 项目仓库URL
PROJECT_URL = "https://github.com/Zeiwoos/SoulPlay"

MJAI_TILE_2_UNICODE = {  # https://en.wikipedia.org/wiki/Mahjong_Tiles_(Unicode_block)
    '1m': '🀇', '2m': '🀈', '3m': '🀉', '4m': '🀊', '5mr': '🀋',
    '5m': '🀋', '6m': '🀌', '7m': '🀍', '8m': '🀎', '9m': '🀏',
    '1p': '🀙', '2p': '🀚', '3p': '🀛', '4p': '🀜', '5pr': '🀝',
    '5p': '🀝', '6p': '🀞', '7p': '🀟', '8p': '🀠', '9p': '🀡',
    '1s': '🀐', '2s': '🀑', '3s': '🀒', '4s': '🀓', '5sr': '🀔',
    '5s': '🀔', '6s': '🀕', '7s': '🀖', '8s': '🀗', '9s': '🀘',
    'E': '🀀', 'S': '🀁', 'W': '🀂', 'N': '🀃',
    'P': '🀆', 'F': '🀅', 'C': '🀄',
    '?': '🀫'
}

# 全局实例
_root = tk.Tk()
_floating_window = None
_queue = queue.Queue()


class FloatingWindow(tk.Toplevel):
    def __init__(self, parent, pos_mode="center"):
        super().__init__(parent)
        self.pos_mode = pos_mode
        self._offset = (0, 0)
        self.configure_window()
        self.create_widgets()
        self.bind_events()

    def configure_window(self):
        self.attributes("-alpha", 0.9)
        self.attributes("-topmost", True)
        self.overrideredirect(True)
        # 移除透明设置，使背景显示深灰色
        self.configure(bg="#2d2d2d")

        window_width, window_height = 300, 200
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()

        if self.pos_mode == "center":
            x = (screen_width - window_width) // 2
            y = (screen_height - window_height) // 2
        elif self.pos_mode == "bottom-right":
            # 计算屏幕右下象限中心位置
            center_x = int(screen_width * 3 / 4)
            center_y = int(screen_height * 3 / 4)
            x = center_x - window_width // 2
            y = center_y - window_height // 2
        else:
            x, y = 100, 100

        self.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def create_widgets(self):
        self.label = tk.Label(
            self, text="悬浮提示", font=(FONT_NAME, 12),
            fg="#000000", bg="#2d2d2d", wraplength=280
        )
        self.label.pack(expand=True, fill="both", padx=10, pady=10)

        self.close_btn = ttk.Button(
            self, text="×", width=2,
            command=self.destroy, style="Floating.TButton"
        )
        self.close_btn.place(x=270, y=5)

    def bind_events(self):
        self.bind("<Button-1>", self.start_move)
        self.bind("<B1-Motion>", self.on_move)

    def start_move(self, event):
        self._offset = (event.x, event.y)

    def on_move(self, event):
        x = self.winfo_x() + (event.x - self._offset[0])
        y = self.winfo_y() + (event.y - self._offset[1])
        self.geometry(f"+{x}+{y}")


class ToolBar(tk.Frame):
    """工具栏类，用于创建带有图标和悬停提示的按钮"""

    def __init__(self, master, height=60):
        super().__init__(master)
        self.height = height
        self.configure(bg="#f0f0f0")
        self.pack(fill=tk.X, pady=5)
        self._hover_text = None

    def add_button(self, text, img_file, command):
        """添加按钮到工具栏"""
        try:
            img = tk.PhotoImage(file=img_file)
            img = img.subsample(int(img.width() / self.height), int(img.height() / self.height))
        except Exception as e:
            print(f"加载图像时出错: {e}")
            img = None

        btn = tk.Button(
            self,
            text=text,
            image=img,
            compound=tk.TOP,
            width=self.height + 10,
            height=self.height + 10,
            command=command,
            bg="#f0f0f0",
            relief=tk.FLAT,
            font=("Segoe UI", 8)
        )
        btn.image = img  # 保持对图像的引用，防止被垃圾回收
        btn.pack(side=tk.LEFT, padx=4, pady=4)

        # 添加悬停提示
        btn.bind("<Enter>", lambda event, t=text: self.show_hover_text(event, t))
        btn.bind("<Leave>", self.hide_hover_text)

        return btn

    def show_hover_text(self, event, text):
        """显示悬停提示"""
        if self._hover_text:
            self.hide_hover_text()
        self._hover_text = tk.Label(
            self,
            text=text,
            bg="#ffffe0",
            relief=tk.SOLID,
            # borderwidth=1,
            padx=5,
            pady=2
        )
        self._hover_text.pack(side=tk.LEFT, padx=5)
        self._hover_text.place(x=event.x_root, y=event.y_root + 20)

    def hide_hover_text(self, event=None):
        """隐藏悬停提示"""
        if self._hover_text:
            self._hover_text.destroy()
            self._hover_text = None

    def add_sep(self):
        """添加分隔符"""
        separator = ttk.Separator(self, orient=tk.VERTICAL)
        separator.pack(side=tk.LEFT, fill='y', expand=False, padx=5)


class PromptUI:
    def __init__(self, root, queue):
        icon = tk.PhotoImage(file='assets/icon.png')
        root.iconphoto(False, icon)

        self.root = root
        self.root.title("麻将辅助系统")
        self.root.geometry("620x540")
        self.root.minsize(620, 540)
        # self.root.configure(bg="#f0f0f0")
        self.queue = queue
        self.floating_visible = False
        # 定义两种定位模式：屏幕中间和右下角中间
        self.floating_modes = ["center", "bottom-right"]
        self.current_mode_index = 0
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_toolbar()

        self.setup_style()
        self.create_widgets()
        # self.setup_menu()
        self.check_queue()

    def create_toolbar(self):
        """创建工具栏"""
        self.toolbar = ToolBar(self.main_frame, height=50)

        # 项目图标按钮
        project_btn = self.toolbar.add_button(
            text="项目仓库",
            img_file="assets/github.png",  # 替换为实际的图标文件路径
            command=self.open_project
        )

        # 帮助按钮
        help_btn = self.toolbar.add_button(
            text="帮助",
            img_file="resources/help.png",  # 替换为实际的图标文件路径
            command=self.show_help
        )

        # 日志按钮
        log_btn = self.toolbar.add_button(
            text="日志",
            img_file="resources/log.png",  # 替换为实际的图标文件路径
            command=self.open_log
        )

        # 添加分隔符
        self.toolbar.add_sep()

        # # 开始运行按钮
        # start_btn = self.toolbar.add_button(
        #     text="开始运行",
        #     img_file="start_icon.png",  # 替换为实际的图标文件路径
        #     command=self.start_listening
        # )

    def open_project(self):
        """打开项目仓库"""
        webbrowser.open("https://github.com/Zeiwoos/SoulPlay")

    def show_help(self):
        """显示帮助信息"""
        help_text = "麻将辅助系统使用指南\n\n1. 点击“项目仓库”按钮可以访问项目的GitHub页面。\n2. 点击“帮助”按钮可以查看使用指南。\n3. 点击“日志”按钮可以查看系统日志。"
        messagebox.showinfo("帮助", help_text)

    def open_log(self):
        """打开日志文件"""
        log_text = "系统日志\n\n- 系统启动: 2024-03-31 19:02:32\n- 模型加载完成: 2024-03-31 19:02:35\n- 开始监听游戏日志: 2024-03-31 19:02:38"
        messagebox.showinfo("日志", log_text)

    def start_listening(self):
        """开始监听游戏日志"""
        print("开始监听游戏日志")

    def setup_style(self):
        style = ttk.Style()
        style.theme_use("clam")
        style.configure("TButton",
                        background=MAIN_BG,
                        foreground=MAIN_FG,
                        relief="flat")
        style.map("TButton",
                  background=[("active", ACCENT_COLOR)])
        # 定义悬浮窗关闭按钮的样式为深色
        style.configure("Floating.TButton",
                        background="#2d2d2d",
                        foreground="#000000",
                        font=(FONT_NAME, 12),
                        relief="flat")

    def create_widgets(self):
        self.root.title("AI 行动提示控制台")
        self.root.geometry("550x350+500+300")
        # self.root.configure(bg=MAIN_BG)

        ai_frame = ttk.LabelFrame(self.main_frame, text="AI 提示")
        ai_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.label = tk.Label(
            ai_frame, text="等待新行动提示...", font=("Segoe UI", 20),
            wraplength=380, justify="left", relief=tk.SUNKEN, height=5)
        self.label.pack(expand=True, fill="both", padx=5, pady=5)

        # 创建一个frame，用于显示“手牌:”和牌面参数
        game_info_frame = ttk.LabelFrame(self.main_frame, text="当前手牌", relief=tk.SUNKEN)
        game_info_frame.pack(fill=tk.BOTH, expand=True, pady=5)
        # self.info_frame = ttk.Frame(self.main_frame)
        # self.info_frame.pack(fill=tk.BOTH, pady=5)
        # self.tile_frame = tk.Frame(self.info_frame, bg=MAIN_BG)
        # self.tile_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # # 静态标签，固定显示“手牌:”，字体大小固定
        # self.tile_static_label = tk.Label(
        #     game_info_frame, text="手牌:", font=(FONT_NAME, 15),
        #     relief=tk.SUNKEN, width=5, anchor="w")
        # self.tile_static_label.pack(side="top",pady=20,fill=tk.BOTH, expand=True)

        # 动态标签，用于显示牌面参数，字体放大到30号
        self.tile_value_label = tk.Label(
            game_info_frame, text="",
            font=(FONT_NAME, 30), relief=tk.SUNKEN, wraplength=380, justify="left")
        self.tile_value_label.pack(side="top", fill=tk.BOTH, expand=True)

        control_frame = ttk.Frame(self.main_frame)
        control_frame.pack(pady=20)
        toggle_btn = ttk.Button(control_frame, text="开关悬浮窗", command=self.toggle_floating)
        toggle_btn.pack(side=tk.BOTTOM, padx=5)

    # def setup_menu(self):
    #     menu = tk.Menu(self.root, bg=MAIN_BG, fg=MAIN_FG)
    #     self.root.config(menu=menu)
    #     view_menu = tk.Menu(menu, bg=MAIN_BG, fg=MAIN_FG)
    #     menu.add_cascade(label="视图", menu=view_menu)
    #     view_menu.add_command(label="切换悬浮窗", command=self.toggle_floating)

    def toggle_floating(self):
        global _floating_window
        if self.floating_visible:
            if _floating_window:
                _floating_window.destroy()
            self.floating_visible = False
        else:
            mode = self.floating_modes[self.current_mode_index]
            _floating_window = FloatingWindow(self.root, pos_mode=mode)
            self.floating_visible = True
            # 切换到下一个定位模式
            self.current_mode_index = (self.current_mode_index + 1) % len(self.floating_modes)

    def check_queue(self):
        # 处理队列中的数据更新
        while not self.queue.empty():
            item = self.queue.get_nowait()
            if isinstance(item, dict):
                # 如果包含提示信息，则更新提示
                if "prompt" in item:
                    prompt = item["prompt"]
                    self.label.config(text=prompt)
                    if self.floating_visible and _floating_window:
                        _floating_window.label.config(text=prompt)
                # 如果包含 tile_manager 参数，则更新手牌显示
                if "hands" in item:
                    hands = item.get("hands", "")
                    self.tile_value_label.config(text=hands)
            else:
                # 如果不是字典，则认为是简单的提示字符串
                self.label.config(text=item)
                if self.floating_visible and _floating_window:
                    _floating_window.label.config(text=item)
        self.root.after(100, self.check_queue)


# 全局 UI 实例
_ui = PromptUI(_root, _queue)


def convert_hand_to_unicode(hand):
    return ''.join(MJAI_TILE_2_UNICODE.get(tile, tile) for tile in hand)


def update_ui_prompt(prompt):
    """接口函数：更新提示信息"""
    print(f"更新提示信息: {prompt}")
    data = {"prompt": prompt}
    _queue.put(data)


def update_tile_manager(hands):
    """接口函数：更新 tile_manager 参数（手牌）"""
    converted = convert_hand_to_unicode(hands)
    data = {"hands": converted}
    _queue.put(data)


def start_ui():
    """启动UI系统"""
    _root.mainloop()
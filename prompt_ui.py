import tkinter as tk
from tkinter import ttk
import queue
import platform

# 全局配置
MAIN_BG = "#ffffff"        # 主程序背景白色
MAIN_FG = "#000000"        # 主程序字体黑色
ACCENT_COLOR = "#569cd6"
FONT_NAME = "微软雅黑" if platform.system() == "Windows" else "PingFang SC"

MJAI_TILE_2_UNICODE = {      # https://en.wikipedia.org/wiki/Mahjong_Tiles_(Unicode_block)
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

        window_width, window_height = 300, 80
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


class PromptUI:
    def __init__(self, root, queue):
        self.root = root
        self.root.title("麻将辅助系统")
        self.root.geometry("600x450")
        self.root.minsize(600, 450)
        self.root.configure(bg=MAIN_BG)
        self.queue = queue
        self.floating_visible = False
        # 定义两种定位模式：屏幕中间和右下角中间
        self.floating_modes = ["center", "bottom-right"]
        self.current_mode_index = 0
        # 创建主框架
        self.main_frame = ttk.Frame(self.root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.setup_style()
        self.create_widgets()
        self.setup_menu()
        self.check_queue()

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
        self.root.configure(bg=MAIN_BG)

        ai_frame = ttk.LabelFrame(self.main_frame, text="AI 提示")
        ai_frame.pack(fill=tk.BOTH, expand=True, pady=10)
        self.label = tk.Label(
            ai_frame, text="等待新行动提示...", font=("Segoe UI", 20),
         fg=MAIN_FG, bg=MAIN_BG, wraplength=380, justify="left")
        self.label.pack(expand=True, fill="both", padx=5, pady=5)

        # 创建一个frame，用于显示“手牌:”和牌面参数
        self.info_frame = ttk.Frame(self.main_frame)
        self.info_frame.pack(fill=tk.BOTH, pady=5)
        self.tile_frame = tk.Frame(self.info_frame, bg=MAIN_BG)
        self.tile_frame.pack(fill=tk.BOTH, padx=5, pady=5)

        # 静态标签，固定显示“手牌:”，字体大小固定
        self.tile_static_label = tk.Label(
            self.tile_frame, text="手牌:", font=(FONT_NAME, 10),
            fg=MAIN_FG, bg=MAIN_BG, width=5, anchor="w")
        self.tile_static_label.pack(side="top")

        # 动态标签，用于显示牌面参数，字体放大到30号
        self.tile_value_label = tk.Label(
            self.tile_frame, text="",
            font=(FONT_NAME, 30), fg=MAIN_FG, bg=MAIN_BG, wraplength=380, justify="left")
        self.tile_value_label.pack(side="top")

        control_frame = ttk.Frame(self.info_frame)
        control_frame.pack(pady=5)
        toggle_btn = ttk.Button(control_frame, text="开关悬浮窗", command=self.toggle_floating)
        toggle_btn.pack(side=tk.LEFT, padx=5)

        # self.control_frame = ttk.Frame(self.root)
        # self.control_frame.pack(pady=5)
        #
        # self.toggle_btn = ttk.Button(
        #     self.control_frame, text="开关悬浮窗",
        #     command=self.toggle_floating)
        # self.toggle_btn.pack(side=tk.LEFT, padx=5)

    def setup_menu(self):
        menu = tk.Menu(self.root, bg=MAIN_BG, fg=MAIN_FG)
        self.root.config(menu=menu)
        view_menu = tk.Menu(menu, bg=MAIN_BG, fg=MAIN_FG)
        menu.add_cascade(label="视图", menu=view_menu)
        view_menu.add_command(label="切换悬浮窗", command=self.toggle_floating)

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

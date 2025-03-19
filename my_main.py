import tkinter as tk
import threading
import queue
import time
from get_react import react_api
from testThread import read_whole_game_log  # 请确保这两个函数已实现，并在适当时调用 update_ui(prompt)
from prompt_ui import _root  # 请确保这个函数已实现

# 全局线程安全队列，用于更新提示信息
prompt_queue = queue.Queue()


def update_ui(prompt):
    """
    全局 API：后台线程调用此函数，将提示信息放入全局队列。
    """
    prompt_queue.put(prompt)


class MainUI:
    def __init__(self, root):
        self.root = root
        self.root.title("主控制界面")
        self.root.geometry("500x300")
        self.root.configure(bg="#2e2e2e")

        # 动态提示标签：显示最新的提示信息
        self.prompt_label = tk.Label(
            self.root,
            text="等待新提示...",
            font=("Helvetica", 16),
            fg="#ffffff",
            bg="#2e2e2e",
            wraplength=480,
            justify="left"
        )
        self.prompt_label.pack(pady=20)

        # 按钮区域
        button_frame = tk.Frame(self.root, bg="#2e2e2e")
        button_frame.pack(pady=10)

        self.start_button = tk.Button(
            button_frame,
            text="开始运行",
            font=("Helvetica", 14),
            command=self.start_listening
        )
        self.start_button.grid(row=0, column=0, padx=10)

        self.hud_button = tk.Button(
            button_frame,
            text="开启HUD",
            font=("Helvetica", 14),
            command=self.open_hud
        )
        self.hud_button.grid(row=0, column=1, padx=10)

        self.close_button = tk.Button(
            button_frame,
            text="关闭",
            font=("Helvetica", 14),
            command=self.root.destroy
        )
        self.close_button.grid(row=0, column=2, padx=10)

        # 定时检查全局队列，更新提示标签
        self.check_queue()

        self.threads_started = False

    def check_queue(self):
        """
        定期检查全局队列，如果有新提示信息，则更新主界面和 HUD（如果开启）。
        """
        while not prompt_queue.empty():
            new_prompt = prompt_queue.get_nowait()
            self.prompt_label.config(text=new_prompt)
            if hasattr(self, 'hud_label') and self.hud_label is not None:
                self.hud_label.config(text=new_prompt)
        self.root.after(100, self.check_queue)

    def start_listening(self):
        """
        启动 react_api 和 read_whole_game_log 后台线程，并禁用“开始运行”按钮。
        """
        if not self.threads_started:
            self.threads_started = True
            threading.Thread(target=react_api, daemon=True).start()
            threading.Thread(target=read_whole_game_log, daemon=True).start()
            self.start_button.config(state="disabled", text="监听中...")

    def open_hud(self):
        """
        创建 HUD 窗口（如果不存在）并置顶显示。
        HUD 为无边框透明灰色小窗口，信息实时更新。
        """
        if not hasattr(self, 'hud_window') or self.hud_window is None or not self.hud_window.winfo_exists():
            self.hud_window = tk.Toplevel(self.root)
            self.hud_window.overrideredirect(True)  # 去除边框
            self.hud_window.attributes("-topmost", True)  # 置顶显示
            self.hud_window.geometry("400x100+50+50")  # 窗口大小和位置
            self.hud_window.configure(bg="#1e1e1e")
            self.hud_window.attributes("-alpha", 0.8)  # 80% 不透明

            self.hud_label = tk.Label(
                self.hud_window,
                text="HUD 提示",
                font=("Helvetica", 14),
                fg="#ffffff",
                bg="#1e1e1e",
                wraplength=380,
                justify="left"
            )
            self.hud_label.pack(expand=True, fill="both", padx=10, pady=10)

            close_hud_button = tk.Button(
                self.hud_window,
                text="关闭HUD",
                font=("Helvetica", 10),
                command=self.close_hud,
                fg="#ffffff",
                bg="#333333",
                relief="flat"
            )
            close_hud_button.pack(side="bottom", pady=5)
        else:
            self.hud_window.lift()

    def close_hud(self):
        """
        关闭 HUD 窗口。
        """
        if hasattr(self, 'hud_window') and self.hud_window is not None:
            self.hud_window.destroy()
            self.hud_window = None
            self.hud_label = None


if __name__ == "__main__":
    # 只创建一个 Tk 实例，并在主线程中运行主控制界面
    _root = tk.Tk()
    app = MainUI(_root)
    _root.mainloop()

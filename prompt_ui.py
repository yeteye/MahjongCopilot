# ui_update.py
import tkinter as tk
import queue

# 创建全局 Tk 实例和 PromptUI 对象（确保只创建一次 UI）
_root = tk.Tk()
_root.title("AI 行动提示")
_root.geometry("400x150")
_root.configure(bg="#1e1e1e")

_queue = queue.Queue()

class PromptUI:
    def __init__(self, root, queue):
        self.root = root
        self.queue = queue
        self.label = tk.Label(
            root, text="等待新行动提示...", font=("Helvetica", 14),
            fg="#b0b0b0", bg="#1e1e1e", wraplength=380, justify="left"
        )
        self.label.pack(expand=True, fill="both", padx=10, pady=10)
        self.check_queue()

    def update_prompt(self, prompt):
        self.label.config(text=prompt)

    def check_queue(self):
        while not self.queue.empty():
            prompt = self.queue.get_nowait()
            self.update_prompt(prompt)
        self.root.after(100, self.check_queue)

# 全局 UI 实例
_ui = PromptUI(_root, _queue)

def update_ui(prompt):
    """在外部线程调用此函数，将提示信息放入全局队列"""
    _queue.put(prompt)

def start_ui():
    """启动 Tkinter UI 主循环"""
    _root.mainloop()

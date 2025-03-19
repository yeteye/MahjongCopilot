from prompt_ui import _root
from testThread import main
import threading

if __name__ == '__main__':
    # 将main()放在一个单独的线程中
    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()

    # 将_root.mainloop()放在主线程中
    _root.mainloop()
from prompt_ui import _root
from testThread import main
import threading
from my_ini import init

if __name__ == '__main__':
    init()

    main_thread = threading.Thread(target=main, daemon=True)
    main_thread.start()

    _root.mainloop()
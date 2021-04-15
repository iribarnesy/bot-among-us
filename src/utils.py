import pyautogui
from threading import Lock, Thread


class SingletonMeta(type):
    """
    This is a thread-safe implementation of Singleton.
    Source: https://refactoring.guru/fr/design-patterns/singleton/python/example#example-0
    """

    _instances = {}
    _lock: Lock = Lock()

    def __call__(cls, *args, **kwargs):
        """
        Possible changes to the value of the `__init__` argument do not affect
        the returned instance.
        """
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        return cls._instances[cls]

def FOCUS_AMONG_SCREEN():
    among_window = pyautogui.getWindowsWithTitle("Among Us")[0]
    if not among_window.isActive:
        if among_window.isMaximized:
            among_window.minimize()
        among_window.maximize()
        pyautogui.click(among_window.center)
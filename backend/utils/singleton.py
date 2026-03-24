from typing import Any
from threading import Lock

class Singleton(type):
    _instances = {}

    _lock: Lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        
        return cls._instances[cls]
    
    def _reset_instances(self):
        "This method should be used for testing only to clear the singleton"
        "This helps with State Pollution"
        self._instances = {}

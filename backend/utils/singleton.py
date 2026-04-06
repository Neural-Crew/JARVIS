from typing import Any
from threading import Lock

class Singleton(type):
    _instances = {}

    _lock: Lock = Lock()
    
    def __call__(cls, *args, **kwargs):
        """
        Methode permettant de mettre en place un singleton de manière organisée
        On prevoie aussi une protection dans le cas du multithreading
        Un lock est mis en place lors de la creation d'une instace. Si
        dans le constructeur de l'instance, on fait appel à une autre
        classe qui à comme metaclasse Singleton, un deadlock va se produire
        Dans ce cas veillez mettre en paramètre de la classe implementant
        singleton un lock.
        ex: Class(parametre1, parametre2, lock=Lock())
        Ceci evitera effectivement un interbloquage et respectera l'aspect singleton de
        la classe.
        """
        lock = cls._lock if 'lock' not in kwargs else kwargs['lock']
        with lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, **kwargs)
                cls._instances[cls] = instance
        
        return cls._instances[cls]
    
    def _reset_instances(self):
        """
        ! Utiliser cette méthode uniquement pour effectuer des tests ! 
        permettant de reinitialiser le singleton dans le cas ou on souhaite 
        recréer l'instance etc...
        Ceci aide avec ce qu'on appelle 'State Pollution' / 
        This method should be used for testing only to clear the singleton"
        This helps with State Pollution
        """
        self._instances = {}

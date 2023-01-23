from abc import ABC, abstractmethod
from dataclasses import dataclass
import os
import json
from typing import Dict


class Store(ABC):
    _path = "store"

    def __init__(self, store: str = "store"):
        self._path = os.path.join(store)
        if not os.path.exists(self._path):
            os.mkdir(self._path)

    def toJSON(self, data: Dict):
        return json.dumps(self, default=lambda o: data,
                          sort_keys=True, indent=4)



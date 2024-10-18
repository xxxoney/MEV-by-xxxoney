from typing import List, Tuple, Any
from dataclasses import dataclass


@dataclass
class Field:
    name: str = ""
    value: Any = 0


@dataclass
class Data:
    files: List[Tuple]
    fields: List[Field]

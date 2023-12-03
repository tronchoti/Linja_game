from enum import Enum
class Color(Enum):
    RED = 1
    BLACK = 2

    def __str__(self) -> str:
        return self.name
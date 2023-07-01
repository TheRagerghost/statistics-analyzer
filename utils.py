import math
import random
from enum import Enum

class SplitType(Enum):
    inclusive = 0
    exclusive = 1

class FileExt(Enum):
    txt = "txt"
    png = "png"
    pdf = "pdf"
    xlsx = "xlsx"


def generate_random_ten(min: float = 10.0, max: float = 20.0, digits: int = 1) -> list[float]:
    numbers = []
    for _ in range(10):
        num = round_full(random.uniform(min, max), digits)
        numbers.append(num) 
    return numbers

def limit_digits(n: float | int, digits: int = 0):
    """
    Changes the number of digits in a float. 
    
    Returns integer if digits = 0 (default).
    """
    num = int(n) if digits == 0 else round_full(n, digits)
    return num

def show_as_percentage(n):
    return f"{n}%"

def round_full(n: float | int, digits = 0):
    return math.ceil(n * pow(10, digits)) / pow(10, digits) if n % 1 >= 0.5 else round(n, digits)

def round_half(n: float | int, digits = 0):
    return round_full(n * 2, digits) / 2
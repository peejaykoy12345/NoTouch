import math

def distance_2d(x1: float, y1: float, x2: float, y2: float) -> float:
    return math.hypot(x2 - x1, y2 - y1)

def is_extended(tip_y, pip_y, mcp_y) -> bool:
    return tip_y < pip_y < mcp_y
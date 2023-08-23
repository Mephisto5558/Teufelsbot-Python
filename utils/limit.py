def limit(n: float | int, min_val: int | float = float('-inf'), max_val: int | float = float('inf')):
  return min(max(float(n), min_val), max_val)

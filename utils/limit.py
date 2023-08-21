def limit(n, min_val=float('-inf'), max_val=float('inf')):
  return min(max(float(n), min_val), max_val)

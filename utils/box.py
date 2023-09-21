from box import Box

def box(*args, **kwargs):
  return Box(*args, default_box=True, default_box_attr=None, box_dots=True, **kwargs)

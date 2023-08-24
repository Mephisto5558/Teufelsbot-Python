from box import Box


def box(*args):
  return Box(*args, default_box=True, default_box_attr=None, box_dots=True)
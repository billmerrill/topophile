from indicies import *

def points_to_text(points):
    return "\n".join([" ".join([str(p[PX]), str(p[PZ]), str(p[PY])]) for p in points])

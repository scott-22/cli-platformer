# using hardcoded values instead of a quadratic for gravity because
# resolution is too low for trajectory to be be parabolic
def deltaheight(t):
    deltaheightvalues = [2, 1, 1, 0, 0, -1, -1, -2]
    return deltaheightvalues[t]
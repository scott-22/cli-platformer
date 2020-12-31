# using hardcoded values instead of a quadratic for gravity because
# resolution is too low so trajectory shouldn't be parabolic
def deltaheight(t):
    deltaheightvalues = [2, 1, 1, -1, -1, -2]
    return deltaheightvalues[t]
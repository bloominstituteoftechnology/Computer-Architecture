# Stack frames
# STack grows downward:
#
# 
# 701: return point 1
# 700: n=4
# 699: return point 2
# 698: n=3
# 697: return point 2
# 696: n=2
# 695: return point 2
# 694: n=1
# 693: return point 2
# 692: n = 0
# 691: 
# 690:
def count(n):
    if n == 0:
        return
    print(n)

    count(n-1)

    # return point 2
    return

count(4)
# return point 1
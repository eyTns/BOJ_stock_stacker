if True:

# fast IO
    import sys
    input = lambda:sys.stdin.readline().strip()
    print = lambda x:sys.stdout.write(f"{x}\n")

# round
    from math import floor
    round = lambda x: floor(x + 0.5)

# 격자에서 dfs
    # ...

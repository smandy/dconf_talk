def pnl( cost, delay, p, onDay):
    return -cost + (p * max(onDay - delay, 0))

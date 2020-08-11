def histogram(s):
    d = dict()
    for c in s:
        if c not in d:
            d[c] = 1
        else:
            d[c] += 1
    return d

def invert_dict(d):
    inverse = dict()
    for key in d:
        val = d[key]
        inverse.setdefault(val, []).append(key)
    return inverse

def ackerman(m, n):
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        return ackerman(m-1, 1)
    elif m > 0 and n > 0:
        return ackerman(m-1, ackerman(m, n-1))

cache = {}
def amoi_ackerman(m, n):
    if m == 0:
        return n + 1
    elif m > 0 and n == 0:
        cache[(m-1,1)] = amoi_ackerman(m-1, 1)
        return cache.get((m-1,1))
    elif m > 0 and n > 0:
        if cache.get((m,n-1)) != None:
            return amoi_ackerman(m-1,cache.get((m,n-1)))
        return amoi_ackerman(m-1, amoi_ackerman(m, n-1))


h = histogram('brontosaurus')
print(invert_dict(h))

print(ackerman(3,4))
print(amoi_ackerman(3,4))
print(str(cache))
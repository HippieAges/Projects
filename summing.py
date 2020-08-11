from functools import reduce

def sum_all(*vals):
    sum = 0
    for val in vals:
        sum += val
    return sum

def new_sum_all(*vals): # vals is an variable-length argument tuple 
    return int(reduce(lambda x,y: x+y, vals))

print(str(sum_all(1,2,3,4,5,6,7,8,9,10)))
print(str(new_sum_all(1,2,3,4,5,6,7,8,9,10)))
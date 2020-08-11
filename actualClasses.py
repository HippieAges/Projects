# class Time:
#     """Represents the time of day.
       
#     attributes: hour, minute, second
#     """
#     def time_to_int(self):
#         minutes = self.hour * 60 + self.minute
#         seconds = minutes * 60 + self.second
#         return seconds

# start = Time()
# start.hour = 9
# start.minute = 45
# start.second = 00
# print(start.time_to_int())

class Point:
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __str__(self):
        return '(%d,%d)' % (self.x,self.y)

    def __add__(self, other):
        if isinstance(other, Point):
            return (self.x + other.x,self.y + other.y)
        elif isinstance(other, tuple):
            return Point(self.x + other[0], self.y + other[1]) 
    
pt = Point(10,5)
new_pt = Point(5,10)
print(pt + new_pt)
print(pt + (1,4))

# chapter 17 exercise 2
class Kangaroo:
    def __init__(self):
        self.pouch_contents = []
    
    def put_in_pouch(self, other):
        self.pouch_contents.append(other)

    def __str__(self):
        return str(self.__class__) + ' '.join(map(str, self.pouch_contents))

kanga = Kangaroo()
roo = Kangaroo()
kanga.put_in_pouch(roo)
print(kanga)
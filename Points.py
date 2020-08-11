import math, turtle

class Point:
    '''attributes: x, y '''

def distance_between_points(pt1, pt2):
    return(math.sqrt((pt1.x + pt2.x)**2)+(pt1.y+pt2.y)**2)

point1 = Point()
point2 = Point()
point1.x = 1
point1.y = 1
point2.x = 5
point2.y = 5

print(distance_between_points(point1, point2))

# chapter 15 exercises

# exercise 1

class Rectangle:
    ''' attributes: width, height, and corner  '''

class Circle:
    ''' attributes: center, and radius '''

circle = Circle()
point = Point()
point.x = 150
point.y = 100
circle.center = point
circle.radius = 75

def point_in_circle(circle, pt):
    # on_boundary formula is the the equation of a circle formula #
    on_boundary = int(math.pow(pt.x - circle.center.x, 2) + math.pow(pt.y - circle.center.y, 2))
    if on_boundary == circle.radius**2:
        print("here")
        return True
    elif pt.x < circle.center.x - circle.radius or pt.x > circle.center.x + circle.radius:
        return False
    elif pt.y < circle.center.y - circle.radius or pt.y > circle.center.y + circle.radius:
        return False
    return True


testPoint = Point()
testPoint.x = 225
testPoint.y = 175
# print(point_in_circle(circle, testPoint))

rect = Rectangle()
rect.width = 50
rect.height = 25
rect.corner = Point()
# top left corner #
rect.corner.x = 150
rect.corner.y = 100

topRight = Point() 
topRight.x = rect.corner.x + rect.width
topRight.y = rect.corner.y
bottomLeft = Point()
bottomLeft.x = rect.corner.x
bottomLeft.y = rect.corner.y + rect.height
bottomRight = Point()
bottomRight.x = topRight.x
bottomRight.y = bottomLeft.y

def rect_in_circle(circle, rect):
    if not point_in_circle(circle, rect.corner) or not point_in_circle(circle, topRight):
        return False
    elif not point_in_circle(circle, bottomLeft) or not point_in_circle(circle, bottomRight):
        return False
    return True 
# print(rect_in_circle(circle, rect))

# exercise 2
def draw_rect(turtle, rect):
    # turtle.setposition(rect.corner.x, rect.corner.y)
    turtle.fd(rect.width)
    turtle.rt(90)
    turtle.fd(rect.height)
    turtle.rt(90)
    turtle.fd(rect.width)
    turtle.rt(90)
    turtle.fd(rect.height)
    turtle.rt(90)

turt = turtle.Turtle()
# draw_rect(turt, rect)

def draw_circle(turtle, circle):
    # turtle.shape("circle")
    turtle.circle(circle.radius)

draw_circle(turt, circle)
turtle.mainloop()
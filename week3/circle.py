class Circle:
    "Define a circle with only a given radius"

    def __init__(self,radius,pi=3.14159265359):
        "Initialise and save radius for the current object"
        self.radius = radius
        self.pi = pi

    def area(self):
        "Print out the area of a circle with the given radius"
        r  = self.radius
        pi = self.pi
        return pi*r*r

    def perimeter(self):
        "Print out the circumference/perimeter of a circle with the given radius"
        r = self.radius
        pi = self.pi
        return 2*pi*r

if __name__ == "__main__":
    r = float(raw_input('Please input a radius: '))
    c = Circle(float(r))
    print "A circle with radius %f has:" %r
    print "Area = {0}, Perimeter: {1}".format(c.area(), c.perimeter())

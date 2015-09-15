class FlexCircle(object):
    """Define a circle with only a given radius.
    If then area or perimeter is changed, the other value will
    be updated with the correct value"""

    def __init__(self,radius):
        "Initialise and save radius for the current object"
        if radius < 0:
            import sys
            print "Radius can't be negative, try again!"
            sys.exit()
        else:
            self.pi        = 3.14159265359
            self.radius    = radius

    @property
    def area(self):
		return self.radius**2*self.pi
    @area.setter
    def area(self, area):
        if area < 0:
            import sys
            print "Area can't be negative, try again!"
            sys.exit()
        else:
		    self.radius     = (area/self.pi)**(0.5)
		    self._perimeter = area*2.0/self.radius

    @property
    def perimeter(self):
        return self.radius*2*self.pi

    @perimeter.setter
    def perimeter(self, perimeter):
        if perimeter < 0:
            import sys
            print "Perimeter can't be negative, try again!"
            sys.exit()
        else:
            self.radius = perimeter/(2.0*self.pi)
            self._area  = self.pi*self.radius*self.radius


if __name__ == "__main__":
    c = FlexCircle(5)
    print "Initiating a FlexCircle object with radius = 5"
    print "Area, perimeter = ", c.area, ",", c.perimeter
    print "Now setting perimeter to 50.."
    c.perimeter = 50
    print "Area, perimeter = ", c.area, ",", c.perimeter
    print "Now setting area to -24.."
    c.area = -24
    print "Area, perimeter = ", c.area, ",", c.perimeter

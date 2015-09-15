class SomeClass(object):
    def __init__(self, n):
        self.list = range(0, n)

    @property
    def list(self):
        return self._list

    @list.setter
    def list(self, val):
        self._list = val
        self._listsquare = [x**2 for x in self._list ]

    @property
    def listsquare(self):
        return self._listsquare

    @listsquare.setter
    def listsquare(self, val):
        self.list = [int(pow(x, 0.5)) for x in val]

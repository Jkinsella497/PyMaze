class Box(object):
    def __init__(self):
        self.draw  = [True,True,True,True] #TBRL i.e. Top,Bottom,Left,Right
        self.visited = False
        self.end = False
        self.value = False
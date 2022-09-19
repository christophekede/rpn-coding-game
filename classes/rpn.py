
import operator  

class RPN:

    def __init__(self):
        self.stack = []

    def getStack(self):
        return self.stack

    def getLenStack(self):
        return len(self.stack)

    def addValueStack(self, val):
        self.stack.append(val)

    def popStack(self):
        return self.stack.pop()


    def calcul(self, ope):
        opes = {'+': operator.add, '-': operator.sub, '*': operator.mul, '/': operator.truediv}
        if(self.getLenStack() == 1):
            val = self.popStack()
            self.addValueStack(opes[ope](val, val))
        if(self.getLenStack() > 1):
            val1, val2 = self.popStack(), self.popStack()
            self.addValueStack(opes[ope](val2, val1))
    
        

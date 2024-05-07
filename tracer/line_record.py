class LineRecord:
    def __init__(self, funName, lineNumber):
        self.functionName = funName
        self.frequency = 1
        self.lineNumber = lineNumber

    def increaseFrequency(self):
        self.frequency += 1
        
    def print_report(self):
        print("{:<30} {:<10} {:<10}".format(self.functionName, self.lineNumber, self.frequency))

    def __eq__(self, other):
        if isinstance(other, LineRecord):
            return self.functionName == other.functionName and self.frequency == other.frequency and self.lineNumber == other.lineNumber
        return False

    @classmethod
    def new_instance_with(cls, funName, lineNumber, frequency):
        instance = cls(funName, lineNumber)
        instance.frequency = frequency
        return instance
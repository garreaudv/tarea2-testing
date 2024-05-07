from abstract_profiler import Profiler
from function_instrumentor import *
from function_record import FunctionRecord

# Clase que rastrea y reporta las funciones que se ejecutan
class FunctionProfiler(Profiler):

    # Metodo que se llama cada vez que se ejecuta una funcion
    @classmethod
    def record_start(cls, functionName, args):
        cls.getInstance().fun_call_start(functionName, args)

    @classmethod
    def record_end(cls, functionName, returnValue):
        cls.getInstance().fun_call_end(functionName, returnValue)
        return returnValue

    # Este metodo inyecta codigo en el programa segun el visitor del profiler
    @classmethod
    def instrument(cls, ast):
        visitor = FunctionInstrumentor()
        return fix_missing_locations(visitor.visit(ast))
    
    # Metodos de instancia
    def __init__(self):
        self.records = {}
        self.call_stack = []
        self.args_map = {}

    def get_record(self, functionName):
        if functionName not in self.records:
            self.records[functionName] = FunctionRecord(functionName)
        return self.records[functionName]

    def fun_call_start(self, functionName, args):
        if self.call_stack:
            caller = self.call_stack[-1]
            self.get_record(functionName).add_caller(caller)
        self.args_map[functionName] = args
        record = self.get_record(functionName)
        record.frequency += 1
        self.call_stack.append(functionName)
        
        

    def fun_call_end(self, functionName, returnValue):
        if self.call_stack and self.call_stack[-1] == functionName:
            self.call_stack.pop()
        record = self.get_record(functionName)
        args = self.args_map.pop(functionName, None)
        if args is not None:
            record.record_call(args, returnValue)
        return returnValue

    def print_fun_report(self):
        print("{:<30} {:<10} {:<10} {:<10}".format('fun', 'freq', 'cache', 'callers'))
        for record in self.records.values():
            record.print_report()
        
    def report_executed_functions(self):
        self.print_fun_report()
        return self.records

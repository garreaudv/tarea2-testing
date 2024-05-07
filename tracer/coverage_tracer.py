import sys
import ast
import inspect
from types import *
import traceback
from stack_inspector import StackInspector
from line_record import LineRecord

""" Clase para la Tarea 2. Para su uso, considere:
with CoverageTracer() as covTracer:
    function_to_be_traced()

covTracer.report_executed_lines()
"""

class CoverageTracer(StackInspector):

    def __init__(self):
        super().__init__(None, self.traceit)
        self.line_dict = {}
        # Completa el codigo necesario

    # Completa la funcion de rastreo
    def traceit(self, frame, event: str, arg):
        if event == "line":
            co = frame.f_code
            func_name = co.co_name
            line_no = frame.f_lineno
            key = (func_name, line_no)

            if key in self.line_dict:
                self.line_dict[key].increaseFrequency()
            else:
                self.line_dict[key] = LineRecord(func_name, line_no)
        return self.traceit



    def print_lines_report(self):
        for line_record in sorted(self.line_dict.values(), key=lambda x: x.lineNumber):
            line_record.print_report() if line_record.functionName not in ("<module>", '__exit__') else None



    def report_executed_lines(self):
        # Ordenar los registros por el número de línea de forma ascendente
        return sorted(self.line_dict.values(), key=lambda x: x.lineNumber)

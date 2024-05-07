import sys
import ast
import inspect
from types import *
import traceback
from stack_inspector import StackInspector

""" Clase para la Tarea 2. Para su uso, considere:
with CoverageTracer() as covTracer:
    function_to_be_traced()

covTracer.report_executed_lines()
"""

class CoverageTracer(StackInspector):

    def __init__(self):
        super().__init__(None, self.traceit)
        # Completa el codigo necesario

    # Completa la funcion de rastreo
    def traceit(self, frame, event: str, arg):
        pass

    def print_lines_report(self):
        print("{:<30} {:<10} {:<10}".format('fun', 'line', 'freq'))
        # Completa el codigo necesario

    def report_executed_lines(self):
        self.print_lines_report()
        # Completa el codigo necesario

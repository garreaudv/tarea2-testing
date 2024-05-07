import unittest
from function_instrumentor import *
from function_profiler import *

"""
Tests para el instrumentor profile de la Tarea 2
"""

class TestFunctionInstrumentor(unittest.TestCase):

    def print_expected_result(self, expected):
        print("============== Expected result ==============")
        print("{:<30} {:<10} {:<10} {:<10}".format('fun', 'freq', 'cache', 'callers'))
        for record in expected.values():
            record.print_report()


    """ Nombre: test_executed_functions1
        Codigo a ser analizado: input_code/code1.py
    """

    def test_executed_functions1(self):
        profiler = FunctionProfiler.profile("input_code/code1.py")
        result = profiler.getInstance().report_executed_functions()

        expected = {'main': FunctionRecord.new_instance_with('main', 1, True, []), 
                    'foo': FunctionRecord.new_instance_with('foo', 1, True, ['main']), 
                    'bar':FunctionRecord.new_instance_with('bar', 2, False, ['foo'])}

        #self.print_expected_result(expected)

        self.assertEqual(result, expected)

    """ Nombre: test_executed_functions2
        Codigo a ser analizado: input_code/code2.py
    """

    def test_executed_functions2(self):

        profiler = FunctionProfiler.profile("input_code/code2.py")
        result = profiler.getInstance().report_executed_functions()

        expected = {'factorial': FunctionRecord.new_instance_with('factorial', 6, False, ['factorial'])}

        #self.print_expected_result(expected)

        self.assertEqual(result, expected)


if __name__ == '__main__':
    unittest.main()

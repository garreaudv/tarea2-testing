import unittest
from ast import *
from coverage_tracer import *
from line_record import LineRecord

"""
Tests para el tracer de la Tarea2
"""

class TestCoverageTracer(unittest.TestCase):

    def print_expected_result(self, expected):
        print("============== Expected result ==============")
        print("{:<30} {:<10} {:<10}".format('fun', 'line', 'freq'))
        for record in expected:
            record.print_report()

    # Recibe un path del archivo a ser leido y retorna un AST en base al contenido del archivo
    def get_ast_from_file(self, filename):
        file = open(filename)
        fileContent = file.read()
        file.close()
        tree = parse(fileContent)

        return tree

    # Recibe el path del archivo a rastrear y lo ejecuta
    def execute_file(self, filename):
        tree = self.get_ast_from_file(filename)

        with CoverageTracer() as self.tracer:
            try:
                exec(compile(tree, filename="<ast>", mode ="exec"), locals(), locals())
            except:
                print("An error ocurred! The code to analyze cannot be executed")


    """ Nombre: test_executed_lines1
        Codigo a ser analizado: input_code/code1.py
    """

    def test_executed_lines1(self):

        self.execute_file("input_code/code1.py")

        result = self.tracer.report_executed_lines()

        expected = [LineRecord.new_instance_with('sum', 5, 2),
                    LineRecord.new_instance_with('test_sum', 12, 1), 
                    LineRecord.new_instance_with('test_sum_tuple', 14, 1)]

        #self.print_expected_result(expected)

        self.assertEqual(result, expected)

    """ Nombre: test_executed_lines2
        Codigo a ser analizado: input_code/code2.py
    """

    def test_executed_lines2(self):

        self.execute_file("input_code/code2.py")

        result = self.tracer.report_executed_lines()

        expected = [LineRecord.new_instance_with('factorial', 2, 1),
                    LineRecord.new_instance_with('factorial', 4, 1),
                    LineRecord.new_instance_with('factorial', 5, 4),
                    LineRecord.new_instance_with('factorial', 6, 3),
                    LineRecord.new_instance_with('factorial', 7, 3),
                    LineRecord.new_instance_with('factorial', 8, 1)]

        #self.print_expected_result(expected)

        self.assertEqual(result, expected)

if __name__ == '__main__':
    unittest.main()

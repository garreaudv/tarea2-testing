from coverage_tracer import *
import sys
from ast import *

# Recibe un path del archivo a ser leido y retorna un AST en base al contenido del archivo
def get_ast_from_file(filename):
    file = open(filename)
    fileContent = file.read()
    file.close()
    tree = parse(fileContent)

    return tree


if __name__ == '__main__':
    tree = get_ast_from_file("input_code/" + sys.argv[1] + ".py")

    with CoverageTracer() as tracer:
        try:
            exec(compile(tree, filename="<ast>", mode ="exec"), locals(), locals())
        except:
            print("An error ocurred! The code to analyze cannot be executed")

    tracer.print_lines_report()

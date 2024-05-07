from function_profiler import *
import sys

if __name__ == '__main__':
    profiler = FunctionProfiler.profile("input_code/" + sys.argv[1] + ".py")
    profiler.print_fun_report()

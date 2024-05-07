from ast import *
from functools import reduce

# Clase que permite inyectar codigo de tal forma que podamos reportar que funciones se ejecutan
class FunctionInstrumentor(NodeTransformer):

    def visit_Module(self, node: Module):
        transformedNode = NodeTransformer.generic_visit(self, node)

        # Inyectamos codigo para importar el profiler
        import_profile_injected = parse("from function_profiler import FunctionProfiler")
        transformedNode.body.insert(0, import_profile_injected.body[0])
        
        fix_missing_locations(transformedNode)

        return transformedNode


    def visit_FunctionDef(self, node: FunctionDef):
        transformedNode = NodeTransformer.generic_visit(self, node)
        
        # Inyectamos codigo en el cuerpo de la funcion
        # para recolectar informacion
        # de una funcion usando el profiler
        argList = list(map(lambda x: x.arg, transformedNode.args.args))

        argNames = list(map(lambda n: Name(id=n, ctx=Load()), argList))
        argNames = [Constant(value=transformedNode.name),
                    List(elts=argNames, ctx=Load())]

        before = Expr(value=Call(
                            func=Attribute(
                                value=Name(id='FunctionProfiler', ctx=Load()),
                                attr='record_start',
                                ctx=Load()),
                                args=argNames,
                                keywords=[]))       
        
        # Insert before statement
        transformedNode.body.insert(0, before)

        # Handle the return
        last_stmt = transformedNode.body[-1]

        if isinstance(last_stmt, Return):
            result_var = 'result'
            result_assignment = Assign(
                targets=[Name(id=result_var, ctx=Store())],
                value=last_stmt.value
            )

            after = Return(
                value=Call(
                    func=Attribute(
                        value=Name(id='FunctionProfiler', ctx=Load()),
                        attr='record_end',
                        ctx=Load()),
                    args=[Constant(value=transformedNode.name), Name(id=result_var, ctx=Load())],
                    keywords=[]
                )
            )

            transformedNode.body = transformedNode.body[:-1] + [result_assignment, after]
        else:
            after = Expr(value=Call(
                                func=Attribute(
                                    value=Name(id='FunctionProfiler', ctx=Load()),
                                    attr='record_end',
                                    ctx=Load()),
                                    args=[Constant(value=transformedNode.name), Constant(value=None)],
                                    keywords=[]))
            transformedNode.body.append(after)

        fix_missing_locations(transformedNode)

        return transformedNode

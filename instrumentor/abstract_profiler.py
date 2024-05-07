import threading
from ast import *

# Clase que representa la estructura de un profiler
class Profiler:
    __singleton_lock = threading.Lock()
    __singleton_instance = None

    # Usamos un singleton para no crear instancias a cada rato
    @classmethod
    def getInstance(cls):
        with cls.__singleton_lock:
            if not cls.__singleton_instance:
                cls.__singleton_instance = cls()
        return cls.__singleton_instance

    # Al resetear actualizamos la instancia de singleton a None
    @classmethod
    def reset(cls):
        cls.__singleton_instance = None

    @classmethod
    def record_start(cls, *other):
        pass

    @classmethod
    def record_end(cls, *other):
        pass

    # Recibe un archivo que contiene un programa Python
    # lo instrumenta y lo ejecuta recolectando datos en el profiler
    # devuelve el objeto profiler con los datos
    @classmethod
    def profile(cls, fileName):
        cls.reset()
        instance = cls.getInstance()
        ast = cls.get_ast_from_file(fileName)
        newAst = cls.instrument(ast)

        # Esta línea imprime el codigo modificado después de inyectarle líneas 
        # con el profiler pueden comentarla o descomentarla si quieren
        
        #print(unparse(newAst)) 
        try:
            exec(compile(newAst, filename="<ast>", mode ="exec"), locals(), locals())
        except:
            print("An error ocurred! My injected code may cause problems")

        return instance
    
    # Este metodo inyecta codigo en el programa segun el visitor del profiler
    @classmethod
    def instrument(cls, ast):
        visitor = NodeTransformer()
        return fix_missing_locations(visitor.visit(ast))
    
    # Recupera el AST dado un archivo
    @classmethod
    def get_ast_from_file(cls, fileName):
        file = open(fileName)
        fileContent = file.read()
        file.close()
        tree = parse(fileContent)
        return tree
    
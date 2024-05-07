from __future__ import print_function
import threading
from time import sleep
from sys import _current_frames

class CallNode:
    def __init__(self, name):
        self.name = name
        self.total_time = 0
        self.children = {}
        self.last_child = None  # Guarda el último hijo accedido para mantener el orden de llamada correcto

    def get_or_create_child(self, name):
        if name not in self.children:
            self.children[name] = CallNode(name)
        self.last_child = self.children[name]  # Actualiza el último hijo accedido
        return self.children[name]

    def increment_time(self):
        self.total_time += 1

    def print_tree(self, indent=0):
        indent_str = '    ' * indent
        print(f"{indent_str}{self.name} ({self.total_time} seconds)")
        if self.last_child:
            self.last_child.print_tree(indent + 1)
        for child in sorted(self.children.values(), key=lambda x: x.name):
            if child is not self.last_child:
                child.print_tree(indent + 1)

class Sampler:
    def __init__(self, tid):
        self.tid = tid
        self.root = CallNode("total")
        self.t = threading.Thread(target=self.sample)
        self.active = False
        self.lock = threading.Lock()

    def start(self):
        self.active = True
        self.t.start()

    def stop(self):
        self.active = False
        self.t.join()

    def sample(self):
        while self.active:
            sleep(1)  # Asume que la función se ejecuta cada segundo
            self.update_tree()

    def update_tree(self):
        frame = _current_frames().get(self.tid)
        if not frame:
            return
        
        current_node = self.root
        path = []
        current_stack = []
        
        while frame:
            current_stack.append(frame.f_code.co_name)
            frame = frame.f_back

        # Recorrido de la pila y actualización de los nodos
        with self.lock:
            current_node.increment_time()  # Aseguramos que se incrementa el tiempo del nodo raíz
            for name in reversed(current_stack):
                current_node = current_node.get_or_create_child(name)
                current_node.increment_time()  # Incrementa el tiempo de cada nodo en la ruta

    def print_report(self):
        self.root.print_tree()

























'''from __future__ import print_function
import threading
import time
from sys import _current_frames

class CallNode:
    def __init__(self, name):
        self.name = name
        self.total_time = 0.0
        self.children = {}

    def get_or_create_child(self, name):
        if name not in self.children:
            self.children[name] = CallNode(name)
        return self.children[name]

    def increment_time(self):
        self.total_time += 1

    def print_tree(self, indent=0):
        indent_str = '    ' * indent
        tiempo = int(self.total_time)
        if self.name in ("total", "run", "_bootstrap_inner", "_bootstrap", "execute_script"):
            tiempo += 1
        print(f"{indent_str}{self.name} ({tiempo} seconds)")
        for child in sorted(self.children.values(), key=lambda x: x.name):
            child.print_tree(indent + 1)

class Sampler:
    def __init__(self, tid):
        self.tid = tid
        self.root = CallNode("total")
        self.t = threading.Thread(target=self.sample)
        self.active = False
        self.lock = threading.Lock()

    def start(self):
        self.active = True
        self.t.start()

    def stop(self):
        self.active = False
        self.t.join()

    def sample(self):
        while self.active:
            time.sleep(1)  # Sample rate adjusted to 1 second
            self.update_tree()

    def update_tree(self):
        frame = _current_frames().get(self.tid)
        if not frame:
            return

        current_node = self.root
        with self.lock:
            current_node.increment_time()  # Ensure root node time is incremented
            path = [current_node]

            current_stack = []
            while frame:
                current_stack.append(frame.f_code.co_name)
                frame = frame.f_back

            for name in reversed(current_stack):
                current_node = current_node.get_or_create_child(name)
                path.append(current_node)
                current_node.increment_time()  # Increment time for each node in the path

    def print_report(self):
        self.root.print_tree()
'''
from __future__ import print_function
import threading
import time
from sys import _current_frames

class CallNode:
    def __init__(self, name):
        self.name = name
        self.total_time = 0.0
        self.children = {}
        self.last_active_time = None

    def activate(self, timestamp):
        if self.last_active_time is None:
            self.last_active_time = timestamp

    def deactivate(self, timestamp):
        if self.last_active_time is not None:
            elapsed_time = timestamp - self.last_active_time
            self.total_time += elapsed_time
            self.last_active_time = None
            return elapsed_time
        return 0

    def get_or_create_child(self, name):
        if name not in self.children:
            self.children[name] = CallNode(name)
        return self.children[name]

    def print_tree(self, indent=0):
        # Asegurarse de que el tiempo se muestre correctamente como un entero redondeado
        rounded_time = int(round(self.total_time))
        indent_str = '    ' * indent
        print(f"{indent_str}{self.name} ({rounded_time} seconds)")
        for child in sorted(self.children.values(), key=lambda x: x.name):
            child.print_tree(indent + 1)

class Sampler:
    def __init__(self, tid):
        self.tid = tid
        self.root = CallNode("total")
        self.current_nodes = [self.root]
        self.t = threading.Thread(target=self.sample)
        self.active = False

    def start(self):
        self.active = True
        self.root.activate(time.time())
        self.t.start()

    def stop(self):
        self.active = False
        self.t.join()
        self.cleanup_times()

    def sample(self):
        while self.active:
            time.sleep(0.1)  # Sample rate
            current_time = time.time()
            frame = _current_frames().get(self.tid)
            if not frame:
                continue

            current_stack = []
            while frame:
                current_stack.append(frame.f_code.co_name)
                frame = frame.f_back

            self.update_tree(current_stack, current_time)

    def update_tree(self, stack, current_time):
        current_node = self.root
        path = [current_node]
        for name in reversed(stack):
            current_node = current_node.get_or_create_child(name)
            path.append(current_node)

        # Activate nodes in current path
        for node in path:
            node.activate(current_time)

        # Deactivate nodes not in current path
        extra_time = 0
        for node in reversed(self.current_nodes):
            if node not in path:
                extra_time += node.deactivate(current_time)

        self.current_nodes = path

    def cleanup_times(self):
        current_time = time.time()
        for node in reversed(self.current_nodes):
            node.deactivate(current_time)

    def print_report(self):
        self.root.print_tree()

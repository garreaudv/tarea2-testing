from __future__ import print_function
import threading
from time import sleep
import traceback
from sys import _current_frames
from collections import defaultdict

class Sampler:
    def __init__(self, tid) -> None:
        self.tid = tid
        self.t = threading.Thread(target=self.sample, args=())
        self.active = True
        self.samples = []
        
        
    def start(self):
        self.active = True
        self.t.start()

    def stop(self):
        self.active = False
        self.t.join()
        
    def checkTrace(self):
        for thread_id, frames in _current_frames().items():
            if thread_id == self.tid:
                frames = traceback.walk_stack(frames)
                stack = []
                for frame, _ in frames: 
                    code = frame.f_code.co_name
                    stack.append(code)
                stack.reverse()
                self.samples.append(tuple(stack))  # Esta linea imprime el stack despues de invertirlo la pueden comentar o descomentar si quieren
    
    def sample(self):
        while self.active:
            self.checkTrace()
            sleep(1)

    def print_report(self):
        print("Stack samples:")
        for sample in self.samples:
            print(sample)
        print("End of stack samples")
        print("Stack samples count:")
        stack_count = defaultdict(int)
        for sample in self.samples:
            stack_count[sample] += 1
        for stack, count in stack_count.items():
            print(f"{stack}: {count}")
        print("End of stack samples count")
        print("Stack samples count sorted:")
        for stack, count in sorted(stack_count.items(), key=lambda x: x[1], reverse=True):
            print(f"{stack}: {count}")
        print("End of stack samples count sorted")
        print("End of report")

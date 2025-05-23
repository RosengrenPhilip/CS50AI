import sys
from typing import override

class Node():
    def __init__(self, state, parent, action):
        self.state = state
        self.parent = parent
        self.action = action

    
class StackFrontier():

    def __init__(self):
            self.frontier = []

    def add(self, node: Node) -> None:
            self.frontier.append(node)
    
    def contains_state(self, state) -> bool:
        return any(node.state == state for node in self.frontier) #Assumes that the frontier contains nodes as defined above
    
    def empty(self) -> bool:
        return len(self.frontier) == 0
    
    def remove(self) -> Node:
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[-1]
            return node
        
class QueueFrontier(StackFrontier):
    
    @override
    def remove(self): 
        if self.empty():
            raise Exception("empty frontier")
        else:
            node = self.frontier[0]
            self.frontier = self.frontier[1:]
            return node

class Maze():
     pass

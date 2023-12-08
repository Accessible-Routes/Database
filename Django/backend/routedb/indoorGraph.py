class indoorGraph():
      def __init__(self, name) -> None:
            self.name = name
            self.adjList = dict()
      def addNode(self, node):
            self.adjList[node.name] = []

      def addEdge(self, node, edge):
            if node in self.adjList.keys():
                  self.adjList[node.name].append(edge)
            else:
                  return False
      def printGraph(self):
            for key in self.adjList.keys():
                  print(key + " : " + self.adjList[key])
      
class Node():
      def __init__(self, id, name) -> None:
            self.id = id
            self.name = name
            self.degree = 0
class Edge():
      def __init__(self, id, start, end, weight) -> None:
            self.id = id
            self.start = start
            self.end = end
            self.weight = weight


if __name__ == "__main__":
      i = indoorGraph("Test")
      n = Node(0, "Name")
      i.addNode(n)
      i.printGraph()
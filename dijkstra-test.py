from dijkstra import dijkstra, Vertex, Edge, Graph

graph = Graph()
v = [Vertex(i) for i in range(9)]
graph.add(Edge(v[0], v[2], 26))
graph.add(Edge(v[0], v[4], 38))
graph.add(Edge(v[1], v[3], 29))
graph.add(Edge(v[2], v[7], 34))
graph.add(Edge(v[3], v[6], 52))
graph.add(Edge(v[4], v[5], 35))
graph.add(Edge(v[4], v[7], 37))
graph.add(Edge(v[5], v[1], 32))
graph.add(Edge(v[5], v[4], 35))
graph.add(Edge(v[5], v[7], 28))
graph.add(Edge(v[6], v[0], 58))
graph.add(Edge(v[6], v[2], 40))
graph.add(Edge(v[6], v[4], 93))
graph.add(Edge(v[7], v[3], 39))
graph.add(Edge(v[7], v[5], 28))
graph.add(Edge(v[7], v[8], 10))
graph.start = v[0]
graph.end = v[6]
graph.make_undirected(lambda w: w)

path = dijkstra(graph)

print(path.distance)
print(path.path)

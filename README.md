# Dijkstroute
An implementation of Dijkstra's algorithm to find a route from the start point to the end point of a maze, or the shortest such route if multiple exist.

## Dijkstra's algorithm and required classes
`dijkstra.py` contains the Dijkstra's algorithm function and the classes required for it (`Vertex`, `Edge`, `Graph`, `PriorityQueue`). These classes have some useful methods that aren't used in this project that may be useful for a different project (e.g. the `Graph.make_undirected()` method that turns a directed graph into an undirected one by reversing all edges, taking as an optional argument a lambda to modify weights of each edge when reversing). A test of this is in `dijkstra-test.py`.

## ASCII Maze route finder
The ASCII Maze route finder uses Dijkstra's algorithm to find a route from the start to the end of an ASCII maze, and to find the shortest such route if multiple exist.

`asciimaze.py` takes either one or two command line arguments. The first is a path to the input maze file, and the second (optional) one is a path to the output (solved) maze file. The input maze file uses `#` for walls, `O` for the start position, `X` for the end position, and a space character for empty space. The solved maze file uses the same characters, with the addition of the `+` character for the route. The solved maze is saved to the output file if one is provided, or printed to stdout if not. If a route doesn't exist, this is logged to stdout.

See `maze.txt` and `solved_maze.txt` for an example.
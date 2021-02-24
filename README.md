# Dijkstroute

## Dijkstra's algorithm and required classes
`dijkstra.py` contains the Dijkstra's algorithm function and the classes required for it.

## ASCII Maze solver
The ASCII Maze solver uses Dijkstra's algorithm to find a path from the start to the end of an ASCII maze, and to find the shortest such path if multiple exist.

`asciimaze.py` takes either one or two command line arguments. The first is a path to the input maze file, and the second (optional) one is a path to the output (solved) maze file. The input maze file uses `#` for walls, `O` for the start position, `X` for the end position, and a space character for empty space. The solved maze file uses the same characters, with the addition of the `+` character for the path. The solved maze is saved to the output file if one is provided, or printed to stdout if not. If a path doesn't exist, this is logged to stdout.

See `maze.txt` and `solved_maze.txt` for an example.
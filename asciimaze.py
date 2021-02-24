import sys
from enum import Enum
from dijkstra import NoPathExistsError, Vertex, Graph, Edge, dijkstra

script, infile, *outfile = sys.argv


class Tile(Enum):
    WALL = 0
    EMPTY = 1
    START = 2
    END = 3
    PATH = 4
    FILLED = 5  # Wall that was added by program (didn't exist in input)


class Direction(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3


class Maze:
    def __init__(self, maze):
        self.maze = maze
        self._fix_widths()

    @property
    def height(self):
        return len(self.maze)

    @property
    def width(self):
        return len(self.maze[0])

    def _fix_widths(self):
        # Make every row the same length
        width = self.width
        need_to_fix = False
        for row in self.maze:
            if len(row) > width:
                width = len(row)
                need_to_fix = True
            elif len(row) < width:
                need_to_fix = True

        if need_to_fix:
            for row in self.maze:
                difference = width - len(row)
                for _ in range(difference):
                    row.append(Tile.FILLED)

    def left(self, x, y):
        # Returns if tile at (x, y) has an empty left neighbour
        if x == 0:
            return False
        return self.maze[y][x-1] not in [Tile.WALL, Tile.FILLED]

    def right(self, x, y):
        # Returns if tile at (x, y) has an empty right neighbour
        if x == self.width - 1:
            return False
        return self.maze[y][x+1] not in [Tile.WALL, Tile.FILLED]

    def top(self, x, y):
        # Returns if tile at (x, y) has an empty top neighbour
        if y == 0:
            return False
        return self.maze[y-1][x] not in [Tile.WALL, Tile.FILLED]

    def bottom(self, x, y):
        # Returns if tile at (x, y) has an empty bottom neighbour
        if y == self.height - 1:
            return False
        return self.maze[y+1][x] not in [Tile.WALL, Tile.FILLED]

    def neighbour(self, direction, x, y):
        # Generalisation if left, right, top, bottom functions
        if direction == Direction.LEFT:
            return self.left(x, y)
        elif direction == Direction.RIGHT:
            return self.right(x, y)
        elif direction == Direction.UP:
            return self.top(x, y)
        elif direction == Direction.DOWN:
            return self.bottom(x, y)

    def neighbours(self, x, y):
        # Returns list of empty neighbours of tile at (x, y)
        neighbours = []
        for direction in Direction:
            if self.neighbour(direction, x, y):
                neighbours.append(direction)
        return neighbours

    def get(self, x, y):
        return self.maze[y][x]

    def put(self, x, y, square):
        self.maze[y][x] = square


class Fork(Vertex):
    def __init__(self, label):
        super().__init__(label)
        self.neighbours = []


class Route(Edge):
    def __init__(self, v1, v2, weight, direction):
        super().__init__(v1, v2, weight)
        self.direction = direction


with open(infile, 'r') as f:
    fc = f.read()
    if fc.count('O') == 0:
        sys.exit('No start tile (O) set in the maze.')
    if fc.count('O') > 1:
        sys.exit('Too many start tiles (O) set in the maze.')
    if fc.count('X') == 0:
        sys.exit('No end tile (X) set in the maze.')
    if fc.count('X') > 1:
        sys.exit('Too many end tiles (X) set in the maze.')
    lines = fc.split('\n')
    # Read string into 2d list
    translation = {
        ' ': Tile.EMPTY,
        '#': Tile.WALL,
        'O': Tile.START,
        'X': Tile.END
    }
    try:
        maze = Maze([[translation[char] for char in line] for line in lines])
    except KeyError as e:
        sys.exit('Invalid character in maze: ' + e.args[0])

graph = Graph()

# Find forks in the path (i.e. tiles with a choice of which direction to go,
# i.e. more than two neighbours) and start and end points and make them
# vertices in the graph.
for y, row in enumerate(maze.maze):
    for x, square in enumerate(row):
        f = Fork((x, y))
        create_fork = False
        neighbours = maze.neighbours(x, y)
        if square == Tile.START:
            graph.start = f
            create_fork = True
        elif square == Tile.END:
            graph.end = f
            create_fork = True
        elif square in [Tile.WALL, Tile.FILLED]:
            continue
        elif len(neighbours) < 3:
            continue
        f.neighbours = neighbours
        graph.add(f)

# Find lengths of edges between vertices, i.e. lengths of paths between two
# forks, and add the edges to the graph
for fork in graph.vertices:
    x, y = fork.label
    for direction in fork.neighbours:
        x_to, y_to = x, y
        last_direction = direction
        distance = 0
        dead_end = False
        if direction == Direction.LEFT:
            x_to -= 1
        elif direction == Direction.RIGHT:
            x_to += 1
        elif direction == Direction.UP:
            y_to -= 1
        elif direction == Direction.DOWN:
            y_to += 1
        while not graph.has_vertex((x_to, y_to)) and not dead_end:
            # While we haven't hit another fork or a dead end, keep going down
            # the path
            if maze.left(x_to, y_to) and last_direction != Direction.RIGHT:
                x_to -= 1
                last_direction = Direction.LEFT
            elif maze.right(x_to, y_to) and last_direction != Direction.LEFT:
                x_to += 1
                last_direction = Direction.RIGHT
            elif maze.top(x_to, y_to) and last_direction != Direction.DOWN:
                y_to -= 1
                last_direction = Direction.UP
            elif maze.bottom(x_to, y_to) and last_direction != Direction.UP:
                y_to += 1
                last_direction = Direction.DOWN
            elif len(maze.neighbours(x_to, y_to)) == 1:
                dead_end = True
            else:
                raise Exception()
            distance += 1
        if dead_end:
            continue
        fork2 = graph.get_vertex((x_to, y_to))
        if fork == fork2:
            continue
        graph.add(Route(fork, fork2, distance + 1, direction))

try:
    path = dijkstra(graph)  # Run Dijkstra's algorithm on the graph
except NoPathExistsError:
    sys.exit('No path from the start to the end exists in this maze.')

for i in range(len(path.vertices) - 1):
    # For each pair of consecutive vertices, set the tiles to PATH tiles in the
    # maze using a similar method to the process of adding edges above
    vertex = path.vertices[i]
    vertex2 = path.vertices[i+1]
    route = graph.get_edge(vertex, vertex2)
    x, y = vertex.label
    x2, y2 = vertex2.label
    direction = route.direction
    # Go in the direction stated by the edge
    if direction == Direction.LEFT:
        x -= 1
    elif direction == Direction.RIGHT:
        x += 1
    elif direction == Direction.UP:
        y -= 1
    elif direction == Direction.DOWN:
        y += 1
    else:
        raise Exception()
    last_direction = direction
    while (x, y) != (x2, y2):
        # Keep going down the path until we reach the next vertex, setting each
        # tile to a PATH tile
        maze.put(x, y, Tile.PATH)
        if maze.left(x, y) and last_direction != Direction.RIGHT:
            x -= 1
            last_direction = Direction.LEFT
        elif maze.right(x, y) and last_direction != Direction.LEFT:
            x += 1
            last_direction = Direction.RIGHT
        elif maze.top(x, y) and last_direction != Direction.DOWN:
            y -= 1
            last_direction = Direction.UP
        elif maze.bottom(x, y) and last_direction != Direction.UP:
            y += 1
            last_direction = Direction.DOWN
        else:
            raise Exception()
    if i != len(path.vertices) - 2:
        # Set the final tile to a PATH tile, unless it is the end vertex as
        # this will need to keep the end marker. We don't need to do this check
        # for the start vertex as the first vertex of any route is never set
        maze.put(x, y, Tile.PATH)

outp = ''
translation = {
    Tile.EMPTY: ' ',
    Tile.WALL: '#',
    Tile.FILLED: '',
    Tile.START: 'O',
    Tile.END: 'X',
    Tile.PATH: '+'
}
for row in maze.maze:
    for square in row:
        outp += translation[square]
    outp += '\n'

if len(outfile) > 0:
    with open(outfile[0], 'w') as f:
        f.write(outp)

else:
    print(outp)

from days import AOCDay, day

import math
from collections import defaultdict


def borders(data):
    top = data[0]
    right = ''.join(line[-1] for line in data)
    bottom = data[-1]
    left = ''.join(line[0] for line in data)
    return (top, right, bottom, left)


def mirrors(data):
    mirrors = [data]
    mirrors.append(data[::-1])
    mirrors.append([row[::-1] for row in data])
    mirrors.append([row[::-1] for row in data][::-1])
    return mirrors


def rotations(data):
    rotations = [data]
    cur = data
    for _ in range(3):
        data = [line[:] for line in data]
        for x in range(len(data)):
            for y in range(len(data[x])):
                data[x][y] = cur[len(data[x]) - y - 1][x]
        cur = data
        rotations.append(data)
    return rotations


def all_options(data):
    options = []
    for mirror in mirrors(data):
        options.extend(rotations(mirror))
    # Remove duplicates
    result = []
    for option in options:
        if option not in result:
            result.append(option)
    return result


@day(20)
class Day20(AOCDay):
    print_debug = "c12"
    test_input = """Tile 2311:
..##.#..#.
##..#.....
#...##..#.
####.#...#
##.##.###.
##...#.###
.#.#.#..##
..#....#..
###...#.#.
..###..###

Tile 1951:
#.##...##.
#.####...#
.....#..##
#...######
.##.#....#
.###.#####
###.##.##.
.###....#.
..#.#..#.#
#...##.#..

Tile 1171:
####...##.
#..##.#..#
##.#..#.#.
.###.####.
..###.####
.##....##.
.#...####.
#.##.####.
####..#...
.....##...

Tile 1427:
###.##.#..
.#..#.##..
.#.##.#..#
#.#.#.##.#
....#...##
...##..##.
...#.#####
.#.####.#.
..#..###.#
..##.#..#.

Tile 1489:
##.#.#....
..##...#..
.##..##...
..#...#...
#####...#.
#..#.#.#.#
...#.#.#..
##.#...##.
..##.##.##
###.##.#..

Tile 2473:
#....####.
#..#.##...
#.##..#...
######.#.#
.#...#.#.#
.#########
.###.#..#.
########.#
##...##.#.
..###.#.#.

Tile 2971:
..#.#....#
#...###...
#.#.###...
##.##..#..
.#####..##
.#..####.#
#..#.#..#.
..####.###
..#.#.###.
...#.#.#.#

Tile 2729:
...#.#.#.#
####.#....
..#.#.....
....#..#.#
.##..##.#.
.#.####...
####.#.#..
##.####...
##..#.##..
#.##...##.

Tile 3079:
#.#.#####.
.#..######
..#.......
######....
####.#..#.
.#...#.##.
#.#####.##
..#.###...
..#.......
..#.###...""".split("\n")

    MONSTER_PATTERN = '''                  # 
#    ##    ##    ###
 #  #  #  #  #  #   '''.split("\n")

    tiles = {}
    grid = {}

    def common(self, input_data):
        input_data = "\n".join(input_data).split("\n\n")
        self.tiles = {}
        self.grid = {}
        for tile in input_data:
            tile = tile.split("\n")
            tile_id = int(tile[0].split(" ")[1].replace(":", ""))
            self.tiles[tile_id] = [list(l) for l in tile[1:]]

    def generate_tiling(self, tile_map):
        puzzle_size = math.isqrt(len(tile_map))
        tiles = [[None for _ in range(puzzle_size)] for _ in range(puzzle_size)]

        def generate_tiling_recurse(tiles, x, y, seen):
            if y == puzzle_size:
                return tiles

            next_x, next_y = x + 1, y
            if next_x == puzzle_size:
                next_x, next_y = 0, next_y + 1

            for tile_id, options in tile_map.items():
                if tile_id in seen:
                    continue

                seen.add(tile_id)

                for index, borders in options.items():
                    top, left = borders[0], borders[3]
                    if x > 0:
                        neighbour_id, neighbour_orientation = tiles[x - 1][y]
                        neighbour_right = tile_map[neighbour_id][neighbour_orientation][1]
                        if neighbour_right != left:
                            continue
                    if y > 0:
                        neighbour_id, neighbour_orientation = tiles[x][y - 1]
                        neighbour_bottom = tile_map[neighbour_id][neighbour_orientation][2]
                        if neighbour_bottom != top:
                            continue
                    tiles[x][y] = (tile_id, index)
                    answer = generate_tiling_recurse(tiles, next_x, next_y, seen)
                    if answer is not None:
                        return answer
                seen.remove(tile_id)
            tiles[x][y] = None
            return None

        return generate_tiling_recurse(tiles, 0, 0, set())

    def part1(self, input_data):
        tile_options = {tile_id: all_options(tile) for tile_id, tile in self.tiles.items()}
        tile_map = defaultdict(dict)
        for tile_id, options in tile_options.items():
            for index, tile in enumerate(options):
                tile_map[tile_id][index] = borders(tile)
        tiling = self.generate_tiling(tile_map)
        corners = [tiling[0][0], tiling[0][-1], tiling[-1][0], tiling[-1][-1]]
        answer = 1
        for c, _ in corners:
            answer *= c
        yield answer

    def make_image(self, tile_options, tiling):
        result = []
        for row in tiling:
            grids = []
            for tile_id, orientation in row:
                grid = tile_options[tile_id][orientation]
                # Remove borders
                grid = [line[1:-1] for line in grid[1: -1]]
                grids.append(grid)

            for y in range(len(grids[0][0])):
                res_row = []
                for i in range(len(grids)):
                    res_row.extend(grids[i][x][y] for x in range(len(grids[i])))
                result.append("".join(res_row))
        return result

    def find_monsters(self, image):
        monster_locs = []
        max_x, max_y = 0, 0
        for dy, line in enumerate(self.MONSTER_PATTERN):
            for dx, c in enumerate(line):
                if c == "#":
                    monster_locs.append((dx, dy))
                    max_x, max_y = max(dx, max_x), max((dy, max_y))

        monster_tiles = set()
        for y in range(len(image)):
            if y + max_y >= len(image):
                break
            for x in range(len(image[y])):
                if x + max_x >= len(image[y]):
                    break
                has_monster = True
                for dx, dy in monster_locs:
                    if image[y + dy][x + dx] != "#":
                        has_monster = False
                        break
                if has_monster:
                    for dx, dy in monster_locs:
                        monster_tiles.add((x + dx, y + dy))
        if len(monster_tiles) == 0:
            return None

        all_squares = set()
        for y, line in enumerate(image):
            for x, c in enumerate(line):
                if c == "#":
                    all_squares.add((x, y))
        return len(all_squares - monster_tiles)

    def part2(self, input_data):
        tile_options = {tile_id: all_options(tile) for tile_id, tile in self.tiles.items()}
        tile_map = defaultdict(dict)
        for tile_id, options in tile_options.items():
            for index, tile in enumerate(options):
                tile_map[tile_id][index] = borders(tile)
        tiling = self.generate_tiling(tile_map)

        image = self.make_image(tile_options, tiling)
        image_options = all_options([list(line) for line in image])

        answer = None
        for opt in image_options:
            answer = self.find_monsters(opt)
            if answer is not None:
                break
        yield answer

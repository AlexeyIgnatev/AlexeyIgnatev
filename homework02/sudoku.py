import pathlib
import random
import typing as tp

T = tp.TypeVar("T")


def read_sudoku(path: tp.Union[str, pathlib.Path]) -> tp.List[tp.List[str]]:
    path = pathlib.Path(path)
    with path.open() as f:
        puzzle = f.read()
    return create_grid(puzzle)


def create_grid(puzzle: str) -> tp.List[tp.List[str]]:
    digits = [c for c in puzzle if c in "123456789."]
    grid = group(digits, 9)
    return grid


def display(grid: tp.List[tp.List[str]]) -> None:
    width = 2
    line = "+".join(["-" * (width * 3)] * 3)
    for row in range(9):
        print(
            "".join(
                grid[row][col].center(width) + ("|" if str(col) in "25" else "") for col in range(9)
            )
        )
        if str(row) in "25":
            print(line)
    print()


def group(values: tp.List[T], n: int) -> tp.List[tp.List[T]]:
    return [values[i - n : i] for i in range(n, len(values) + 1, n)]


def get_row(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return grid[pos[0]]


def get_col(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    return [i[pos[1]] for i in grid]


def get_block(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.List[str]:
    top = pos[0] - pos[0] % 3
    left = pos[1] - pos[1] % 3

    rows = [get_row(grid, (i, 0)) for i in range(top, top + 3)]
    cols = [get_col(rows, (0, i)) for i in range(left, left + 3)]

    res = []
    for i in range(3):
        res.append(cols[0][i])
        res.append(cols[1][i])
        res.append(cols[2][i])

    return res


def find_empty_positions(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.Tuple[int, int]]:
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == ".":
                return i, j
    return -1, -1


def find_possible_values(grid: tp.List[tp.List[str]], pos: tp.Tuple[int, int]) -> tp.Set[str]:
    row = get_row(grid, pos)
    col = get_col(grid, pos)
    block = get_block(grid, pos)

    a = set("123456789.")
    b = set()
    for i in row:
        b.add(i)
    for i in col:
        b.add(i)
    for i in block:
        b.add(i)

    a -= b
    return a


def solve(grid: tp.List[tp.List[str]]) -> tp.Optional[tp.List[tp.List[str]]]:
    p = find_empty_positions(grid)
    if p[0] == -1 and p[1] == -1:
        return grid

    values = list(find_possible_values(grid, p))
    if len(values) == 0:
        return None
    random.shuffle(values)

    for v in values:
        grid[p[0]][p[1]] = v
        res = solve(grid)

        if res:
            return res

    grid[p[0]][p[1]] = "."
    return None


def check_solution(solution: tp.List[tp.List[str]]) -> bool:
    for i in range(len(solution)):
        for j in range(len(solution[i])):
            p = (i, j)
            col = get_col(solution, p)
            row = get_row(solution, p)
            block = get_block(solution, p)
            if not (
                len(set(col)) == len(set(row)) == len(set(block)) == len(solution)
                and "." not in col
                and "." not in row
                and "." not in block
            ):
                return False
    return True


def generate_sudoku(N: int) -> tp.List[tp.List[str]]:
    grid = [["."] * 9 for i in range(9)]
    solve(grid)

    pos = [(i, j) for i in range(9) for j in range(9)]
    random.shuffle(pos)

    N = 81 - N
    for i in range(N):
        p = pos[i]
        grid[p[0]][p[1]] = "."

    return grid


if __name__ == "__main__":
    for fname in ["puzzle1.txt", "puzzle2.txt", "puzzle3.txt"]:
        grid = read_sudoku(fname)
        display(grid)
        solution = solve(grid)
        if not solution:
            print(f"Puzzle {fname} can't be solved")
        else:
            display(solution)

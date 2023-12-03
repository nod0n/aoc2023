#!/usr/bin/env python
from typing import Iterable

# red, green, blue cubes
# each game: secret number of cubes hidden in bag
# each round in game: handful of randomly selected cubes shown from bag
# goal: indentify possible games with limits of cubes in bag:
# red <= 12, green <= 13, blue <= 14
# (check each round if it was possible to show that amount of cubes per color)

type Max = tuple[int, int, int]
type SplitRound = list[list[str]]
type Round = dict[str, int]
type Game = tuple[Round, ...]
type GameID = int
type Line = tuple[GameID, Game]
type SetOfCubes = dict[str, int]


def split_round(round_: str) -> SplitRound:
    return [cube.strip().split(" ") for cube in round_.split(",")]


def parse_round(round_: str) -> Round:
    return {color: int(n) for n, color in split_round(round_)}


def parse_game(game: str) -> Game:
    return [parse_round(round_) for round_ in game.split(";")]


def parse_line(line: str) -> Line:
    split_line = line.split(":")
    return int(split_line[0].split(" ")[1]), parse_game(split_line[1])


def parse_file(file: Iterable) -> map:
    return map(parse_line, file)


def check_round(round_: Round, max_: Max = (12, 13, 14)) -> bool:
    max__ = {"red": max_[0], "green": max_[1], "blue": max_[2]}
    return 0 == sum(n > max__[color] for color, n in round_.items())


def check_game(game: Game) -> bool:
    return 0 == sum(not check_round(round_) for round_ in game)


def power_of_set_of_cubes(game: Game) -> SetOfCubes:
    cubes = {"red": [], "green": [], "blue": []}
    for round_ in game:
        for color, n in round_.items():
            cubes[color].append(n)
    set_of_cubes = {color: max(n) for color, n in cubes.items()}
    power_of_set_of_cubes_ = 1
    for n in set_of_cubes.values():
        power_of_set_of_cubes_ *= n
    return power_of_set_of_cubes_


def sum_file(file: str) -> int:
    with open(file) as f:
        return sum(i for i, game in parse_file(f) if check_game(game))


def sum_file2(file: str) -> int:
    with open(file) as f:
        return sum(power_of_set_of_cubes(game) for _, game in parse_file(f))


def test_parse_round() -> bool:
    round_: str = "50 green, 3 blue, 4 red"
    correct: Round = {"green": 50, "blue": 3, "red": 4}
    return parse_round(round_) == correct


def test_parse_game():
    game: str = "3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    correct: Game = [
        {"blue": 3, "red": 4},
        {"red": 1, "green": 2, "blue": 6},
        {"green": 2},
    ]
    return parse_game(game) == correct


def test_parse_line():
    line = "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    correct: Line = 1, [
        {"blue": 3, "red": 4},
        {"red": 1, "green": 2, "blue": 6},
        {"green": 2},
    ]
    return correct == parse_line(line)


def test_check_round():
    round1 = "15 blue, 12 red, 13 green"
    round2 = "13 green, 14 blue, 12 red"
    return not check_round(parse_round(round1)) and check_round(
        parse_round(round2)
    )


def test_check_game():
    game1 = "15 blue, 12 red, 13 green; 13 green, 14 blue, 12 red"
    game2 = "14 blue, 12 red, 13 green; 13 green, 14 blue, 12 red"
    return not check_game(parse_game(game1)) and check_game(parse_game(game2))


def main(test: bool = False):
    if test:
        print(f"parse round: {test_parse_round()}")
        print(f"parse game: {test_parse_game()}")
        print(f"parse line: {test_parse_line()}")
        print(f"check round: {test_check_round()}")
        print(f"check game: {test_check_game()}")
    print(f"sum of ids: {sum_file('2a_input')}")
    print(f"sum of powers of sets of cubes: {sum_file2('2b_input')}")


if __name__ == "__main__":
    main(True)

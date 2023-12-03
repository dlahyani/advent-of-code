from math import prod


LIMITS = {"red": 12, "green": 13, "blue": 14}

TITLE_PREFIX = "Game "


def parse_drawing(drawing: str) -> tuple[str, int]:
    number, color = drawing.strip().split(" ")
    return (color, int(number))


def parse_round(round: str) -> dict[str, int]:
    drawings: list[tuple[str, int]] = [parse_drawing(d) for d in round.split(",")]
    return {color: number for color, number in drawings}


def parse_game(game: str) -> list[dict[str, int]]:
    rounds: list[str] = game.split(";")
    return [parse_round(r) for r in rounds]


def is_round_possible(round: dict[str, int]) -> bool:
    return all(number <= LIMITS[color] for color, number in round.items())


def is_game_possible(game: list[dict[str, int]]) -> bool:
    return all(is_round_possible(round) for round in game)


def min_set_required_for_game(game: list[dict[str, int]]) -> dict[str, int]:
    reds = [r.get("red", 0) for r in game]
    greens = [r.get("green", 0) for r in game]
    blues = [r.get("blue", 0) for r in game]

    return {"red": max(reds), "green": max(greens), "blue": max(blues)}


def game_power(game: list[dict[str, int]]) -> int:
    min_set = min_set_required_for_game(game)
    return prod(min_set.values())


with open("2023/02/input.txt", "r") as f:
    valid_games = []
    games_powers = []
    for l in f:
        title, game_content = l.split(":")
        game_id = int(title[len(TITLE_PREFIX) :])
        game = parse_game(game_content)
        if is_game_possible(game):
            valid_games.append(game_id)

        games_powers.append(game_power(game))

    s = sum(valid_games)
    print(s)

    s = sum(games_powers)
    print(s)

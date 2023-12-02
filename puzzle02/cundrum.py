import numpy as np


def load_games(game_strings: list[str]) -> list[tuple[int, dict[list]]]:
    """
    Converts each game string into a tuple of its game index and a dictionary that contains
    the colors as keys and a list of the amount of draws per set in that game as values.
    e.g (1, {'red': [5, 10, 15, 6, 4, 5], 'green': [4, 4, 5, 3], 'blue': [7, 7, 5, 7, 8, 4]})
    Returns a list of these tuples

    :param game_strings: contains all game strings read from the input file
    """

    all_games = []
    for line in game_strings:
        # split game string into its idx and a list of game set strings
        game_idx, game_sets = line.strip().split(":")
        game_idx = int(game_idx.split(" ")[1])
        game_sets = game_sets.split(";")

        # game sets is now a list of strings like [' 1 red,4 blue,2 green', ' 6 red,2 green,11 blue',' 1 red, 7 blue']
        # now we want to convert it to a dict like {'red': [1, 6, 1], 'green': [2, 2], 'blue': [4, 11, 7]}
        game_set_dict = {"red": [], "green": [], "blue": []}
        for set_string in game_sets: 
            # split ' 1 red, 4 blue, 2 green' into [' 1 red', ' 4 blue', ' 2 green']
            color_split = set_string.split(",")
            # extract int and color from each string and append to dict of that game
            for color_string in color_split:
                amount, color = color_string.strip().split(" ")
                game_set_dict[color].append(int(amount))
                
        all_games.append((game_idx, game_set_dict))

    return all_games


def sum_possible_games_with_replacement(games: list[tuple[int, list[dict]]], available_cubes: dict) -> int:
    """
    Checks if a game is possible for each game and returns the sum of the indices of all possible games

    :param games: list of tuples of game indices and a dictionary that contains
                  the colors as keys and a list of the amount of draws per set in that game as values
    :param available_cubes: contains the amount of cubes available per color
    """

    sum = 0
    for game_idx, game in games:
        is_game_possible = True
        for color in game.keys():
            if np.any(np.array(game[color]) > available_cubes[color]):
                is_game_possible = False
                break

        if is_game_possible:
            sum += game_idx

    return sum

def sum_min_needed_cubes(games: list[tuple[int, list[dict]]]) -> int:

    sum = 0

    for _, game in games:
        min_needed = {"red": 0, "green": 0, "blue": 0}
        for drawn_color in game.keys():
            min_needed[drawn_color] = np.max(game[drawn_color])

        sum += np.prod(list(min_needed.values()))

    return sum

if __name__ == "__main__":
    available_cubes = {"red": 12, "green": 13, "blue": 14}
    with open("input.txt") as fp:
        game_strings = fp.readlines()
        games = load_games(game_strings)
        sum_possible_games_idx = sum_possible_games_with_replacement(
            games, available_cubes)
        print(f"Part 1 result: {sum_possible_games_idx}")
        print(f"Part 2 result: {sum_min_needed_cubes(games)}")

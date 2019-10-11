import nflgame
import argparse
import score_stats
import fit_distribution


def find_id(target_name, year):
    ids_found = set()
    games = nflgame.games(year)
    for game in games:
        for player in game.max_player_stats():
            if target_name == player.name:
                ids_found.add(player.playerid)
    return ids_found


def get_player_stats(target_id, year, per_game_stats):
    games = nflgame.games(year)
    for game in games:
        for player in game.max_player_stats():
            if target_id == player.playerid:
                per_game_stats[game.gamekey] = player.stats


def multi_year_stats(player):
    stats = {}
    for year in [2018, 2019]:

        ids = find_id(player, year)
        if len(ids) != 1:

            print("Non-one id found")
            print(year)
            print(ids)
            return None
        else:
            target_id = ids.pop()
            get_player_stats(target_id, year, stats)
    return stats


if __name__ == "__main__":
    # argument parsing
    parser = argparse.ArgumentParser(
        description="Generate rough distributions of player points"
    )

    parser.add_argument(
        "--config-file", help="PATH to JSON config file", dest="config_file"
    )
    parser.add_argument("--player", help="player name", dest="player")
    args = parser.parse_args()
    print(args)
    print("")
    player = args.player
    stats = multi_year_stats(player)
    if stats:
        points = []
        for key, value in stats.items():
            points.append(score_stats.score(value))
        print(points)
        dist_name = fit_distribution.fit_player(points, player)
        print(dist_name.name)

import nflgame
import argparse
import score_stats
import fit_distribution


def find_id(target_name, year):
    ids_found = set()
    games = nflgame.games(year)
    for game in games:
        for player in game.max_player_stats():
            name_and_pos = str(player.player)
            full_name = name_and_pos.split("(")[0].strip()
            if target_name == full_name:
                ids_found.add(player.playerid)
    return ids_found


def get_player_stats(target_id, year, per_game_stats):
    games = nflgame.games(year)
    for game in games:
        for player in game.max_player_stats():
            if target_id == player.playerid:
                per_game_stats[game.gamekey] = player.stats


def multi_year_stats(player, years):
    stats = {}
    for year in years:
        year = int(year)
        ids = find_id(player, year)
        if len(ids) != 1:
            print("Did not find exactly one id for player")
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
    parser.add_argument("--years", nargs="+")
    parser.add_argument("--ppr", help="default is half PPR", type=float)
    parser.add_argument("--player", help="player name", dest="player")
    parser.add_argument(
        "--bucket-size",
        help="Bucket size in histogram is roughly this many fantasy points (Default 2)",
        type=int,
        dest="bucket_size",
    )
    args = parser.parse_args()
    print(args)
    print("")
    player = args.player
    ppr = args.ppr
    bucket_size = args.bucket_size
    if bucket_size is None or bucket_size < 0:
        bucket_size = 2
    if ppr is None:
        ppr = 0.5
    years = args.years
    stats = multi_year_stats(player, years)
    if stats:
        points = []
        for key, value in stats.items():
            points.append(score_stats.score(value, ppr))
        print(points)
        dist_name = fit_distribution.fit_player(points, player, ppr, bucket_size)
        print(dist_name.name)

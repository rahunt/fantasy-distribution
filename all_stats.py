import nflgame
import argparse
import score_stats
import fit_distribution
import os


def build_stats(years):
    stats = {}
    name_lookup = {}
    games = nflgame.games(years)
    for game in games:
        for player in game.max_player_stats():
            name_and_pos = str(player.player)
            full_name = name_and_pos.split("(")[0].strip()
            if player.playerid not in stats:
                stats[player.playerid] = {}
            stats[player.playerid][game.gamekey] = player.stats
            name_lookup[player.playerid] = full_name

    return stats, name_lookup


pprs = [(0.0, "Standard"), (0.5, "Half-PPR"), (1.0, "PPR")]


def make_and_save_graphs(root, stats, player_name):
    player_path = root + "/" + player_name
    try:
        os.makedirs(player_path, exist_ok=True)
        for x in pprs:
            ppr, ppr_name = x
            points = []
            save_file = player_path + "/" + ppr_name + ".png"
            print(save_file)
            for key, value in stats.items():
                points.append(score_stats.score(value, ppr))
                dist_name = fit_distribution.fit_player(
                    points, player_name, ppr, bucket_size, save_file=save_file
                )
    except Exception as ex:
        print("Error generating graphs for : " + player_name)
        print(ex)
        try:
            os.rmdir(player_path)
        except:
            print("Error removing : " + player_path)


if __name__ == "__main__":
    # argument parsing
    parser = argparse.ArgumentParser(
        description="Generate rough distributions of player points"
    )
    parser.add_argument("--years", type=int, nargs="+")
    parser.add_argument("--root-directory", help="rootdir", dest="root")
    parser.add_argument(
        "--bucket-size",
        help="Bucket size in histogram is roughly this many fantasy points (Default 2)",
        type=int,
        dest="bucket_size",
    )
    args = parser.parse_args()
    print(args)
    print("")
    root = args.root
    bucket_size = args.bucket_size
    if bucket_size is None or bucket_size < 0:
        bucket_size = 2
    years = args.years
    stats, name_lookup = build_stats(years)
    for player_id in stats.keys():
        player_stats = stats[player_id]
        player_name = name_lookup[player_id]
        print(player_name)
        make_and_save_graphs(root, player_stats, player_name)

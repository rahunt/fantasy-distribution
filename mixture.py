import numpy as np
import matplotlib.pyplot as plt
import get_stats


def team_mixture(best_fits):
    n = len(best_fits)
    res = best_fits[0].pdf
    for i in range(1, len(best_fits)):
        res += best_fits[i].pdf
    res = res / n
    print(res)
    return res


def win_probabilities(team_a_mix, team_b_mix):
    return (0, 0)


# NOTE: It would be nice to allow for manual mean input (could use external projections)
def bfds(player_list, stats, ppr, bucket_size):
    team_dists = []
    for player in player_list:
        if player not in stats:
            print("unable to find stats for:" + player)
            return None
        else:
            points = stats[player]
            team_dists.append(
                fit_distribution.fit_player(
                    points, player, ppr, bucket_size, save_file=False
                )
            )
    return team_dists


def plot_teams(team_a_mix, team_a_name, team_b_mix, team_b_name):
    return None


if __name__ == "__main__":
    # argument parsing
    parser = argparse.ArgumentParser(
        description="Generate rough distributions of team points and win probabilities"
    )
    parser.add_argument("--years", nargs="+")
    parser.add_argument("--ppr", help="default is half PPR", type=float)
    parser.add_argument(
        "--team-configs", help="json file of teams ", dest="team_configs"
    )
    parser.add_argument(
        "--bucket-size",
        help="Bucket size in histogram is roughly this many fantasy points (Default 2)",
        type=int,
        dest="bucket_size",
    )
    args = parser.parse_args()
    print(args)
    team_config_file = args.team_configs
    ppr = args.ppr
    bucket_size = args.bucket_size
    if bucket_size is None or bucket_size < 0:
        bucket_size = 2
    if ppr is None:
        ppr = 0.5
    years = args.years
    all_players = []
    team_a_players = []
    team_b_players = []
    stats = get_stats.multi_year_points(all_players, years)
    team_a_dists = bfds(team_a_players, stats, ppr, bucket_size)
    team_b_dists = bfds(team_b_players, stats, ppr, bucket_size)
    if not team_a_dists or not team_b_dists:
        return None
    team_a_mix = mixture(team_a_dists)
    team_b_mix = mixture(team_b_dists)
    plot_teams(team_a_mix, team_a_name, team_b_mix, team_b_name)
    probs = win_probabilities(team_a_mix, team_b_mix)
    print(team_a_name + " probability : " + str(probs[0]))
    print(team_b_name + " probability : " + str(probs[0]))

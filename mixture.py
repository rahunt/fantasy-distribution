import argparse
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt
from scipy import signal

import get_stats
import fit_distribution
import team_config

def team_mixture(best_fits):
    n = len(best_fits)
    res = best_fits[0].pdf
    pad_x = len(res)
    for i in range(1, len(best_fits)):
        player = best_fits[i].pdf
        print(sum(player))
        print(best_fits[i].player_name + ":"+ str(player))
        padded = np.pad(player,(0, (i-1)*pad_x))
        res = signal.fftconvolve(res,padded,mode='full')
        res
        res = np.append(res,[0,0])[:pad_x*(i+1)]
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
                    points, player, ppr, bucket_size, save_file=True
                )
            )
    return team_dists

def plot_team(team_mix,team_name,team_players):
    plt.figure(figsize=(12, 8))
    start =0
    size = len(team_mix)
    end = (size / 10000 )* 50 
    x = np.linspace(start, end, size)
    pdf = team_mix
    print(pdf)
    print("TEAM MIX SUM " + str(sum(pdf)))
    pdf_series = pd.Series(pdf, x)
    print(pdf_series)
    ax = pdf_series.plot(lw=2, label=(team_name +": bfd"), legend=True)
    players = ", ".join(team_players)
    ax.set_title(team_name + "\n Players: " + players )
    ax.set_xlabel(u"Points")
    ax.set_ylabel("Frequency")
    ax.set_ylim(0, max(team_mix))
    
    plt.savefig(team_name + ".png")


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
    config = team_config.Config(team_config_file)
    ppr = args.ppr
    bucket_size = args.bucket_size
    if bucket_size is None or bucket_size < 0:
        bucket_size = 2
    if ppr is None:
        ppr = 0.5
    years = args.years
    all_players = config.team_a_players + config.team_b_players
    team_a_players = config.team_a_players
    team_b_players = config.team_b_players
    team_a_name = config.team_a_name
    team_b_name = config.team_b_name
    stats = get_stats.multi_player_points(all_players, years,ppr)
    team_a_dists = bfds(team_a_players, stats, ppr, bucket_size)
    team_a_mix = team_mixture(team_a_dists)
    plot_team(team_a_mix, team_a_name, team_a_players)
    '''
    team_b_dists = bfds(team_b_players, stats, ppr, bucket_size)
    if not team_a_dists or not team_b_dists:
        return None
    team_a_mix = mixture(team_a_dists)
    team_b_mix = mixture(team_b_dists)
    plot_teams(team_a_mix, team_a_name, team_b_mix, team_b_name)
    probs = win_probabilities(team_a_mix, team_b_mix)
    print(team_a_name + " probability : " + str(probs[0]))
    print(team_b_name + " probability : " + str(probs[0]))
    '''

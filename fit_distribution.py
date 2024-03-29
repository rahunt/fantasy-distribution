import warnings
import numpy as np
import pandas as pd
import scipy.stats as st
import statsmodels as sm
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats._continuous_distns import _distn_names

matplotlib.rcParams["figure.figsize"] = (16.0, 12.0)
matplotlib.style.use("ggplot")

# Create models from data
def best_fit_distribution(data, bins=10, ax=None):
    """Model data by finding best fit distribution to data"""
    # Get histogram of original data
    y, x = np.histogram(data, bins=bins, density=True)
    x = (x + np.roll(x, -1))[:-1] / 2.0

    # Distributions to check
    DISTRIBUTIONS = map(lambda x: getattr(st, x), _distn_names)
    # Best holders
    best_distribution = st.norm
    best_params = (0.0, 1.0)
    best_sse = np.inf

    # Estimate distribution parameters from data
    for distribution in DISTRIBUTIONS:

        # Try to fit the distribution
        try:
            # Ignore warnings from data that can't be fit
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore")

                # fit dist to data
                params = distribution.fit(data)

                # Separate parts of parameters
                arg = params[:-2]
                loc = params[-2]
                scale = params[-1]

                # Calculate fitted PDF and error with fit in distribution
                pdf = distribution.pdf(x, loc=loc, scale=scale, *arg)
                sse = np.sum(np.power(y - pdf, 2.0))

                # if axis pass in add to plot
                try:
                    if ax:
                        pd.Series(pdf, x).plot(ax=ax)
                    end
                except Exception:
                    pass

                # identify if this distribution is better
                if best_sse > sse > 0:
                    best_distribution = distribution
                    best_params = params
                    best_sse = sse

        except Exception:
            pass

    return (best_distribution.name, best_params, best_sse)


def make_pdf(dist, params, size=10000):
    """Generate distributions's Probability Distribution Function """

    # Separate parts of parameters
    arg = params[:-2]
    loc = params[-2]
    scale = params[-1]
    '''
    # Get sane start and end points of distribution
    start = (
        dist.ppf(0.01, *arg, loc=loc, scale=scale)
        if arg
        else dist.ppf(0.01, loc=loc, scale=scale)
    )
    end = (
        dist.ppf(0.99, *arg, loc=loc, scale=scale)
        if arg
        else dist.ppf(0.99, loc=loc, scale=scale)
    )
    '''
    # NOTE: May need common x_axis to combine
    start = 0
    end = 50
    # Build PDF and turn into pandas Series
    x = np.linspace(start, end, size)
    pdf = dist.pdf(x, loc=loc, scale=scale, *arg)
    print(pdf)
    pdf_series = pd.Series(pdf, x)
    print(pdf_series)
    
    return pdf, pdf_series


class Best_fit_result:
    def __init__(self, pdf, distr, params, player_name):
        self.pdf = pdf
        self.distribution = distr
        self.params = params
        self.player_name = player_name
        self.dist_name = distr.name


def fit_player(fantasy_points, player_name, ppr, bucket_size, save_file=True):
    # Load data from statsmodels datasets
    data = pd.Series(fantasy_points)

    bins = int(max(fantasy_points) / bucket_size)
    # Plot for comparison
    plt.figure(figsize=(12, 8))
    ax = data.plot(kind="hist", bins=bins, density=True, alpha=0.5)
    # Save plot limits
    ax.set_ylim(0, 1)
    dataYLim = ax.get_ylim()

    # Find best fit distribution
    best_fit_name, best_fit_params, best_sse = best_fit_distribution(data, bins, ax)
    best_dist = getattr(st, best_fit_name)

    # Make PDF with best params
    pdf, pdf_series = make_pdf(best_dist, best_fit_params)

    result = Best_fit_result(pdf, best_dist, best_fit_params, player_name)
    # Display
    if not save_file:
        return result
    player_name = player_name.replace(" ", "_")
    # Currently not saved, could add the all overlay in the future (or best n)?
    ax.set_ylim(dataYLim)
    ax.set_title(player_name + u"\n All Fitted Distributions")
    ax.set_xlabel(str(ppr) + " PPR Points")
    ax.set_ylabel("Frequency")

    plt.figure(figsize=(12, 8))
    ax = pdf_series.plot(lw=2, label=(player_name + ":BFD"), legend=True)
    data.plot(
        kind="hist",
        bins=bins,
        density=True,
        alpha=0.5,
        label="Data",
        legend=True,
        ax=ax,
    )

    param_names = (
        (best_dist.shapes + ", loc, scale").split(", ")
        if best_dist.shapes
        else ["loc", "scale"]
    )
    param_str = ", ".join(
        ["{}={:0.2f}".format(k, v) for k, v in zip(param_names, best_fit_params)]
    )
    dist_str = "{}\n params:({})".format(best_fit_name, param_str)

    sse_str = "\n Best SSE:" + str(round(best_sse, 8))
    ax.set_title(player_name + "\nWith best fit distribution: " + dist_str + sse_str)
    ax.set_xlabel(u"0.5 PPR Points")
    ax.set_ylabel("Frequency")
    plt.savefig(player_name + ".png")
    return result

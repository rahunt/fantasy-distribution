def safe_get(stats, key):
    if key in stats:
        return stats[key]
    else:
        return 0


def score(stats):
    rec_pts = safe_get(stats, "receiving_rec") * 0.5
    yds_pts = 0.1 * (
        safe_get(stats, "receiving_yds") + safe_get(stats, "rushing_yds")
    ) + (0.04 * safe_get(stats, "passing_yds"))
    td_pts = 6 * (
        safe_get(stats, "receiving_tds") + safe_get(stats, "rushing_tds")
    ) + 4 * safe_get(stats, "passing_tds")
    tpm_pts = 2 * (
        safe_get(stats, "receiving_twoptm")
        + safe_get(stats, "rushing_twoptm")
        + safe_get(stats, "passing_twoptm")
    )
    int_pts = (-2) * safe_get(stats, "passing_ints")
    fum_pts = (-2) * safe_get(stats, "fumbles_lost")
    return rec_pts + yds_pts + td_pts + tpm_pts

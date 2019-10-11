# fantasy-distribution
Graph a histogram of a player's Fantasy Football points as well as the best fitting distribution from scipy


## Setup
- Use python3
- Set up a venv
- dependencies: nflgame,scipy,matplotlib,pandas,numpy,statsmodels


## How to use
In venv: 
   python ./get_stats.py --player "Tyler Lockett" --years 2018 2019 --ppr 0.5

Writes out a png in current dir : Tyler_Lockett.png

![Tyler Lockett 2018-2019](https://github.com/rahunt/fantasy-distribution/blob/master/Tyler_Lockett.png)

![Alvin Kamara 2018-2019](https://github.com/rahunt/fantasy-distribution/blob/master/Alvin_Kamara.png)

## Known issues
- Doesn't account for injuries
- Lol rookies

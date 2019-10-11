# fantasy-distribution
Graph a histogram of a player's half PPR points as well as the best fitting distribution from scipy


## Setup
Use python3
Set up a venv
dependencies: nflgame,scipy,matplotlib,pandas,numpy,statsmodels


## How to use
In venv: 
   python ./get_stats.py --player "T.Lockett" --years 2018 2019

Writes out a png in current dir : T.Lockett.png

![Tyler Lockett 2018-2019](https://github.com/rahunt/fantasy-distribution/blob/master/T.Lockett.png)

![Alvin Kamara 2018-2019](https://github.com/rahunt/fantasy-distribution/blob/master/A.Kamara.png)

## Known issues
D.Williams vs. D.Williams will just error out
Matplot warnings due to deprecated args
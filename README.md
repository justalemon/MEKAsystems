# MEKAsystems

[![Heroku](https://img.shields.io/badge/heroku-deploy-79589F.svg)](https://heroku.com/deploy?template=https://github.com/justalemon/MEKAsystems)
[![CodeFactor](https://www.codefactor.io/repository/github/justalemon/ggov/badge)](https://www.codefactor.io/repository/github/justalemon/ggov)
[![Discord](https://img.shields.io/badge/discord-join-7289DA.svg)](https://discord.gg/Cf6sspj)

This is Discord a Bot created by me to be used in gaming and programming servers.

Most of the time, is running via automatic deployments on Heroku with a free Dyno (not ideal, but it works).

![Preview](https://raw.githubusercontent.com/justalemon/MEKAsystems/master/preview.png)

## Prerequisites

* Python 3.6 or higher
* [Discord.py](https://github.com/Rapptz/discord.py) 7f4c57dd5ad20b7fa10aea485f674a4bc24b9547 or higher
* [Motor](https://github.com/mongodb/motorpy) 2.0.0 or higher
* [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) 0.17.0 or higher ([python-Levenshtein](https://github.com/ztane/python-Levenshtein) is optional but recommended)
* [lxml](https://github.com/lxml/lxml) 4.3.0 or higher
* [youtube-dl](https://github.com/rg3/youtube-dl) 2019.1.16 or higher

## Install

* Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) (login not requried)
* Clone the repo or download the ZIP
* Create a `.env` file with the configuration values (see below)
* Run `heroku local`

## Configuration

To configure the Bot, edit or create a `.env` file and set the respective [configuration values](https://github.com/justalemon/MEKAsystems/blob/master/app.json#L23-L34).

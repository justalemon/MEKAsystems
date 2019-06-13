<div align="center">
<!-- <img src="https://raw.githubusercontent.com/justalemon/MEKAsystems/master/logo.png" width="750" /> -->
<br><br>
<a href="https://heroku.com/deploy?template=https://github.com/justalemon/MEKAsystems"><img src="https://img.shields.io/badge/heroku-deploy-79589F.svg"></a>
<a href="https://www.codefactor.io/repository/github/justalemon/mekasystems"><img src="https://www.codefactor.io/repository/github/justalemon/mekasystems/badge"></a>
<a href="https://dependabot.com"><img src="https://api.dependabot.com/badges/status?host=github&repo=justalemon/MEKAsystems"></a>
<a href="https://discord.gg/Cf6sspj"><img src="https://img.shields.io/badge/discord-join-7289DA.svg"></a>
<br><br>
This is Discord a Bot created by me to be used in gaming and programming servers.
<br>
Most of the time, is running via automatic deployments on Heroku with a free Dyno (not ideal, but it works).
<br><br>
<img src="https://raw.githubusercontent.com/justalemon/MEKAsystems/master/preview.png"/>
</div>

## Prerequisites

* Python 3.6 or higher
* [Discord.py](https://github.com/Rapptz/discord.py) 1.2.2 or higher
* [Motor](https://github.com/mongodb/motorpy) 2.0.0 or higher
* [dnspython](https://github.com/rthalley/dnspython) 1.16.0 or higher
* [FuzzyWuzzy](https://github.com/seatgeek/fuzzywuzzy) 0.17.0 or higher ([python-Levenshtein](https://github.com/ztane/python-Levenshtein) is optional but recommended)
* [lxml](https://github.com/lxml/lxml) 4.3.4 or higher
* [python-dotenv](https://github.com/theskumar/python-dotenv) 0.10.1 or higher (if you plan to run the bot manually)

## Install

* Create a `.env` file with the configuration values (see below)
* Then, you have two options:
  * Install the [Heroku CLI](https://devcenter.heroku.com/articles/heroku-cli) and run `heroku local` (login not requried)
  * Run `python launch.py --env --manual`

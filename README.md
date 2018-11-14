# Mazzotta Bot

My telegram bot.

## Commands

|Command|Action|
|---|---|
|/help|Show this text|
|/say|Ask the bot to say something in a bot voice|
|/sing|Ask the bot to sing something in a bot voice|
|/zhaw|Show current ZHAW stats|

## Getting Started

### Prerequisites
* Docker 18 or later

### Bootstrap

```
# Get the code, cd to mazzotta-bot, setup mazzotta-bot in Docker
git clone git@github.com:emazzotta/mazzotta-bot.git && \
    cd mazzotta-bot && \
    make bootstrap
```

### Configure

Configure your `.env`-file.

### Run

```
make start
```

## Author

[Emanuele Mazzotta](mailto:hello@mazzotta.me)

[![Build Status](https://travis-ci.org/emazzotta/mazzotta-bot.svg?branch=master)](https://travis-ci.org/emazzotta/mazzotta-bot)

# Mazzotta Bot

🤖 My telegram bot with features I find useful in a bot.

## Commands

|Command|Action|
|---|---|
|/help|Show this text|
|/s|Explain what /s stands for|
|/say|Say something in a bot voice (/say [lang=de] <text>)|
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

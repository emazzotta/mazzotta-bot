FROM python:3.7-alpine3.8

LABEL maintainer="hello@mazzotta.me"

ENV PYTHONPATH /app:$PYTHONPATH
ENV TZ=Europe/Zurich

WORKDIR /app

RUN apk add --update --no-cache \
    bash \
    bc \
    espeak \
    ffmpeg \
    && rm -rf /var/lib/apt/lists/* /var/cache/apk/* \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime \
    && echo $TZ > /etc/timezone \
    && wget https://raw.githubusercontent.com/emazzotta/dotfiles/master/bin/kw -O /usr/local/bin/kw \
    && chmod 755 /usr/local/bin/kw \
    && wget https://raw.githubusercontent.com/emazzotta/dotfiles/master/bin/progressbar -O /usr/local/bin/progressbar \
    && chmod 755 /usr/local/bin/progressbar

COPY requirements.txt /app
RUN pip install -r requirements.txt

COPY src /app/src

CMD ["python", "src/bot.py"]

FROM node:alpine
# Adds a compiler so python can compile the python requirements
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot
RUN apk add --no-cache --virtual .pynacl_deps build-base python3-dev libffi-dev


# Install Python
ENV PYTHONUNBUFFERED=1
RUN apk add --update --no-cache python3 && ln -sf python3 /usr/bin/python
RUN python3 -m ensurepip
RUN pip3 install --no-cache --upgrade pip setuptools

# Rest of my stuff
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY .env .
COPY music ./music
COPY discord_bot.py .
# Add ffmpeg
RUN apk add  --no-cache ffmpeg


CMD [ "python", "discord_bot.py" ]
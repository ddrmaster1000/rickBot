FROM python:3
# Adds a compiler so python can compile the python requirements
RUN mkdir -p /usr/src/bot
WORKDIR /usr/src/bot

# Rest of my stuff
COPY requirements.txt .
RUN pip install -r requirements.txt
# COPY .env .
COPY rick_bot.py .

CMD [ "python", "rick_bot.py" ]
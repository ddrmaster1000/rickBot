# Most code credits go to https://github.com/RuolinZheng08/twewy-discord-chatbot
# the os module helps us access environment variables
# i.e., our API keys
import os

# these modules are for querying the Hugging Face model
import json
import requests

# the Discord Python API
import discord

# Other
from dotenv import load_dotenv
import re

load_dotenv()


# this is my Hugging Face profile link
API_URL = 'https://api-inference.huggingface.co/models/'

class MyClient(discord.Client):
    def __init__(self, model_name):
        super().__init__()
        self.model_name = model_name
        self.api_endpoint = API_URL + model_name
        # retrieve the secret API token from the system environment
        huggingface_token = os.getenv('HUGGINGFACE_TOKEN')
        # format the header in our request to Hugging Face
        self.request_headers = {
            'Authorization': 'Bearer {}'.format(huggingface_token)
        }

    def query(self, payload):
        """
        make request to the Hugging Face model API
        """
        data = json.dumps(payload)
        response = requests.request('POST',
                                    self.api_endpoint,
                                    headers=self.request_headers,
                                    data=data)
        ret = json.loads(response.content.decode('utf-8'))
        return ret

    async def on_ready(self):
        # print out information when the bot wakes up
        print('Logged in as')
        print(self.user.name)
        print(self.user.id)
        print('------')
        # send a request to the model without caring about the response
        # just so that the model wakes up and starts loading
        self.query({'inputs': {'text': 'Hello!'}})

    async def on_message(self, message):
        """
        this function is called whenever the bot sees a message in a channel
        """
        # ignore the message if it comes from the bot itself
        if message.author.id == self.user.id:
            return

        print(message.channel)
        # Forces the bot to only be used in a specific text channel.
        if str(message.channel) != "rick-chat":
            return

        # # form query payload with the content of the message
        # # The below is if you wanted to use the history of the channel into the model.
        # # It seems kinda weird when you do this.
        # messages = await message.channel.history(limit=5).flatten()
        # message_string = ""
        # for message in messages:
        #     # message_string += f"{message.author}: {message.content}\n"
        #     message_string += f"{message.content}\n"
        # message_string += "Rick:"
        # payload = {'inputs': {'text': f"{message_string}"}}

        # print(payload)
        payload = {'inputs': {'text': message.content}}
        # while the bot is waiting on a response from the model
        # set the its status as typing for user-friendliness
        async with message.channel.typing():
            response = self.query(payload)
        bot_response = response.get('generated_text', None)
        print("got response")

        # we may get ill-formed response if the model hasn't fully loaded
        # or has timed out
        if not bot_response:
            if 'error' in response:
                bot_response = '`Error: {}`'.format(response['error'])
            else:
                bot_response = 'Hmm... something is not right.'

        # Model is still Loading
        if f"Error: Model {self.model_name} is currently loading" in str(bot_response):
            await message.reply(f"Sorry {message.author.mention}, I'm grabbing a damn beer. Give me 1 FREAking *BURB* minute.")
            return

        # send the model's response to the Discord channel
        await message.channel.send(bot_response)

def main():
    # ddrmaster1000/DialoGPT-medium-rick is my model name
    client = MyClient('ddrmaster1000/DialoGPT-medium-rick')
    client.run(os.getenv('DISCORD_TOKEN'))

if __name__ == '__main__':
  main()
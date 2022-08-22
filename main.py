import discord
from discord import Intents
from discord.ext import tasks

import random
import datetime

import os
from dotenv import load_dotenv

load_dotenv('.env')
channel_id = int(os.getenv('CHANNEL_ID'))


def get_random_date(start_date, end_date):
    # get diff between start and end, use result to generate random day
    time_between_dates = end_date - start_date
    days_between_dates = time_between_dates.days
    random_number_of_days = random.randrange(days_between_dates)

    random_date = start_date + datetime.timedelta(days=random_number_of_days)
    return datetime.datetime.combine(random_date, datetime.time(0, 0))


class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    async def on_ready(self):
        print(f'Logged in as {self.user} (ID: {self.user.id})')
        self.post_random_message.start()

    async def select_message(self):
        channel = self.get_channel(channel_id)
        messages = []
        # loops until it finds a date where messages were posted
        while not messages:
            date_earliest_msg = datetime.date(2022, 8, 13)
            rand_date = get_random_date(date_earliest_msg, datetime.date.today())
            print(rand_date)
            rand_date_nextday = rand_date + datetime.timedelta(days=1)
            # use rand_date to get list of messages from one randomly selected day
            messages = [message async for message in channel.history(limit=10,
                                                                     before=rand_date_nextday,
                                                                     after=rand_date)]
        message = messages[random.randrange(len(messages))]
        if message.author == client.user:
            return await self.select_message()
        return message

    @tasks.loop(hours=24)
    async def post_random_message(self):
        message = await self.select_message()
        await message.reply(content=message.content)

    @post_random_message.before_loop
    async def before_my_task(self):
        print("this is before_my_task")
        await self.wait_until_ready()


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(os.getenv('TOKEN'))

import discord
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
        while not messages:
            random_date = get_random_date(datetime.date(2022, 8, 13), datetime.date.today())
            print(random_date)
            messages = await channel.history(limit=3,
                                             before=random_date + datetime.timedelta(days=1),
                                             after=random_date
                                             ).flatten()
        print(messages[0].content)
        return messages[0]

    # async def select_message(self):
    #     channel = self.get_channel(699334420678705243)
    #     messages = []
    #     while not messages:
    #         random_date = get_random_date(datetime.date(2022, 8, 13), datetime.date.today())
    #         print(random_date)
    #         messages = await channel.history(limit=3,
    #                                          before=random_date + datetime.timedelta(days=1),
    #                                          after=random_date
    #                                          ).flatten()
    #     print(messages[0].content)
    #     return messages[0]

    @tasks.loop(seconds=30)
    async def post_random_message(self):
        channel = self.get_channel(channel_id)
        message = await self.select_message()
        await channel.send(message.content)

    @post_random_message.before_loop
    async def before_my_task(self):
        print("this is before_my_task")
        await self.wait_until_ready()


client = MyClient(intents=discord.Intents.default())
client.run(os.getenv('TOKEN'))

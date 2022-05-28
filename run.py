"""Send a windows notification when a specific discord user logs in."""
import sys
import datetime
import json

import discord
from notifypy import Notify

intents = discord.Intents().all()
client = discord.Client(intents=intents)
user_id = int(input("User id: "))

notif = Notify()

def log(user):
    """Logs user log in time"""

    with open("log.json", "r", encoding='utf-8') as file:
        data = json.load(file)

    jsn = {"user": user, "time": datetime.datetime.now().strftime("%H:%M:%S")}
    data.append(jsn)

    with open("log.json", "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)

@client.event
async def on_member_update(before, after):
    """Runs when a member state updates"""
    on_states = ["online", "idle", "dnd"]

    if str(before.status) == "offline" and str(after.status) in on_states and after.id == user_id:
        print(f'User {after.name} log in detected')
        notif.application_name = "Python"
        notif.title = 'Discord login'
        notif.message = f'{after.name} log in detected'
        notif.send()

        log(after.name)
        sys.exit()

@client.event
async def on_ready():
    """Runs when the bot is ready"""
    uname = client.get_user(user_id)
    if uname is None:
        print("User not found")
        await client.close()
    else:
        print("Waiting for user:",uname)

client.run('YOUR_TOKEN')

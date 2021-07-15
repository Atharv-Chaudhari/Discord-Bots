from keep_alive import keep_alive
import discord
import os
from calendar import monthrange
import requests
import json
from replit import db
from urllib.request import urlopen
from datetime import datetime, date

today_date = datetime.today().date()
#first_day_of_month = today_date.replace(day=1)
last_day_of_month = today_date.replace(
    day=monthrange(today_date.year, today_date.month)[1])
client = discord.Client()

if "responding" not in db.keys():
    db["responding"] = True


def get_data():
    url = os.getenv('url')
    response = urlopen(url)
    data_json = json.loads(response.read())
    return (data_json)

def get_data_end():
    url = os.getenv('url_end')
    response = urlopen(url)
    data_json = json.loads(response.read())
    return (data_json)


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    msg = message.content
    #embed = discord.Embed()
    if msg.startswith("$upcoming_all_contests"):
        data = get_data()
        t = data['objects']
        q = 0
        t.reverse()
        for i in range(len(t)):
            z = t[i]['start'].split('T')[0].split("-")
            start_date = date(int(z[0]), int(z[1]), int(z[2]))
            if (start_date >= today_date):
              q = q + 1
              await message.channel.send("Name :-" + t[i]['event']+"\nStart Date :- " +t[i]['start'].split('T')[0] +"\nEnd Date :- " +t[i]['end'].split('T')[0])
              await message.channel.send(("Link :-", t[i]['href']))
              if (q == 15):
                break
        await message.channel.send("Note :- Only Upcoming 15 Contests Will be visible")

    if msg.startswith("$upcoming_contests"):
        data = get_data()
        t = data['objects']
        #for i in range(len(t)):
        for i in range(len(t)):
            z = t[i]['start'].split('T')[0].split("-")
            start_date = date(int(z[0]), int(z[1]), int(z[2]))
            if (start_date >= today_date and start_date <= last_day_of_month):
                await message.channel.send("Name :-" + t[i]['event']+"\nStart Date :- " +t[i]['start'].split('T')[0] +"\nEnd Date :- " +t[i]['end'].split('T')[0])
                await message.channel.send(("Link :-", t[i]['href']))
                #embed.description = "[Link]((t[i]['href']))"
                #await message.channel.send(embed=embed)
    if msg.startswith("$ongoing_all_contests"):
        data = get_data_end()
        t = data['objects']
        #for i in range(len(t)):
        t.reverse()
        for i in range(len(t)):
            z = t[i]['start'].split('T')[0].split("-")
            start_date = date(int(z[0]), int(z[1]), int(z[2]))
            z = t[i]['end'].split('T')[0].split("-")
            end_date = date(int(z[0]), int(z[1]), int(z[2]))
            if (end_date > today_date and start_date <= today_date):
                await message.channel.send("Name :-" + t[i]['event']+"\nStart Date :- " +t[i]['start'].split('T')[0] +"\nEnd Date :- " +t[i]['end'].split('T')[0])
                await message.channel.send(("Link :-", t[i]['href']))
    if msg.startswith("$ongoing_contests"):
        data = get_data_end()
        t = data['objects']
        #for i in range(len(t)):
        t.reverse()
        q=0
        for i in range(len(t)):
            z = t[i]['start'].split('T')[0].split("-")
            start_date = date(int(z[0]), int(z[1]), int(z[2]))
            z = t[i]['end'].split('T')[0].split("-")
            end_date = date(int(z[0]), int(z[1]), int(z[2]))
            if (end_date > today_date and start_date <= today_date):
              q=q+1
              await message.channel.send("Name :-" + t[i]['event']+"\nStart Date :- " +t[i]['start'].split('T')[0] +"\nEnd Date :- " +t[i]['end'].split('T')[0])
              await message.channel.send(("Link :-", t[i]['href']))
            if(q==15):
              break
        await message.channel.send("Note :- Only ongoing 15 Contests Will be visible who have end date near")

    if msg.startswith("$responding"):
        value = msg.split("$responding ", 1)[1]

        if value.lower() == "true":
            db["responding"] = True
            await message.channel.send("Responding is on.")
        else:
            db["responding"] = False
            await message.channel.send("Responding is off.")


keep_alive()
client.run(os.getenv('TOKEN'))

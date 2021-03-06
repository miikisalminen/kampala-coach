import os
from dotenv import dotenv_values
import discord


temp = dotenv_values(".env")
TOKEN = temp["DISCORD_TOKEN"] #grab token from .env file instead

members = []
f = open("db.txt", "r")
for member in f:
    members.append([member.split(":")[0],int(member.split(":")[1].strip())])
print(members)
client = discord.Client()

def write_to_db(author):
    f = open("db.txt", "a")
    f.write("{0}:0\n".format(author))
    f.close
    members.append([str(author), 0])
    print(members)
    
def update_to_db(sum, author):
    for i in members:
        if i[0] == author:
            i[1] = i[1] + sum
    
    open("db.txt", "w").close()
    f = open("db.txt", "a")
    for i in members:
        f.write("{0}:{1}\n".format(i[0], i[1]))
    f.close()

@client.event
    
async def on_message(message):

    if message.channel.id != 995774810179260456 and not message.author.bot and message.content[0] == '%':
        response = "And who the fuck are you? Meet me at <#995774810179260456> and we'll talk."
        await message.channel.send(response)
        return

    found = False
    for i in members:
        if i[0] == str(message.author):
            found = True
        
    if message.content =="%register":
        for i in members:
            if found:
                response = "You're already in the game champ!"
                
        if not found:
            response = "Alright {0}! I'm putting you on the list.".format(message.author)
            write_to_db(message.author)
        
        print(response)
        await message.channel.send(response)

    if message.content.split()[0] =="%log":
        
        if message.content.split()[1] =="walk" and found:
            update_to_db(int(message.content.split()[2]),str(message.author))
            response="Good job, I'm putting down {0} minutes of walking for you. **(+{0} <:KAP:995930394715246642>)** :man_walking:".format(message.content.split()[2])
        elif message.content.split()[1] =="run" and found:
            update_to_db(int(message.content.split()[2])*2,str(message.author))
            response="Good job, I'm putting down {0} minutes of running for you. **(+{1} <:KAP:995930394715246642>)** :man_running:".format(message.content.split()[2],int(message.content.split()[2])*2)    
        elif message.content.split()[1] =="bike" and found:
            update_to_db(int(message.content.split()[2])/2,str(message.author))
            response="Good job, I'm putting down {0} minutes of biking for you. **(+{1} <:KAP:995930394715246642>)** :bike:".format(message.content.split()[2],int(message.content.split()[2])/2)    
        elif message.content.split()[1] =="gym" and found:
            update_to_db(int(message.content.split()[2])*2,str(message.author))
            response="Good job, I'm putting down {0} minutes of gym for you. **(+{1} <:KAP:995930394715246642>)** :muscle:".format(message.content.split()[2],int(message.content.split()[2])*2)    
        else:
            response="We dont do that in this gym... Are you sure you're registered?"
        await message.channel.send(response)

    if message.content =="%leaderboard":
        response = " :trophy: **KAMPALA ACTIVITY LEADERBOARD** :trophy: \n"
        for i in sorted(members, key=lambda x: x[1])[::-1]:
            response+= "{0} : {1} <:KAP:995930394715246642>\n".format(i[0], i[1])

        await message.channel.send(response)

async def on_ready():
    print("ONLINE")

client.run(TOKEN)
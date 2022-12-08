from handlers import *
from disnake.ext import *
import disnake
from log import *
import json
import pysondb
from json import dump
from pathlib import Path

def jsonDelete(data, id):
    with open(f"xp/{id}.json", "r+") as file:
        fileText = file.read().replace(data, "")
        file.close
    with open(f"xp/{id}.json", "w") as file:
        file.write(fileText)
        file.close()

def jsonCreate(data):
    with open(f"xp/{data}.json", "a") as file:
        file.close()

def jsonAdd(data, id):
    with open(f"xp/{id}.json", "r+") as file:
        file.write(str(data))
        file.close()

def jsonRead(data, id):
    with open(f"xp/{id}.json", "r+") as file:
        for x in file.readlines():
            if str(data) in str(x):
                return x

class ownerCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        rootLogger.info("Модуль {} подключен!".format(self.__class__.__name__))

    @commands.slash_command(
        name="addlvl",
        description="add lvl to user")
    @commands.has_role("админмяу")
    async def addlvl(ctx, member: disnake.Member, amount: int):
        userData = jsonRead(member.id, member.id).replace(""", """)
        userDataList = json.loads(userData)
        userCoin = userDataList["coin"]
        userLVL = userDataList["lvl"]
        userXP = userDataList["xp"]
        giveCoin = random.randint(1, 10)
        newUserCoins = int(giveCoin) + int(userCoin)
        newUserLvL = int(userLVL) + int(amount)
        jsonDelete(str(jsonRead(member.id, member.id)), member.id)
        jsonAdd({"user":member.id, "coin":newUserCoins, "lvl":newUserLvL, "xp":0}, member.id)
        await ctx.send(f"Done. New user lvl: {newUserLvL}")


    @commands.slash_command(
        name="deletechannels",
        description="Удаление каналов")
    @commands.has_any_role(810213578333224960,912548559247798272)
    async def deletechannels(inter, channelnames: str):
        for channel in inter.guild.channels:
            if channel.name == channelnames:
                await channel.delete()

    @commands.slash_command(name="indexating", description="Индексирование пользователей")
    @commands.has_any_role(912548559247798272)
    async def index(inter):
        time1 = datetime.datetime.now()
        async for member in bot.get_guild(inter.guild_id).fetch_members():
                        userMention = member.mention
                        userID = member.id
                        path = Path("users/users.json")
                        data = json.loads(path.read_text(encoding="utf-8"))
                        newUserData = {
                            f"{member.id}":{
                                "userID":member.id,
                                "warnCounter":0,
                                "muteCounter":1,
                                "userMention":f"{member.mention}",
                                "guild": f"{inter.guild_id}"
                                },
                            }     
                        data["users"][f"{inter.guild_id}"].append(newUserData)
                        path.write_text(json.dumps(data, indent=7), encoding="utf-8", newline="\n")
        time2 = datetime.datetime.now()
        time = time2-time1
        await inter.response.send_message(f"OK, {time}", ephemeral=True)
        
    
    


def setup(bot):
    bot.add_cog(ownerCommands(bot))

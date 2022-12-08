from handlers import now, takeSettings, bot
from disnake import *
from disnake.ext import *
from log import *
import json
import random
import os
from pathlib import Path
import log

class xp_module(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        rootLogger.info("Модуль {} подключен!".format(self.__class__.__name__))

    @bot.listen()
    async def on_message(message):
        if message.guild.id != 780911193329762305:
            return
        elif not message.author.bot:
            path = Path(f"xp/users_{message.guild.id}.json")
            data = json.loads(path.read_text(encoding="utf-8"))
            userID = message.author.id
            if f"{message.author.id}" not in data:
                userWritedData = {
                            f"{message.author.id}":[{
                                "user": message.author.id,
                                "coin": 0,
                                "lvl": 0,
                                "user_xp": 0,
                                "guild": message.guild.id
                            }],
                    }
                data["users"][f"{message.guild.id}"].update(userWritedData)
                path.write_text(json.dumps(data, indent=6), encoding="utf-8", newline="\n") 
                
            path = Path(f"xp/users_{message.guild.id}.json")
            data = json.loads(path.read_text(encoding="utf-8"))       
            userDataList = data["users"][f"{message.guild.id}"][f'{userID}'][0]

            print(data["users"][f"{message.guild.id}"][f'{message.author.id}'])
            userID = userDataList['user']
            userCoin = userDataList["coin"]
            userLVL = userDataList["lvl"]
            userXP = userDataList['user_xp']
            otherUserXP = data["users"][f"{message.author.id}"][0]
            userGUILD = userDataList["guild"]
            print(otherUserXP)
            print(userXP)
            if int(userXP) >= 100:
                giveCoin = 50
                newUserCoins = int(giveCoin) + int(userCoin)
                newUserLvL = int(userLVL) + 1
                newUserXP = 0
                data["users"][f"{message.guild.id}"][f"{message.author.id}"]["coin"] = newUserCoins
                data["users"][f"{message.guild.id}"][f"{message.author.id}"][0]["lvl"] = newUserLvL
                data["users"][f"{message.guild.id}"][f"{message.author.id}"][0]["user_xp"] = newUserXP
                path.write_text(json.dumps(data, indent=6), encoding="utf-8", newline="\n")
                emb = disnake.Embed(title="**Koshki.bot ALERT**", description=f"🎉 {message.author.mention}, у вас новый уровень!\n**Ваш Уровень:** {newUserLvL}", colour=disnake.Colour.from_rgb(47, 49, 54))
                await bot.get_channel(int(takeSettings(message.guild.id, "lvl_alert_channel"))).send(f"{message.author.mention}", embed=emb)

            else:
                newUserXP = userXP + random.randint(1, 5)
                data["users"][f"{message.author.id}"][0]["user_xp"] = newUserXP
                path.write_text(json.dumps(data, indent=6), encoding="utf-8", newline="\n")
        if not message.author.bot:
            log.rootLogger.info(f'[TIME: {now}][GUILD: {message.guild.id}][GUILD_NAME: {message.guild.name}][MESSAGE_FROM: {message.author.id}/{message.author.name}] Message: {message.content}')                
            



def setup(bot):
    bot.add_cog(xp_module(bot))

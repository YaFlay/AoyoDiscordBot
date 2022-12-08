from disnake.ext import commands
import disnake
from handlers import *
import json
from log import *
from pysondb import db
from pathlib import Path
def jsonRead(data):
    with open("database.json", "r") as file:
        for x in file.readlines():
            if str(data) in str(x):
                return x

def jsonDelete(data):
    with open("database.json", "r") as file:
        fileText = file.read().replace(data, "")
        file.close
    with open("database.json", "w") as file:
        file.write(fileText)
        file.close()

def jsonAdd(data):
    with open("database.json", "r+") as file:
        file.write(str(data))
        file.close()

class changeNick(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        rootLogger.info("Модуль {} Включен".format(self.__class__.__name__))

    @commands.slash_command(
        name="changenick",
        description="Меняет никнейм ")
    async def changenick(self, inter, member: disnake.Member, changednick):
        path = Path("users/user.json")
        readedData = json.loads(path.read_text(encoding="utf-8"))    
        if f"{member.id}" not in readedData[f"{inter.guild_id}"]:
            userData = {
                    f"{member.id}":{
                        "userID":member.id,
                        "warnCounter":0,
                        "muteCounter":0,
                        "userMention":f"{member.mention}",
                        "guild":f"{member.guild.id}"
                    }
                }


            data[f"{inter.guild_id}"].append(userData)
            path.write_text(json.dumps(data, indent=6), encoding="utf-8", newline="\n")
        
        warnCounter = readedData[f"{inter.guild_id}"][f"{member.id}"]["warnCounter"]     
        e = disnake.Embed(description="Koshki.Moderation SYSTEM", color = disnake.Color.purple())
        e.add_field(name = "**Сменил:**", value = inter.author.mention)
        e.add_field(name = "**Старый ник:**", value = member.name)
        e.add_field(name = "**Новый ник:**", value = changednick)
        e.add_field(name = "**Количество смененных ников:**", value = warnCounter)
        channel = bot.get_channel(int(takeSettings(inter.guild_id, "mute_channel")))
        await inter.response.send_message("Done.", ephemeral=True)
        if warnCounter >= 2:
            mute_role = disnake.utils.get(inter.guild.roles, id = 882170431279349770)
            await member.add_roles(mute_role)
            times_start = datetime.datetime.today()
            emb_user = disnake.Embed(title = "**Уведомление - Mute**", color = disnake.Color.purple())
            emb_user.add_field(name = "**Выдал:**", value = "SYSTEM", inline = False)
            emb_user.add_field(name = "**Причина:**", value = "ник", inline = False)
            emb_user.add_field(name = "**Длительность:**", value="Перманентный", inline = False)
            emb_user.add_field(name = "**Сервер:**", value = inter.guild.name, inline = False)
            emb_user.set_footer(text = f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

            emb = disnake.Embed(title = f"**System - Mute**", color = disnake.Color.purple())
            emb.add_field(name = "**Выдал:**", value =  "SYSTEM", inline = False)
            emb.add_field(name = "**Нарушитель:**", value = member.mention, inline = False)
            emb.add_field(name = "**ID нарушителя:**", value = member.id, inline = False)
            emb.add_field(name = "**Причина:**", value = "ник", inline = False)
            emb.add_field(name = "**Длительность:**", value = "пермач", inline = False)
            emb.set_footer(text = f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')

            await member.add_roles(mute_role)
            await channel.send(embed = emb)
            await member.send(embed = emb_user)
            await member.edit(nick=changednick)
            muteCounter = int(readedData[f"{inter.guild_id}"][f"{member.id}"]["muteCounter"]) + 1
            readedData[f"{inter.guild_id}"][f"{member.id}"]["muteCounter"].replace(readedData[f"{inter.guild_id}"][f"{member.id}"]["muteCounter"],muteCounter)
            path.write_text(json.dumps(readedData, indent=6), encoding="utf-8", newline="\n")
        else:
            await channel.send(embed = e)
            await member.edit(nick=changednick)
            await member.send(embed=e)
            userDataFromFile = readedData[f"{inter.guild_id}"][f"{member.id}"]
            warnCounter = int(jsonData[f"{member.id}"]["warnCounter"]) + 1
            readedData[f"{inter.guild_id}"][f"{member.id}"]["warnCounter"].replace(userDataFromFile["warnCounter"],muteCounter)
            path.write_text(json.dumps(data, indent=6), encoding="utf-8", newline="\n")



def setup(bot):
    bot.add_cog(changeNick(bot))

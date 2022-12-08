import handlers as hs
from handlers import takeSettings
import disnake
from disnake.ext import commands, tasks
import asyncio
import json
import os
from datetime import datetime, timedelta, timezone
import datetime as dt
from log import rootLogger
from pysondb import db
from pathlib import Path

def date_diff(str_date):
        try:
            dt_end = dt.datetime.strptime(str_date, "%d/%m/%Y %H:%M")

        except Exception as err:
            print("Error")
        else:
            dt_start = dt.datetime(dt_end.year,1,1,0,0)
            diff_seconds = (dt_end - dt_start).total_seconds()
            return diff_seconds




class moderationCommands(commands.Cog):

    def __init__(self,bot):
        self.bot = bot
        self.mutes.start()
        rootLogger.info("Модуль {} Включен".format(self.__class__.__name__))




    @tasks.loop(seconds=60.0)
    async def mutes(self):
        thisTime = datetime.now().strftime("%d/%m/%Y %H:%M")
        path = Path("mutes.json")
        userData = json.loads(path.read_text(encoding="utf-8"))

        if f"{thisTime}" in userData["mutes"]:
            guild = self.bot.get_guild(int(userData["mutes"][f"{thisTime}"]["guild"]))
            channel = self.bot.get_channel(int(takeSettings(guild.id, "mute_channel")))
            member = await guild.fetch_member(int(userData["mutes"][f"{thisTime}"]["user"]))
            embed = disnake.Embed(title="**Auto-Unmute SYSTEM**", color=disnake.Color.purple())
            embed.add_field(name= "**UnMute user**", value = f"{member.mention} unmuted by autoUnmute.")
            embed.set_footer(text=thisTime)
            await channel.send(embed=embed)
            await member.send(embed=embed)
            await member.remove_roles(disnake.utils.get(guild.roles, id = int(takeSettings(guild.id, "mute_role"))))
            with open("mute.json", "w") as file: 
                usersOtherData = userData.replace(userData[f"{thisTime}"], "")
                json.dump(usersOtherData, file, indent=7)
                file.close()
            rootLogger.info(f"Unmute {member.name}")
        



    @commands.slash_command(
        name="embed",
        description="Создание Embed сообщения")
    @commands.has_permissions(kick_members=True)
    async def embed_message(inter, title:str,  field_name:str, field_value:str):
        rootLogger.info(f"Create embed message by {inter.author.name} in channel {inter.channel.name}. Title: {title}, Field name: {field_name}, Field value: {field_value}. ")
        emb = disnake.Embed(title = title, color = disnake.Color.purple())
        emb.add_field(name = field_name, value = field_value, inline = False)
        emb.set_footer(text = f" Embed message by {inter.author.name}")
        emb.set_author(
    name="Aoyo",
    url="https://github.com/YaFlay",
    icon_url="https://cdn.discordapp.com/avatars/1036651201174970498/41d6da88e57399714186051e4767a36d.png?size=256",
)
        
        await inter.send(embed=emb)

    @commands.slash_command(
        name="mute",
        description="Мут")
    @commands.has_permissions(kick_members=True)
    async def add(self, inter, member: disnake.Member, amount: str, reason: str):
        mute_role = guild.get_role(id = int(takeSettings(inter.guild_id, "mute_role")))
        rootLogger.info(f"Mute {member.name} by moderator {inter.author.name}. Reason: {reason}. Amount: {amount}")
        path = Path("users/users.json")
        userData = json.loads(path.read_text(encoding="utf-8"))
        if f"{member.id}" not in userData["users"][f"{inter.guild_id}"]:
            newUserData = {
                f"{member.id}":{
                    "userID":member.id,
                    "warnCounter":0,
                    "muteCounter":1,
                    "userMention":f"{member.mention}",
                    "guild": f"{inter.guild_id}"
                },
            }
            userData["users"][f"{inter.guild_id}"].append(newUserData)
            path.write_text(json.dumps(userData, indent=7), encoding="utf-8", newline="\n")
        

        else:
            userData["users"][f"{inter.guild_id}"]["muteCounter"].replace(userData["users"][f"{inter.guild_id}"]["muteCounter"], (int(userData["users"][f"{inter.guild_id}"]["muteCounter"]) + 1))
        times_start = dt.datetime.today()
        times_start = times_start.strftime("%Y-%m-%d, %H:%M:%S")
        emb_user = disnake.Embed(title = "**Уведомление - Mute**", color = disnake.Color.purple())
        emb_user.add_field(name = "**Выдал:**", value = inter.author.mention, inline = False)
        emb_user.add_field(name = "**Причина:**", value = reason, inline = False)
        emb_user.add_field(name = "**Длительность:**", value = amount, inline = False)
        emb_user.add_field(name = "**Сервер:**", value = inter.guild.name, inline = False)
        emb_user.set_footer(text = f"Дата: {times_start}")
        emb_user.set_author(
    name="Aoyo",
    url="https://github.com/YaFlay",
    icon_url="https://cdn.discordapp.com/avatars/1036651201174970498/41d6da88e57399714186051e4767a36d.png?size=256",
)

        if member is None:
            emb = disnake.Embed(title = "[ERROR] Mute", description = f"{inter.author.mention}, Укажите пользователя!", color = disnake.Color.purple())
            emb.add_field(name = "Пример:", value = f"{inter.prefix}мьют [@участник] <время(с, м, ч, д)> [причина]", inline = False)
            emb.add_field(name = "Пример 1:", value = f"{inter.prefix}мьют @YaFlay 1ч пример")
            emb.add_field(name = "Время:", value = f"с - секунды\nм - минуты\nч - часы\nд - дни")
            emb.set_author(
    name="Aoyo",
    url="https://github.com/YaFlay",
    icon_url="https://cdn.discordapp.com/avatars/1036651201174970498/41d6da88e57399714186051e4767a36d.png?size=256",
)

            await inter.send(embed = emb)
        else:
            if amount:
                end_time = amount[-1:]
                time = int(amount[:-1])
                timeInt = amount[:-1]
                timeStr = amount.replace(timeInt, "")
                timeInt = int(timeInt)
                if time <= 0:
                    emb = disnake.Embed(title = "[ERROR] Mute", description = f"{inter.author.mention}, Время не может быть меньше 1!", color = disnake.Color.purple())
                    emb.add_field(name = "Пример:", value = f"{inter.prefix}мьют [@участник] <время> [причина]", inline = False)
                    emb.add_field(name = "Пример 1:", value = f"{inter.prefix}мьют @YaFlay 1ч пример")
                    emb.add_field(name = "Время:", value = f"м - минуты\nч - часы\nд - дни")

                    emb.set_author(
    name="Aoyo",
    url="https://github.com/YaFlay",
    icon_url="https://cdn.discordapp.com/avatars/1036651201174970498/41d6da88e57399714186051e4767a36d.png?size=256",
)

                    await inter.send(embed = emb)
                else:
                    if end_time == "м" or "m":

                            emb = disnake.Embed(title = f"**System - Mute**", color = disnake.Color.purple())
                            emb.add_field(name = "Выдал:", value = inter.author.mention, inline = False)
                            emb.add_field(name = "Нарушитель:", value = member.mention, inline = False)
                            emb.add_field(name = "ID нарушителя:", value = member.id, inline = False)
                            emb.add_field(name = "Причина:", value = reason, inline = False)
                            emb.add_field(name = "Длительность:", value = "{} минут".format(time))
                            emb.set_footer(text = f"Дата: {times_start}")
                            emb.set_author(
    name="Aoyo",
    url="https://github.com/YaFlay",
    icon_url="https://cdn.discordapp.com/avatars/1036651201174970498/41d6da88e57399714186051e4767a36d.png?size=256",
)

                            timesdelta = timedelta(minutes=timeInt)
                    elif end_time == "ч" or "h":

                                emb = disnake.Embed(title = f"**System - Mute**", color = disnake.Color.purple())
                                emb.add_field(name = "**Выдал:**", value = inter.author.mention, inline = False)
                                emb.add_field(name = "**Нарушитель:**", value = member.mention, inline = False)
                                emb.add_field(name = "**ID нарушителя:**", value = member.id, inline = False)
                                emb.add_field(name = "**Причина:**", value = reason, inline = False)
                                emb.add_field(name = "**Длительность:**", value = "{} час(ов)".format(time))
                                emb.set_footer(text = f"Дата: {times_start}")
                                emb.set_author(
    name="Aoyo",
    url="https://github.com/YaFlay",
    icon_url="https://cdn.discordapp.com/avatars/1036651201174970498/41d6da88e57399714186051e4767a36d.png?size=256",
)

                                timesdelta = timedelta(hours=timeInt)

                    elif end_time == "д" or "d":
                            emb = disnake.Embed(title = f"**System - Mute**", color = disnake.Color.purple())
                            emb.add_field(name = "**Выдал:**", value = inter.author.mention, inline = False)
                            emb.add_field(name = "**Нарушитель:**", value = member.mention, inline = False)
                            emb.add_field(name = "**ID нарушителя:**", value = member.id, inline = False)
                            emb.add_field(name = "**Причина:**", value = reason, inline = False)
                            emb.add_field(name = "**Длительность:**", value = "{} день(ей)".format(time), inline = False)
                            emb.set_footer(text = f"Дата: {times_start}")
                            emb.set_author(
    name="Aoyo",
    url="https://github.com/YaFlay",
    icon_url="https://cdn.discordapp.com/avatars/1036651201174970498/41d6da88e57399714186051e4767a36d.png?size=256",
)
                            timesdelta = timedelta(days = timeInt)
                    else:
                        await inter.response.send_message("Error", ephemeral=True)
                future_in_half_hour = datetime.now(timezone.utc) + timesdelta
                # Получение времени сейчас
                local_time = future_in_half_hour.astimezone().strftime("%d/%m/%Y %H:%M")
                path = Path("mutes.json")
                data = json.loads(path.read_text(encoding="utf-8"))
                newUserData = {
                    f"{local_time}":{
                        "user": f"{member.id}",
                        "guild": f"{inter.guild_id}"
                    },
                }
                data["mutes"].append(newUserData)
                path.write_text(json.dumps(data, indent=7), encoding="utf-8", newline="\n")
                rootLogger.info(f"User: {member.id} unmuted in {local_time}")
                channel = self.bot.get_channel(int(takeSettings(inter.guild_id, "mute_channel")))
                
                await inter.response.send_message("Done.", ephemeral=True)
                await member.add_roles(mute_role)
                await channel.send(embed = emb)
                await member.send(embed = emb_user)


    @commands.slash_command(
        name="deletechannel",
        description="Удаляет канал")
    @commands.has_permissions(manage_channels=True)
    async def changeChannel(inter):
        rootLogger.info(f"Deleting channel {inter.channel.name} by moderator {inter.author.name}")
        channel = bot.get_channel(inter.channel.id)
        category = disnake.utils.get(inter.guild.categories, id=809916621232799786)
        admin_role = disnake.utils.get(inter.guild.roles, id=810213578333224960)
        await channel.edit(
                name=f"del╵{inter.channel.name}",
                category=category,
                sync_permissions=True,
                reason=f"Delete channel. Moderator: {inter.author.name}")
        await channel.send(f"Channel removed. <@&810213578333224960>")
        await inter.response.send_message("Done.", ephemeral=True)

    @commands.slash_command(
        name="enableslowmode",
        description="Включает слоумод в канале")
    @commands.has_permissions(kick_members=True)
    async def enableslowmode(inter, amount: str):
        rootLogger.info(f"Enable slowmode in channel {inter.channel.name} by moderator {inter.author.name}")
        timeInt = amount[:-1]
        timeStr = amount[-1:]
        await inter.response.send_message("Done.", ephemeral=True)
        if timeStr in ["с", "s"]:
            await inter.channel.edit(slowmode_delay=timeInt)
        elif timeStr in ["м","m"]:
            await inter.channel.edit(slowmode_delay=[timeInt * 60])
        elif timeStr in ["h","ч"]:
            await inter.channel.edit(slowmode_delay=[timeInt * 60 * 60])
        else:
            await inter.send("Неправильно указано время, или иное")






    @commands.slash_command(
        name="permmute",
        description="Мут навсегда")
    @commands.has_permissions(kick_members=True)
    async def permmute(inter, member: disnake.Member, reason: str):
        times_start = datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
        rootLogger.info(f"Permanently muted user {member.name} by moderator {inter.author.name}. Reason: {reason}")
        channel = bot.get_channel(837053353812426752)
        mute_role = disnake.utils.get(inter.guild.roles, id = 882170431279349770)
        emb_user = disnake.Embed(title = "**Уведомление - Mute**", color = disnake.Color.purple())
        emb_user.add_field(name = "**Выдал:**", value = inter.author.mention, inline = False)
        emb_user.add_field(name = "**Причина:**", value = reason, inline = False)
        emb_user.add_field(name = "**Длительность:**", value="Перманентный", inline = False)
        emb_user.add_field(name = "**Сервер:**", value = inter.guild.name, inline = False)
        emb_user.set_footer(text = f"Дата: {times_start}")

        emb = disnake.Embed(title = f"**System - Mute**", color = disnake.Color.purple())
        emb.add_field(name = "**Выдал:**", value = inter.author.mention, inline = False)
        emb.add_field(name = "**Нарушитель:**", value = member.mention, inline = False)
        emb.add_field(name = "**ID нарушителя:**", value = member.id, inline = False)
        emb.add_field(name = "**Причина:**", value = reason, inline = False)
        emb.add_field(name = "**Длительность:**", value = "пермач", inline = False)
        emb.set_footer(text = f"Дата: {times_start}")
        await inter.response.send_message("Done.", ephemeral=True)
        await member.add_roles(mute_role)
        await channel.send(embed = emb)
        await member.send(embed = emb_user)



    @commands.slash_command(
        name="unmute",
        description="Размут")
    @commands.has_permissions(kick_members=True)
    async def unmute(inter, user:disnake.Member, reason):
        role = disnake.utils.get(inter.guild.roles, name="🔇  •  замучен!")
        rootLogger.info(f"Unmuted user {user.name} by moderator {inter.author.name}. Reason: {reason}")
        if role in user.roles:
            await user.remove_roles(role)

            await user.add_roles(role)
            embed = disnake.Embed(title="Размут", description=f"{user.mention} был размучен, причина: {reason}" , color = disnake.Color.purple())


            embed.add_field(name="Размучен модератором :" , value = f"{inter.author.mention}")

            await inter.response.send_message("Done.", ephemeral=True)
            await user.remove_roles(role)
            channel = bot.get_channel(837053353812426752)
            await channel.send(embed=embed)

        else:
            await inter.send("Неправильный аргумент, или пользователь не замучен")




def setup(bot):
    bot.add_cog(moderationCommands(bot))


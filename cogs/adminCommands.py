import disnake
from handlers import *
from disnake.ext import *
import datetime
from log import *
from pathlib import Path
class adminCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        rootLogger.info("Модуль {} подключен!".format(self.__class__.__name__))

    @commands.slash_command(
        name="addtask",
        description="Добавление задачи")
    async def voting(inter, member: disnake.Member, task: str, deadline: str):
        channel = bot.get_channel(int(takeSettings(inter.guild_id, "taskmanager_channel")))
        if deadline:
            times_start = datetime.datetime.today()
            embError = disnake.Embed(title="**Koshki.TaskManager[ERROR]**", colour=disnake.Color.purple())
            embError.add_field(name="**Ошибка!**", value="Вы неправильно указали дед-лайн!")
            embError.add_field(name="**Пример как надо:**", value="deadline:5д")
            embError.add_field(name="**Время:**", value="с/s - секунды \nм/m - минуты\nч/h - часы\nд/d - дни")
            end_time = deadline[-1:]
            time = int(deadline[:-1])
            if time <= 0:
                await ctx.send(embed=embError)
            else:
                if end_time in ["с","s"]:
                    time_end = datetime.timedelta(seconds=time)
                elif end_time in ["м","m"]:
                    time_end = datetime.timedelta(minutes=time)
                elif end_time in ["ч","h"]:
                    time_end = datetime.timedelta(hours=time)
                elif end_time in ["д","d"]:
                    time_end = datetime.timedelta(days=time)
                else: await inter.send(embed=embError)
        emb = disnake.Embed(title="**Koshki.TaskManager**", colour=disnake.Color.purple())
        emb.add_field(name=f"Задание для", value = f"{member.id}")
        emb.add_field(name=f"**Задача от {inter.author.name}**: ", value=task)
        emb.add_field(name="**Дедлайн**", value=time_end)
        emb.add_field(name=f"**Спрашивает:**", value=f"-")
        emb.set_footer(text = f'Дата: {times_start.strftime("%Y-%m-%d, %H:%M:%S")}')
        emb.set_author(
    name="Aoyo",
    url="https://github.com/YaFlay",
    icon_url="https://cdn.discordapp.com/avatars/1036651201174970498/41d6da88e57399714186051e4767a36d.png?size=256",
)

        buttons = disnake.ui.View()
        buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="checkmark", emoji="<:checkmark:905943731067305996>"))
        buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="deletesign", emoji="<:deletesign:905943741775368272>"))
        buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="question", emoji=f"❔"))
        await channel.send(content=member.mention, embed=emb, allowed_mentions=disnake.AllowedMentions(roles=True), view=buttons)
        await inter.response.send_message("Done.", ephemeral=True)
        
def setup(bot):
    bot.add_cog(adminCommands(bot))

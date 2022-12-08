import os, asyncio, log, datetime, random, disnake, sys, json
from disnake.utils import get
from disnake.ext import commands
from asyncio import sleep
from pysondb import db
from time import time
from log import rootLogger
from pathlib import Path


def takeSettings(guild_id, data):    
    path = Path("guilds/guilds.json")
    readedData = json.loads(path.read_text(encoding="utf-8"))
    pon = readedData["guilds"][f"{guild_id}"][f"{data}"]
    return pon 

TOKEN = 'ur token   '
main_path = __file__.replace(os.path.basename(__file__), "")
bot = commands.Bot(command_prefix="/", intents=disnake.Intents().all())
bot.remove_command("help")

now = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")

@bot.listen()
async def on_ready():
    status = [disnake.Status.online, disnake.Status.idle, disnake.Status.dnd]
    rootLogger.warning(f"{bot.user} is online and connected to Discord.")
    disnakeGameStatus = disnake.Game(name="Only slash commands! Author github: github.com/yaflay", type=4)
    for filename in os.listdir(f"{main_path}/cogs"):
        if filename.endswith(".py"):
            namefile = filename.replace(".py", '')
            bot.load_extension(f"cogs.{namefile}")
    i = 0
    while True:
        await bot.change_presence(status=status[i], activity=disnakeGameStatus)
        if i >= 2: i = 0
        i = i+1

        await sleep(30)


@bot.command(is_owner=True, pass_context=True, alias="reload")
async def reload(ctx):
    for filename in os.listdir(f"{main_path}/cogs"):
        if filename.endswith(".py"):
            namefile = filename.replace(".py", '')
            bot.reload_extension(f"cogs.{namefile}")
    await ctx.message.delete()

@bot.command( pass_context = True, alias="clear")
@commands.has_permissions(manage_messages=True)
async def clear( ctx, amount = 1 ):

    await ctx.channel.purge( limit = 1 )
    await ctx.channel.purge( limit = amount )

@bot.command(is_owner=True, alias='leave')
async def leave(ctx, arg):
    print(arg)
    await bot.get_guild(int(arg)).leave()

if __name__ != "__main__":
    try:
        bot.run(TOKEN)
    except ConnectionError as e:
        rootLogger.error(f"Time: {now}, Internet exception: {e}. Closing the process....")
        sys.exit()
    except Exception as e:
        rootLogger.error(f"Time: {now} Exception: {e}. Writing in file...")
        with open("logs/last_error.log", "a") as file:
            file.write(e)
            file.close()
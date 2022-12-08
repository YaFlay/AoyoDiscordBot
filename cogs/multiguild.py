from disnake import *
from disnake.ext import commands
from handlers import *
from os import path
from json import dump, dumps, loads
from log import rootLogger
import json
from pathlib import Path

class multiGuildSettings(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		rootLogger.info("Модуль {} подключен!".format(self.__class__.__name__))

	@commands.slash_command(
		name="settings",
		description="Настройка сервера(если вам это не надо, добавьте канал-заглушку.)")
	@commands.has_permissions(administrator=True)
	async def controlGuildSettings(inter, mute_role: disnake.Role, 
		mute_channel: disnake.TextChannel,
		guest_room: disnake.TextChannel,
		taskmanager_channel: disnake.TextChannel,
		on_join_role: disnake.Role):
		writedData={
		f"{inter.guild_id}":[{
				"mute_role": f"{mute_role.id}",
				"mute_channel": f"{mute_channel.id}",
				"lvl_alert_channel": f"None",
				"guest_room": f"{guest_room.id}",
				"taskmanager_channel": f"{taskmanager_channel.id}",
				"on_join_role": f"{on_join_role.id}"
			}],
		}
		path = Path("guilds/guilds.json")
		data = json.loads(path.read_text(encoding="utf-8"))
		data["guilds"].append(writedData)
		path.write_text(json.dumps(data, indent=7), encoding="utf-8", newline="\n")

		await inter.response.send_message("Done. Your server saved in bot`s settings!", ephemeral=True)


def setup(bot):
	bot.add_cog(multiGuildSettings(bot))
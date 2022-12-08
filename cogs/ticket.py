from disnake.ext import commands
from disnake import *
from handlers import *
from log import *
import json
from dislash import Option
import disnake
from pathlib import Path


class ticket(commands.Cog):
	def __init__(self,bot):
		self.bot = bot
		rootLogger.info(f"Модуль {self.__class__.__name__} подключен!")

	@commands.slash_command(
		name="create_ticket",
		description="Создание тикета для вашего сервера!")
	@commands.has_permissions(administrator=True)
	async def createTicket(inter, ticket_name: str, ticket_description: str, channel: disnake.TextChannel, channel_for_category: disnake.TextChannel=Option("channel_for_category",description="Отправьте канал, в категории которого надо создавать тикеты")):
		embed = disnake.Embed(title="**Ticket**", colour=disnake.Color.blue())
		embed.add_field(name=ticket_name, value=ticket_description)
		buttons = disnake.ui.View()
		buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="createTicket", label="Создать тикет"))
		writedData={
		f"{inter.guild_id}":{
			"category": f"{channel_for_category.category.id}",
			"guild": f"{inter.guild_id}"
			},
		}
		path = Path("tickets/ticket.json")
		data = json.loads(path.read_text(encoding="utf-8"))
		data["tickets"].append(writedData)
		path.write_text(json.dumps(data, indent=3), encoding="utf-8", newline="\n")
		await channel.send(embed=embed, view=buttons)
def setup(bot):
	bot.add_cog(ticket(bot))
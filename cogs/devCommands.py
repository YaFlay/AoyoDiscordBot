# devCommands.py
from handlers import *
from log import *
from disnake import *
from disnake.ext import *
import datetime

class devCommands(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		rootLogger.info(f'Модуль {self.__class__.__name__} подключен!')

	@commands.slash_command(
		name='addchangelog',
		description='Added task in changelog')
	@commands.has_any_role(912548559247798272, 1022256767658364968, 1022256972646580335)
	async def changelog(inter, changelog: str):
		time = datetime.datetime.now().strftime("%Y-%m-%d, %H:%M:%S")
		embed = disnake.Embed(colour = disnake.Colour.purple())
		embed.add_field(name=f'{inter.author.name} **добавил функцию**:', value=f'{changelog}')
		embed.set_footer(text=f'Time: {time}. Author: {inter.author.name}')
		await bot.get_channel(1030145406346219601).send(embed=embed)
		await inter.response.send_message('Done.', ephemeral=True)

def setup(bot):
	bot.add_cog(devCommands(bot))
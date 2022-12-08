from handlers import *
from disnake import *
from disnake.ext import *
from log import *

class giveroles(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		rootLogger.info("Модуль {} подключен!".format(self.__class__.__name__))

	@commands.slash_command(
		name = 'manager',
		description = 'Message for add manager')
	@commands.has_any_role(810213578333224960)
	async def manager(self, inter):
		
		embedFirst = disnake.Embed(colour=disnake.Colour.from_rgb(47, 49, 54))
		embedFirst.set_image('https://media.discordapp.net/attachments/797411622313263104/980180573408595988/Frame_281.png')

		embedSecond = disnake.Embed(description='📘 Вы можете заполнить заявку на одну из должностей и присоединиться к нашей команде, сделать это можно нажав на `кнопку` снизу.\n\nПосле рассмотрения заявки вам отпишут в личные сообщения и объяснят основную информацию о работе.\n\nУчтите, что вы должны ответственно подходить к заполнению заявки и последующей работе. Возможно работа будет занимать у вас свободное время, будьте готовы к этому.\n\n💗 *Мы ждём тебя на стажировке!* ', colour=disnake.Colour.from_rgb(47, 49, 54))
		embedSecond.set_image('https://media.discordapp.net/attachments/876280751488909332/979778066417070151/Frame_280.png?width=1440&height=4')
		
		embedThird = disnake.Embed(description='<@&781297818353926154> - Самая простая в модерации сервера должность. На ней вы обязаны показать себя как можно лучше, чтобы в будущем вас повысили!\n<@&860472730012483584>  - должность на которой вам нужно будет работать с другими серверами и договариваться о взаимном пиаре, для рекламы нашего сервера.\n <@&1034193316163633172> - не самая простая должность, на который вы должны будете выложиться на все сто, что бы вас повысили! Вы будете писать код, либо же помогать писать его вышестоящим по званию программистам. ', colour=disnake.Colour.from_rgb(47, 49, 54))
		embedThird.set_image('https://media.discordapp.net/attachments/876280751488909332/979778066417070151/Frame_280.png?width=1440&height=4')

		buttons = disnake.ui.View()
		buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="moderationButton", emoji="✏️", label='мяудератор'))
		buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="managerButton", emoji="✏️", label='мяунеджер'))
		buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="coderButton", emoji="✏️", label='мяудев'))
		await inter.response.send_message('Done', ephemeral=True)
		await self.bot.get_channel(979848267791753236).send(embeds=[embedFirst, embedSecond, embedThird], view=buttons)


def setup(bot):
	bot.add_cog(giveroles(bot))
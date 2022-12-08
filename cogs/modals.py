# modals.py
from handlers import *
from log import rootLogger
from disnake import *
from disnake.ext import *

class modals(commands.Cog):
	def __init__(self, bot):
		self.bot = bot
		rootLogger.info(f'Модуль {self.__class__.__name__} включен!')
	class renamePrivateRoom(disnake.ui.Modal):
		def __init__(self):
			components = [
			disnake.ui.TextInput(
				label='Новое название канала:',
				placeholder="Я люблю нюхать бебру",
				custom_id='newNamePrivateRoom',
				style=TextInputStyle.short,
				)]
			super().__init__(
				title='Изменение приватного канала',
				custom_id='renamePrivateRoom',
				components=components,
				)
	class setUserLimit(disnake.ui.Modal):
		def __init__(self):
			components = [
			disnake.ui.TextInput(
				label='Новое максимальное кол-во пользователей:',
				placeholder="99",
				custom_id='newUserLimit',
				style=TextInputStyle.short,
				max_length=2
				)]
			super().__init__(
				title='Изменение приватного канала',
				custom_id='setUserLimit',
				components=components,
				)
	class programmistModal(disnake.ui.Modal):
		def __init__(self):
			components = [
			disnake.ui.TextInput(
				label='Ваш возраст:',
				placeholder="18",
				custom_id='age',
				style=TextInputStyle.short,
				max_length=3,
				),
			disnake.ui.TextInput(
				label='Язык, который вы знаете:',
				placeholder='Python',
				custom_id='Language',
				style=TextInputStyle.short,
				max_length=10,
				),
			disnake.ui.TextInput(
				label='Ссылка на ваш гитхаб:',
				placeholder='https://github.com/YaFlay',
				custom_id='Github',
				style=TextInputStyle.short,
				max_length=40,
				),
			disnake.ui.TextInput(
				label='Грамотность в плане кода:',
				placeholder='99/100',
				custom_id='codeLiteracy',
				style=TextInputStyle.short,
				max_length=10,
				),
			]
			super().__init__(
				title='Заявка в программисты',
				custom_id='CodersModal',
				components=components,
				)

	class managerModal(disnake.ui.Modal):
	    def __init__(self):
	        # The details of the modal, and its components
	        components = [
	            disnake.ui.TextInput(
	                label="Ваш возраст:",
	                placeholder="18",
	                custom_id="age",
	                style=TextInputStyle.short,
	                max_length=2,
	            ),
	            disnake.ui.TextInput(
	                label="Насколько вы знаете правила сервера:",
	                placeholder="99 / 100",
	                custom_id="rules",
	                style=TextInputStyle.short,
	                max_length=10
	            ),
	            disnake.ui.TextInput(
	                label="Был ли у вас опыт в данной сфере",
	                placeholder="да / нет",
	                custom_id="xp",
	                style=TextInputStyle.short,
	                max_length=10
	            ),
	            disnake.ui.TextInput(
	                label="Как вы оцениваете свою грамотность?",
	                placeholder="99 / 100",
	                custom_id="literacy",
	                style=TextInputStyle.short,
	                max_length=10
	            ),
	        ]
	        super().__init__(
	            title="Заявка в менеджеры",
	            custom_id="managerModal",
	            components=components,
	        )


	class helperModal(disnake.ui.Modal):
	    def __init__(self):
	        # The details of the modal, and its components
	        components = [
	            disnake.ui.TextInput(
	                label="Ваш возраст:",
	                placeholder="18",
	                custom_id="ВОЗРАСТ",
	                style=TextInputStyle.short,
	                max_length=2,
	            ),
	            disnake.ui.TextInput(
	                label="Насколько вы знаете правила сервера:",
	                placeholder="99 / 100",
	                custom_id="ЗНАНИЯ ПРАВИЛ",
	                style=TextInputStyle.short,
	                max_length=10
	            ),
	            disnake.ui.TextInput(
	                label="Был ли у вас опыт в данной сфере",
	                placeholder="да / нет",
	                custom_id="ОПЫТ",
	                style=TextInputStyle.short,
	                max_length=10
	            ),
	            disnake.ui.TextInput(
	                label="Как вы оцениваете свою грамотность?",
	                placeholder="99 / 100",
	                custom_id="ГРАМОТНОСТЬ",
	                style=TextInputStyle.short,
	                max_length=10
	            ),
	        ]
	        super().__init__(
	            title="Заявка в хелперы",
	            custom_id="helperModal",
	            components=components,
	        )
	@bot.event
	async def on_modal_submit(inter: disnake.ModalInteraction):
		if inter.custom_id in ['helperModal', 'managerModal', 'CodersModal']:
			if inter.custom_id == 'helperModal': modalName = 'хелперы'; channel = bot.get_channel(979847249716707368)
			elif inter.custom_id == 'managerModal': modalName = 'менеджеры'; channel = bot.get_channel(980176067279085668)
			elif inter.custom_id == 'CodersModal': modalName = 'программисты'; channel = bot.get_channel(1034188859921141851)
			embed = disnake.Embed()
			for key, value in inter.text_values.items():
				embed.add_field(
					name=key.capitalize(),
					value=value[:1024],
					inline=False,
				)
			embed.set_footer(text=inter.author.id)
			buttons = disnake.ui.View()
			buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="modalcheckmark", emoji="<:checkmark:905943731067305996>"))
			buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="modaldeletesign", emoji="<:deletesign:905943741775368272>"))
			await inter.response.send_message('Заявка подана.', ephemeral=True)
			await channel.send(embed=embed, view=buttons)
		elif inter.custom_id in ['renamePrivateRoom', 'setUserLimit']:
			if inter.custom_id == 'renamePrivateRoom':
				for key, value in inter.text_values.items():
					if key == 'newNamePrivateRoom':
						await bot.get_channel(inter.channel_id).edit(name=value[:1024])
			if inter.custom_id == 'setUserLimit':
				for key, value in inter.text_values.items():
					if key == 'newUserLimit':
						await bot.get_channel(inter.channel_id).edit(user_limit=int(value[:1024]))
			await inter.response.send_message('Готово!', ephemeral=True)
		pass

def setup(bot):
	bot.add_cog(modals(bot))
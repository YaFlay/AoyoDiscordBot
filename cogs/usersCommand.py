from disnake.ext import commands
import disnake
from handlers import *
from log import *
class usersCommand(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        rootLogger.info("Модуль {} подключен!".format(self.__class__.__name__))

    @commands.slash_command(
        name="invite",
        description="Создает ссылку для приглашения")
    async def invite(ctx):
            guilInviteId = bot.get_guild(ctx.guild.id)
            link = await guilInviteId.text_channels[0].create_invite()
            await ctx.send(f'{link} ваша ссылка!')

    @commands.slash_command(
        name='invitebot',
        description='Пригласить бота к себе на сервер')
    async def invitebot(inter):
        await inter.response.send_message('https://discord.com/api/oauth2/authorize?client_id=979671843264938045&permissions=8&scope=bot', ephemeral=True)


def setup(bot):
    bot.add_cog(usersCommand(bot))

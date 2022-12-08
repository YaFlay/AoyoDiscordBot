from disnake.ext import commands
import disnake
from handlers import *
from log import *
class sellerCommands(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        rootLogger.info("Модуль {} подключен!".format(self.__class__.__name__))


    @commands.slash_command(
        name="giveaway",
        description="Розыгрыш")
    @commands.has_role("Koshki.seller")
    async def giveaway(ctx):
        # Giveaway command requires the user to have a "Giveaway Host" role to function properly

        # Stores the questions that the bot will ask the user to answer in the channel that the command was made
        # Stores the answers for those questions in a different list
        giveaway_questions = ['Пиши что хочешь', 'Какой приз?', 'Как долго будет длиться (в секундах)?',]
        giveaway_answers = []

        # Checking to be sure the author is the one who answered and in which channel
        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        # Askes the questions from the giveaway_questions list 1 by 1
        # Times out if the host doesn't answer within 30 seconds
        for question in giveaway_questions:
            await ctx.send(question)
            try:
                message = await bot.wait_for('message', timeout= 30.0, check= check)
            except asyncio.TimeoutError:
                await ctx.send('Ты не ответил вовремя. Спроси заново через 30 секунд.')
                return
            else:
                giveaway_answers.append(message.content)

        # Grabbing the channel id from the giveaway_questions list and formatting is properly
        # Displays an exception message if the host fails to mention the channel correctly
        try:
            c_id = giveaway_answers[0][2:-1]
        except:
            await ctx.send(f'Ошибка 167(WRONG CHANNEL)')
            return

        # Storing the variables needed to run the rest of the commands
        channel = bot.get_channel(1022897510156599436)
        prize = str(giveaway_answers[1])
        time = int(giveaway_answers[2])

        # Sends a message to let the host know that the giveaway was started properly

        # Giveaway embed message
        give = disnake.Embed(color = disnake.Color.blue())
        give.set_author(name = f'Розыгрыш!!', icon_url = 'https://i.imgur.com/VaX0pfM.png')
        give.add_field(name= f'{ctx.author.name} разыгрывает: {prize}!', value = f'Нажми на  🎉 чтоб участвовать!\n Закончится розыгрш через {round(time/60, 2)} минут!', inline = False)
        end = datetime.datetime.utcnow() + datetime.timedelta(seconds = time)
        give.set_footer(text = f'Розыгрыш закончится {end} UTC!')
        my_message = await channel.send(embed = give)

        # Reacts to the message
        await my_message.add_reaction("🎉")
        await asyncio.sleep(time)

        new_message = await channel.fetch_message(my_message.id)

        # Picks a winner
        users = await new_message.reactions[0].users().flatten()
        users.pop(users.index(bot.user))
        winner = random.choice(users)

        # Announces the winner
        winning_announcement = disnake.Embed(color = disnake.Color.blue())
        winning_announcement.set_author(name = f'Розыгрыш закончен!', icon_url= 'https://i.imgur.com/DDric14.png')
        winning_announcement.add_field(name = f'🎉 Приз: {prize}', value = f'🥳 **Победитель**: {winner.mention}\n 🎫 **Количество участвовающих**: {len(users)}', inline = False)
        winning_announcement.set_footer(text = 'Спасибо за участие!')
        await channel.send(embed = winning_announcement)

def setup(bot):
    bot.add_cog(sellerCommands(bot))

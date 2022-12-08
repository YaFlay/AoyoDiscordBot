from disnake.ext import commands
from disnake import *
import disnake
from handlers import *
from log import *
from cogs.modals import *
from random import randint
from pathlib import Path

class events(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        rootLogger.info("Модуль {} подключен!".format(self.__class__.__name__))

    @bot.event
    async def on_command_error(ctx, error):
        rootLogger.error(f"Error {error}")
        channel = bot.get_channel(1026134775368515655)
        await channel.send(error)
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("У вас недостаточно прав для выполнения этой команды")
        pass



    @bot.event
    async def on_member_join(member):
        if member.id != 979671843264938045:
            userCounter = member.guild
            joinMember = member.joined_at
            userMention = member.mention
            userID = member.id
            isBot = member.bot
            userNick = member.name
            memberTopRole = member.top_role
            onJoinRole = disnake.utils.get(member.guild.roles, id = int(takeSettings(member.guild.id, "on_join_role")))
            channelGuestRoom = bot.get_channel(int(takeSettings(member.guild.id, "guest_room")))
            emb = disnake.Embed(title=f":cat:**Привет, {member.name}!**", description=f"<#783510578454069249> - базовая информация о сервере!", colour=disnake.Colour.from_rgb(47, 49, 54))
            emb.set_image(url="https://media.discordapp.net/attachments/797411622313263104/978301653633601546/Frame_249_.png")
            await channelGuestRoom.send(member.mention,embed=emb)
            await member.add_roles(onJoinRole)
            userData = {
                f"{userID}":{
                "userID":member.id,
                "warnCounter":0,
                "muteCounter":1,
                "userMention":f"{member.mention}",
                "guild":f"{member.guild.id}"
                }
            }

            path = Path("users/users.json")
            data = json.loads(path.read_text(encoding="utf-8"))
            data[f"{member.guild_id}"].append(userData)
            path.write_text(json.dumps(data, indent=7), encoding="utf-8", newline="\n")
        elif member.id == 979671843264938045:
            if member.guild.system_channel is not None:
                channel = member.guild.system_channel
            elif member.guild.public_updates_channel is not None:
                channel = member.guild.public_updates_channel
            pass
            embed = disnake.Embed(title="**Aoyo приветствие**", description="Для того, что бы настроить бота, используйте команду settings", color=disnake.Colors.orange)
            await channel.send(embed=embed)
        pass

            

    @bot.event
    async def on_member_remove(member):
        channelGuestRoom = bot.get_channel(int(takeSettings(member.guild.id, "guest_room")))
        emb = disnake.Embed(title=f"😿 **Пока-пока, {member.name}!**", colour=disnake.Colour.from_rgb(47, 49, 54))
        emb.set_image(url="https://media.discordapp.net/attachments/797411622313263104/978301653356785714/Frame_248_.png")
        emb.set_footer(text="Ждем тебя снова!")
        await channelGuestRoom.send(embed=emb)

    @bot.event
    async def on_voice_state_update(member, before, after):
        if after.channel and after.channel != before.channel:
            if after.channel.name != f"{member.name}`s voice channel":
                guild = bot.get_guild(member.guild.id)
                if after.channel.name in ["[+] СОЗДАТЬ", "[+]СОЗДАТЬ"]: 
                    category = disnake.utils.get(guild.categories, id=after.channel.category.id)
                    for channel in guild.channels:
                        if channel.name == f"{member.name}`s voice channel":
                            await member.edit(voice_channel=channel)

                            return
                    if member.voice.channel.name != f"{member.name}`s voice channel":
                        await member.edit(voice_channel=await guild.create_voice_channel(name=f"{member.name}`s voice channel", category=category))
                    embed = disnake.Embed(title = "**Управление приватными комнатами**", description="Вы можете изменить конфигурацию своей комнаты с помощью кнопок ниже.", colour=disnake.Colour.from_rgb(47, 49, 54))
                    embed.add_field(name="Переименовать приватную комнату:", value="✏️")
                    embed.add_field(name="Задать лимит участников приватной комнаты:", value="👥")
                    embed.add_field(name="Закрыть/Открыть приватную комнату:", value="🔒")
                    embed.add_field(name="Скрыть/Открыть приватную комнату:", value="👀")
                    buttons = disnake.ui.View()
                    buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="renamePrivateRoom", emoji="✏"))
                    buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="setUsersLimit", emoji="👥"))
                    buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="closePrivateRoom", emoji=f"🔒"))
                    buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="hidePrivateRoom", emoji=f"👀"))
                    await bot.get_channel(member.voice.channel.id).send(embed = embed, view = buttons)

        elif before.channel and after.channel != before.channel:
            if before.channel.name == f"{member.name}`s voice channel":
                await before.channel.delete()
            elif before.channel.name not in ["[+] СОЗДАТЬ", "[+]СОЗДАТЬ"]:
                print(before.channel.members)
                if before.channel.members == []:
                    await before.channel.delete()
            pass


    @bot.event
    async def on_button_click(inter: disnake.MessageInteraction):
        component_id = inter.component.custom_id
        if component_id in ["checkmark", "deletesign", "question", "modalcheckmark", "modaldeletesign"]:
            embedMessage = inter.message.embeds[0]
            guild = bot.get_guild(inter.guild.id)
            message = await bot.get_channel(inter.channel.id).fetch_message(inter.message.id)
            if component_id in ["checkmark", "deletesign", "question"]:
                userMentionField = int(embedMessage.fields[0].value)
                embedMessage.remove_field(index=3)
                if component_id in ["checkmark", "deletesign"]:
                    embedMessage.remove_field(index=2)
            
            if component_id == "checkmark":
                if inter.author.id == userMentionField:
                    embedMessage.add_field(name="**Выполнено**:",value=f"{inter.author.mention}")
                    await message.edit(embed=embedMessage, view=None)
            elif component_id == "deletesign":
                if inter.user.id == userMentionField:
                    embedMessage.add_field(name="**Отказано**:",value=f"{inter.author.mention}")
                    await message.edit(embed=embedMessage, view=None)
            elif component_id == "question":
                await message.create_thread( name="Ask a question", auto_archive_duration=60)
                embedMessage.add_field(name=f"**Спрашивает:**", value=f"{inter.author.mention}")
                await bot.get_channel(inter.message.id).send(f"Спрашивайте, {inter.author.mention}")
                await message.edit(embed=embedMessage)
        elif component_id == "modalcheckmark":
            member = await guild.fetch_member(int(embedMessage.footer.text))
            if inter.channel.id == 979847249716707368:
                await member.add_roles(disnake.utils.get(guild.roles, id = 781297818353926154))
                squadName = "хелпер"
            elif inter.channel.id == 980176067279085668:
                await member.add_roles(disnake.utils.get(guild.roles, id = 860472730012483584))
                squadName = "мяунеджер"
            elif inter.channel.id == 1034188859921141851:
                await member.add_roles(disnake.utils.get(guild.roles, id = 1034193316163633172))
                squadName = "программист"
            await member.send(f"Теперь вы {squadName}!")
            await message.edit(view=None)
            await inter.send("Добавил роль.", ephemeral=True)

        elif component_id == "modaldeletesign":
            await inter.message.delete()
            await inter.send_message("Удалено")

        elif component_id == "createTicket":
            embed = disnake.Embed(title="Управление тикетом", description="Если вы готовы завершить тикет, нажмите ниже.", colour=disnake.Color.blue())
            buttons = disnake.ui.View()
            buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="closeTicket", label="Закрыть тикет"))

            path = Path("tickets/tickets.json")
            fromJsonData = json.loads(path.read_text(encoding="utf-8"))

            member = inter.author
            guild = bot.get_guild(int(fromJsonData["tickets"][f"{inter.guild_id}"]["guild"]))
            category = disnake.utils.get(guild.categories, id=int(fromJsonData["tickets"][f"{inter.guild_id}"]["category"]))
            role = guild.get_role(int(takeSettings(inter.guild.id, "on_join_role")))
            
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(view_channel=False),
                role: disnake.PermissionOverwrite(view_channel=False),
                member: disnake.PermissionOverwrite(view_channel=True)
            }
            channel = await guild.create_text_channel(name=f"ticket-{randint(0,1000)}", category=category, overwrites=overwrites)
            await channel.send(content=inter.author.mention,embed=embed, view=buttons)

        elif component_id == "closeTicket":
            embed = disnake.Embed(title="Подтверждение", description=f"Вы уверены, что хотите закрыть тикет, {inter.author.name}?")
            buttons = disnake.ui.View()
            buttons.add_item(disnake.ui.Button(style=disnake.ButtonStyle.secondary, custom_id="closeTicketPerm", label="Да, закрыть тикет"))
            await inter.response.send_message(embed=embed, view=buttons)

        elif component_id == "closeTicketPerm":
            await bot.get_channel(inter.channel.id).delete(reason="Close ticket")
        
        elif component_id == "closePrivateRoom": 
            guild = bot.get_guild(inter.guild_id)
            role = guild.get_role(int(takeSettings(inter.guild.id, "on_join_role")))
            member = inter.author
            print(str(inter.channel.permissions_for(role)))
            if inter.channel.permissions_for(role):
                overwrites = {
                    guild.default_role: disnake.PermissionOverwrite(connect=False),
                    role: disnake.PermissionOverwrite(connect=False),
                    member: disnake.PermissionOverwrite(connect=True)
                }
                await bot.get_channel(inter.channel.id).edit(overwrites=overwrites)
                await inter.response.send_message("Готово.", ephemeral=True)          
        elif component_id == "hidePrivateRoom":
            guild = bot.get_guild(inter.guild.id)
            role = guild.get_role(int(takeSettings(inter.guild_id, "on_join_role")))
            member = inter.author
            overwrites = {
                guild.default_role: disnake.PermissionOverwrite(view_channel=False),
                role: disnake.PermissionOverwrite(view_channel=False),
                member: disnake.PermissionOverwrite(view_channel=True)
            }
            await bot.get_channel(inter.channel.id).edit(overwrites=overwrites)
            await inter.response.send_message("Готово.", ephemeral=True)          


        elif component_id == "renamePrivateRoom": await inter.response.send_modal(modal=modals.renamePrivateRoom())
        elif component_id == "setUsersLimit": await inter.response.send_modal(modal=modals.setUserLimit())
        
        elif component_id == "moderationButton" : await inter.response.send_modal(modal=modals.helperModal())
        elif component_id == "managerButton" : await inter.response.send_modal(modal=modals.managerModal())
        elif component_id == "coderButton" : await inter.response.send_modal(modal=modals.programmistModal())
       
        else: await inter.response.send_message("Неизвестная команда.", ephemeral=True)



    
def setup(bot):
    bot.add_cog(events(bot))

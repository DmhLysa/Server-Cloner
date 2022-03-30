import discord
from pystyle import *
import os

client = discord.Client()
token = Write.Input('Entrez votre token discord : \n', Colors.blue_to_purple, interval=0)
os.system("cls" or "clear")

class ServerCloner:
    def __init__(self, client: discord.Client, i_guild: discord.Guild, o_guild: discord.Guild):
        self.created_map = {}
        self.client = client
        self.input_guild = i_guild
        self.output_guild = o_guild
    
    async def clear_server(self):
        Write.Print('J ai commencer le clear de ton serveur.\n', Colors.blue_to_purple, interval=0)
        Write.Print('Current Stage: Roles\n', Colors.blue_to_purple, interval=0)
        for role in self.output_guild.roles:
            try:
                await role.delete()
                Write.Print(f'Role supprime {str(role.id)}.\n', Colors.blue_to_purple, interval=0)
            except:
                Write.Print(f'Je n ai pas reussi a supprimer un role : {str(role.id)}.\n', Colors.blue_to_purple, interval=0)
                continue

        Write.Print("Tous les roles ont ete supprime\n", Colors.red, interval=0)

        for channel in self.output_guild.channels:
            try:
                await channel.delete()
                Write.Print(f'Salon supprime {str(channel.id)}.\n', Colors.purple_to_blue, interval=0)
            except:
                Write.Print(f'Je n ai pas reussi a supprimer un salon : {str(channel.id)}.\n', Colors.purple_to_blue, interval=0)

        Write.Print("Clear fini\n", Colors.red, interval=0)
        
    async def create_roles(self):
        server_roles = []
        for role in self.input_guild.roles:
            server_roles.insert(0, role)

        for role in server_roles:
            new_role = await self.output_guild.create_role(name=role.name, permissions=role.permissions, colour=role.colour, hoist=role.hoist, mentionable=role.mentionable)
            Write.Print(f'Role cree : {str(new_role.id)}\n', Colors.green_to_red, interval=0)
    
    async def create_categories(self):
        
        for category in self.input_guild.categories:
            overwrites_to = {}
            for key, value in category.overwrites.items():
                role = discord.utils.get(self.input_guild.roles, name=key.name)
                overwrites_to[role] = value
            new_category = await self.output_guild.create_category_channel(
                name=category.name, overwrites=overwrites_to
            )
            await new_category.edit(
                position=int(category.position), nsfw=category.is_nsfw()
            )
            Write.Print(f'Categorie cree : {str(new_category.id)}\n', Colors.green_to_blue, interval=0)
            self.created_map[str(category.id)] = new_category.id
    
    async def create_text_channels(self):
        for channel in self.input_guild.text_channels:
            overwrites_to = {}
            for key, value in channel.overwrites.items():
                    role = discord.utils.get(self.input_guild.roles, name=key.name)
                    overwrites_to[role] = value
            if channel.category_id is not None:
                new_category_id = self.created_map.get(str(channel.category_id))

                new_category = await self.client.fetch_channel(int(new_category_id))
                new_channel = await new_category.create_text_channel(
                    name=channel.name, topic=channel.topic, position=channel.position, slowmode_delay=channel.slowmode_delay, 
                    nsfw=channel.is_nsfw(), overwrites=overwrites_to
                )
                Write.Print(f'channel cree {str(new_channel.id)}.\n', Colors.green_to_cyan, interval=0)
            else:
                new_channel = await self.output_guild.create_text_channel(name=channel.name, topic=channel.topic, position=channel.position,
                                                slowmode_delay=channel.slowmode_delay, nsfw=channel.is_nsfw(),
                                                overwrites=overwrites_to)
                Write.Print(f'channel cree {str(new_channel.id)}.\n', Colors.green_to_cyan, interval=0)

    async def create_voice_channels(self):
        for channel in self.input_guild.voice_channels:
            overwrites_to = {}
            for key, value in channel.overwrites.items():
                    role = discord.utils.get(self.input_guild.roles, name=key.name)
                    overwrites_to[role] = value
            if channel.category_id is not None:
                new_category_id = self.created_map.get(str(channel.category_id))
                new_category = await self.client.fetch_channel(int(new_category_id))
                new_channel = await new_category.create_voice_channel(name=channel.name, position=channel.position,
                                                    user_limit=channel.user_limit, overwrites=overwrites_to)
                Write.Print(f'channel cree {str(new_channel.id)}.\n', Colors.green_to_white, interval=0)
            else:
                new_channel = await self.output_guild.create_voice_channel(name=channel.name, position=channel.position,
                                                 user_limit=channel.user_limit, overwrites=overwrites_to)
                Write.Print(f'channel cree {str(new_channel.id)}.\n', Colors.green_to_cyan, interval=0)

    async def start(self):
        not_finished = True
        while not_finished:
            await self.clear_server()    
            await self.create_roles()
            await self.create_categories()
            await self.create_text_channels()
            await self.create_voice_channels()
            not_finished = False

Write.Print("Je commence le clonage\n", Colors.green_to_red, interval=0)

async def start_cloning():
    i_guild = client.get_guild(int(Write.Input("Entre l ID du discord que tu veux cloner : \n", Colors.green_to_red, interval=0)))
    o_guild = client.get_guild(int(Write.Input("Entre l ID du discord ou tu veux coller le clone : \n", Colors.green_to_red, interval=0)))

    cloner = ServerCloner(client, i_guild, o_guild)
    await cloner.start()
    Write.Print('Clonage fini \n', Colors.green_to_red, interval=0)
    Write.Input('Appuies sur entrer pour fermer la fenetre', Colors.green_to_red, interval=0)

@client.event
async def on_ready():
    await start_cloning()

client.run(token, bot=False)


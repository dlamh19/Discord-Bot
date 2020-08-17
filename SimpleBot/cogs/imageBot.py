import aiohttp
import discord
from discord.ext import commands, tasks


class imageBot(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print("ImageBot is online!")

    @commands.command()
    async def dog(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://random.dog/woof.json") as r:
                    data = await r.json()
                    embed = discord.Embed(title = "Woof")
                    embed.set_image(url = data['url'])
                    embed.set_footer(text = "http://random.dog")

                    await ctx.send(embed = embed)
    
    @commands.command()
    async def fox(self, ctx):
        async with ctx.channel.typing():
            async with aiohttp.ClientSession() as cs:
                async with cs.get("http://randomfox.ca/floof") as r:
                    data = await r.json()
                    embed = discord.Embed(title = "Awooo")
                    embed.set_image(url = data['image'])
                    embed.set_footer(text = "http://randomfox.ca")

                    await ctx.send(embed = embed)

def setup(client):
    client.add_cog(imageBot(client))

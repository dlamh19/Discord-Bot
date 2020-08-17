import discord

from discord.ext import commands, tasks
from itertools import cycle


client = commands.Bot(command_prefix = "!")

status = cycle(['Panda Happy', 'Panda Sad', 'Panda Mad'])

# Prints when the Bot is Ready/On
# Changes Status of Bot
@client.event
async def on_ready():
    #await client.change_presence(status=discord.Status.online, activity=discord.Game("Panda is here!"))
    change_status.start() # starts the loop for presence
    print("Bot is ready!")

@tasks.loop(seconds = 120)
async def change_status():
    await client.change_presence(activity = discord.Game(next(status)))

# displays in the terminal if a user joined the server
@client.event
async def on_member_join(member):
    print(f"{member} has joined the server")


# displays in the terminal if a user joined the server
@client.event
async def on_member_remove(member):
    print(f"{member} has left the server")

@client.event
async def on_command_error(ctx, error):
    #Checks if the command used has the right arguments passed in
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please pass in all required arguments.')

    #Checks if the user uses a command that DNE
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Invalid Command.')

@client.command(aliases=["kick", "Kick"])
async def _kick(ctx, member: discord.Member, *, reason=None):
    await member.kick(reason=reason)
    await ctx.channel.send(f"Kicked {member.mention} because {reason}")


@client.command(aliases=["ban", "Ban"])
@commands.has_permissions(ban_members = True)
async def _ban(ctx, member: discord.Member, *, reason=None):
    await member.ban(reason=reason)
    await ctx.channel.send(f"Banned {member.mention} because {reason}")


# unbans a user
@client.command()
async def unban(ctx, *, member):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split("#")

    # checks every ban entry inside the list
    for ban_entry in banned_users:
        user = ban_entry.user

        # checks if the users name and discriminator is the same as the member unban
        if (user.name, user.discrimnator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.channel.send(f"Unbanned {user.mention}")
            return

#clears amount # of messages
@client.command()
@commands.has_permissions(manage_messages = True)
async def clear(ctx, amount:int):
    await ctx.channel.purge(limit = amount)

@clear.error
async def clear_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send('Please specify an amount of messages to delete.')

@client.command(aliases=["Panda", "panda"])
async def _Panda(ctx):
    await ctx.channel.send("Hi Cutie!")
    
@client.command(aliases=["stinky", "Stinky"])
async def _Stinky(ctx):
    await ctx.channel.send("No, you STINKY!")

client.load_extension("cogs.musicBot")
client.load_extension("cogs.imageBot")
client.run("NzM3Mzk1NDYwMDc1MDI4NTgw.Xx8vCQ.P_6MzUp2FuKb8KvYYpP5Y6V3tC4")
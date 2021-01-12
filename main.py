from discord.ext import commands
import os
from dotenv import load_dotenv
from keep_alive import keep_alive

client = commands.Bot(command_prefix='^')

load_dotenv()

@client.command()
async def load(ctx, extension):
    client.load_extension(f'cogs.{extension}')
    await ctx.send('Loaded Cog '+extension)


@client.command()
async def unload(ctx, extension):
    client.unload_extension(f'cogs.{extension}')
    await ctx.send('Unloaded Cog '+extension)


for filename in os.listdir('./cogs'):
    if filename.endswith('.py'):
        client.load_extension(f'cogs.{filename[:-3]}')

keep_alive()
client.run(os.getenv("DISCORD_BOT_SECRET"))

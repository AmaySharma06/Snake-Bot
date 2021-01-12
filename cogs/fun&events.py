import discord
from discord.ext import commands,tasks
from random import choice, randrange
import praw
import os,json
from dotenv import load_dotenv
from itertools import cycle


def randcolor():
    col = [
        discord.Colour.dark_blue(),
        discord.Colour.blurple(),
        discord.Colour.dark_green(),
        discord.Colour.dark_orange(),
        discord.Colour.green(),
        discord.Colour.dark_red(),
        discord.Colour.dark_teal()
    ]
    a = choice(col)
    return a

load_dotenv()
class Reddit:
    reddit = praw.Reddit(
      client_id=os.getenv("client_id"),
      client_secret=os.getenv("client_secret"),
      username=os.getenv("username"),
      password=os.getenv("password"),
      user_agent="python"
    )

    subr_meme = reddit.subreddit('memes')
    subr_joke = reddit.subreddit('jokes')

    memes = []
    jokes = []
    memes_used = []
    jokes_used = []


class Fun(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.command()
    async def meme(self, ctx):
        if ctx.channel.id == 777079599505997844:
            a = randcolor()
            while True:
                rand = randrange(0, len(Reddit.memes))
                if rand not in Reddit.memes_used:
                    break
            Reddit.memes_used.append(rand)
            random_sub = Reddit.memes[rand]
            name = random_sub.title
            img = random_sub.url
            embed = discord.Embed(color=a, title=name)
            embed.set_image(url=img)
            embed.set_thumbnail(
                url="https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg")
            if len(Reddit.memes_used) == 500:
                Reddit.memes_used.clear()
            message = await ctx.send(embed=embed)
            await message.add_reaction("👍")
            await message.add_reaction("👎")
        else:
            await ctx.send('This command cannot be used here, go to ' + '<#777079599505997844>')

    @commands.command()
    async def joke(self, ctx):
        a = randcolor()
        while True:
            num = randrange(0, len(Reddit.jokes))
            if num not in Reddit.jokes_used:
                break
        Reddit.jokes_used.append(num)
        random_joke = Reddit.jokes[num]
        name = random_joke.title
        body = random_joke.selftext
        embed = discord.Embed(color=a, title=f"Joke for {str(ctx.author)[:-5]}")
        embed.add_field(name=f"{name}", value=f"{body}.")
        embed.set_thumbnail(
            url="https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg")
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")


class Events(commands.Cog):
    
    status = cycle(['with ^help','Bot made by','Amay Sharma'])
    client = None
    blacklist = None

    def __init__(self, client):
        self.client = client
        Events.client = client
      
    @tasks.loop(seconds=5)
    async def change_status():
      await Events.client.change_presence(activity = discord.Game(next(Events.status)))


    @commands.Cog.listener()
    async def on_ready(self):
        print('Almost Ready to go!')
        top = Reddit.subr_meme.top(limit=500)
        for sub in top:
            Reddit.memes.append(sub)
        top = Reddit.subr_joke.top(limit=500)
        for sub in top:
            Reddit.jokes.append(sub)
        Events.change_status.start()
        with open('cogs/words.txt','r') as f:
          Events.blacklist = f.readlines()
        print('Ready!')

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.client.user:
            return
        try:
          for role in message.author.roles:
            if role.id == 777886176903954442:
              return
          if message.channel.id ==780084568954372137 :
            return
        except AttributeError: pass
      
    
        if 'https://discord.gg/' in message.content:
            await message.delete()
            await message.channel.send(f'Please send invites in dm <@!{message.author.id}>')
            
    @commands.Cog.listener()
    async def on_raw_reaction_add(self,event):
      message = event.message_id

      with open('reactions.json','r') as f:
        data = json.load(f)
      try:
        record = data[str(message)]
      except KeyError:
        return
      guild = Events.client.get_guild(event.guild_id)
      channel = guild.get_channel(event.channel_id)
      user = guild.get_member(event.user_id)
      message = await channel.fetch_message(message)
      if user.id == Events.client.user: return
      if str(event.emoji) in record.keys():
        role = message.guild.get_role(record[event.emoji.name])
        await user.add_roles(role)
    
      else: return 
    
def setup(client):
    client.add_cog(Fun(client))
    client.add_cog(Events(client))

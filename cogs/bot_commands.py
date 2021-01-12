import discord
from discord.ext import commands
from random import choice
import asyncio
import json

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


class Normal(commands.Cog):
    def __init__(self, client):
        self.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def poll(self, ctx, *, arg):
        a = randcolor()
        embed = discord.Embed(color=a, title=f"Poll by {str(ctx.author)[:-5]}")
        embed.add_field(name="Poll for the sever", value=arg)
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        )
        message = await ctx.send(embed=embed)
        await message.add_reaction("👍")
        await message.add_reaction("👎")

    @commands.command()
    async def createembed(self, ctx, *, content):
        '''
         title | name | description | thumbnail
        '''
        lis = content.split("|")
        embed = discord.Embed(color=randcolor(), title=lis[0])
        embed.set_author(
            name=str(ctx.author)[:-5], icon_url=ctx.author.avatar_url)
        embed.add_field(name=lis[1], value=lis[2])
        try:
            thumb = lis[3]
        except IndexError:
            thumb = "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        embed.set_thumbnail(url=thumb)
        await ctx.send(embed=embed)

    @commands.command()
    async def ping(self, ctx):
        await ctx.send('Pong!')

    @commands.command()
    async def say(self, ctx, *, arg):
        await ctx.message.delete()
        await ctx.send(arg)

    @commands.command()
    async def joined(self, ctx, member: discord.Member):
        embed = discord.Embed(color=randcolor())
        embed.add_field(
            name=str(ctx.author)[:-5],
            value=f'{member.name} joined at {member.joined_at}')
        embed.set_thumbnail(url=member.avatar_url)
        await ctx.send(embed=embed)


class Giveaways(commands.Cog):
    def __init__(self, client):
        self.client = client
        Giveaways.client = client

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def gstart(self, ctx, channel: discord.guild.TextChannel, *, reward):
        a = randcolor()
        embed = discord.Embed(
            color=a, title=f"Giveaway hosted for {ctx.guild}")
        embed.set_author(
            name=str(ctx.author)[:-5], icon_url=ctx.author.avatar_url)
        embed.add_field(
            name=f"Giveaway for {reward}",
            value=
            f"Click on the 🎉 reaction to register for it. \n Hosted by <@!{ctx.author.id}>"
        )
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        )
        gm = await channel.send(embed=embed)
        try:
            await gm.add_reaction("🎉")
        except Exception:
            await gm.add_reaction("🎉")

    users = None

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def gend(self, ctx, msg: int):
        message = await ctx.fetch_message(msg)
        Giveaways.users = await message.reactions[0].users().flatten()
        Giveaways.users.pop(Giveaways.users.index(self.client.user))
        winner = choice(Giveaways.users)
        Giveaways.users.pop(Giveaways.users.index(winner))
        await ctx.send(
            f"<@!{winner.id}> has won giveaway of {len(Giveaways.users)} members!"
        )
        await ctx.send("https://discord.com/channels/" +
                       str(message.guild.id) + "/" + str(message.channel.id) +
                       "/" + str(message.id))

    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def greroll(self, ctx):
        winner = choice(Giveaways.users)
        Giveaways.users.pop(Giveaways.users.index(winner))
        await ctx.send(f"New winner is <@!{winner.id}>")

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def giveaway(ctx, guild_invite: discord.Invite = None):
      def check(m):
          return m.author == ctx.author and m.channel == ctx.channel

      questions = [
          "Please tell the channel of the giveaway",
          "For what duration should it last", "Number of winners",
          "What will be the award"
      ]
      replies = []
      for i in questions:
          await ctx.channel.send(i)

          try:
              message = await Giveaways.client.wait_for(
                  "message", timeout=180, check=check)
              replies.append(message.content)

          except asyncio.TimeoutError:
              await ctx.channel.send(
                  "You didnt respond in time.. The procedure is stopped")
              return

      
      embed = discord.Embed(
          title=replies[3],
          description=f"React with 🎉 to have a chance to win **{replies[3]}**\nHosted by {ctx.author.mention}",
          colour=discord.Colour.green())

      embed.add_field(name="Timer", value="countdown")

      embed.set_footer(text=f"Number of winners : {replies[2]}")

      channel = ""

      for i in replies[0]:
          try:
              int(i)
              channel = channel + i
          except:
              print("lol")

      replies[0] = int(channel)

      channel = Giveaways.client.get_channel(replies[0])

      giveaway_message = await channel.send(embed=embed)
      await giveaway_message.add_reaction("🎉")

      timer = replies[1].split(":")
      days = timer[0]
      hours = timer[1]
      minutes = timer[2]
      seconds = timer[3]

      a = ((int(days) * 3600 * 24) + (int(hours) * 3600) + (int(minutes) * 60) +
          (int(seconds)))

      for i in range(a, 0, -1):

          days = i // 86400
          hours = (i % 86400) // 3600
          minutes = (i % 3600) // 60
          seconds = (i % 3600) % 60

          new_embed = discord.Embed(
              title=replies[3],
              description=f"React with 🎉 to have a chance to win **{replies[3]}**\nHosted by {ctx.author.mention}",
              colour=discord.Colour.green())

          new_embed.add_field(
              name="Timer",
              value=(str(days) + ":" + str(hours) + ":" + str(minutes) + ":" +
                    str(seconds)))

          new_embed.set_footer(text=f"Number of winners : {replies[2]}")

          await giveaway_message.edit(embed=new_embed)
          await asyncio.sleep(1)

      new_embed = discord.Embed(
          title=replies[3],
          description=f"React with 🎉 to have a chance to win **{replies[3]}**\nHosted by {ctx.author.mention}",
          colour=discord.Colour.green())

      new_embed.add_field(name="Timer", value="The time is over :( ")

      new_embed.set_footer(text=f"Number of winners : {replies[2]}")

      await giveaway_message.edit(embed=new_embed)

      channel = giveaway_message.channel
      new_message = await channel.fetch_message(giveaway_message.id)

      users = await new_message.reactions[0].users().flatten()
      users.pop(users.index(Giveaways.client.user))
      for members in users:
          if guild_invite != None:
              if members not in guild_invite.guild.members:
                  users.pop(users.index(members))

      await channel.send(
          f"There were {len(users)} valid enteries\nThese people have 90% more chances to win"
      )
      winner = []
      try:
          for i in range(int(replies[2])):
              winner.append(choice(users))

      except:
          await channel.send("Not enough people reacted :(")

      for i in winner:

          await channel.send(f"""{i.mention} won the ***{replies[3]}*** 🥳🥳🎉🎉
          https://discordapp.com/channels/{channel.guild.id}/{channel.id}/{new_message.id}
  Claim yout prize from {ctx.author.mention}""")

class Moderation(commands.Cog):
    def __init__(self, client):
        self.client = client
        Moderation.client = client

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, Member: discord.Member, *, reason="Unspecified"):
        img = "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        a = randcolor()
        await Member.ban(reason=reason)
        for i in ctx.guild.text_channels:
            if str(i) == "audit-log":
                embed = discord.Embed(color=a, title="Audit Message")
                embed.add_field(
                    name="Ban",
                    value=
                    f"<@!{Member.id}> has been banned by {str(ctx.author)[:-5]}",
                    inline=False)
                embed.add_field(name="Reason", value=reason)
                embed.set_thumbnail(url=img)
                await i.send(embed=embed)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def kick(self, ctx, Member: discord.Member, *, reason="Unspecified"):
        img = "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        a = randcolor()
        for i in ctx.guild.text_channels:
            if str(i) == "audit-log":
                embed = discord.Embed(color=a, title="Audit Message")
                embed.add_field(
                    name="Kick",
                    value=
                    f"<@!{Member.id}> has been kicked by {str(ctx.author)[:-5]}",
                    inline=False)
                embed.add_field(name="Reason", value=reason)
                embed.set_thumbnail(url=img)
                await i.send(embed=embed)
        await Member.send(embed=embed)
        await Member.kick(reason=reason)

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, *, member):
        banned_users = await ctx.guild.bans()
        member_name, member_hash = member.split("#")
        for bans in banned_users:
            user = bans.user
        if (user.name, user.discriminator) == (member_name, member_hash):
            await ctx.guild.unban(user)
        a = randcolor()
        for i in ctx.guild.text_channels:
            if str(i) == "audit-log":
                embed = discord.Embed(color=a, title="Audit Message")
                embed.add_field(
                    name="Unban",
                    value=
                    f"<@!{user.id}> has been unbanned by {str(ctx.author)[:-5]}",
                    inline=False)
                embed.set_thumbnail(
                    url=
                    "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
                )
                await i.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def mute(self, ctx, member: discord.Member, reason="Unspecified"):
        a = randcolor()
        check = True
        for i in member.guild.roles:
            if str(i) == "Muted":
                await member.add_roles(i)
                check = False
        if not check:
            message = f"{str(ctx.author)[:-5]} has muted member {str(member)[:-5]}"
        else:
            message = "Muted role not found, please make one for the server"
        embed = discord.Embed(color=a, title="Audit Message")
        embed.add_field(name="Muting", value=message)
        embed.add_field(name="Reason", value=reason)
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        )
        await ctx.send(embed=embed)
        for i in ctx.guild.text_channels:
            if str(i) == "audit-log":
                await i.send(embed=embed)
        await member.send(embed=embed)

    @commands.command()
    @commands.has_permissions(manage_roles=True)
    async def unmute(self, ctx, member: discord.Member):
        a = randcolor()
        check = True
        for i in member.guild.roles:
            if str(i) == "Muted":
                await member.remove_roles(i)
                check = False
        if not check:
            message = f"{str(ctx.author)[:-5]} has unmuted member {str(member)[:-5]}"
        else:
            message = "Member already unmuted"
        embed = discord.Embed(color=a, title="Audit Message")
        embed.add_field(name="Unmuting", value=message)
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        )
        await ctx.send(embed=embed)
        for i in ctx.guild.text_channels:
            if str(i) == "audit-log":
                await i.send(embed=embed)

    @commands.command()
    @commands.has_permissions(administrator=True)
    async def nuke(self, ctx):
        a = randcolor()
        b = ctx.channel
        await ctx.channel.clone()
        await ctx.channel.delete()
        embed = discord.Embed(color=a, title="Audit Message")
        embed1 = discord.Embed(color=a, title="Audit Message")
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        )
        embed.add_field(
            name="Nuke",
            value=f"This Channel was frikin' nuked by {str(ctx.author)[:-5]}")
        embed1.add_field(
            name="Nuke", value=f"{str(ctx.author)[:-5]} nuked {b}")
        for i in ctx.guild.text_channels:
            if str(i) == str(b):
                try:
                    asyncio.sleep(3)            
                    await i.send(embed=embed)
                    await i.send(
                        "https://tenor.com/view/explosion-explode-clouds-of-smoke-gif-17216934"
                    )
                except Exception:
                    asyncio.sleep(3)
                    await i.send(embed=embed)
                    await i.send(
                        "https://tenor.com/view/explosion-explode-clouds-of-smoke-gif-17216934"
                    )
            elif str(i) == "audit-log":
                await i.send(embed=embed1)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount=5):
        a = randcolor()
        embed = discord.Embed(color=a, title="Audit Message")
        embed.set_thumbnail(
            url=
            "https://media.discordapp.net/attachments/767369859406888972/777080266858168320/images_22.jpeg"
        )
        messages = await ctx.channel.history(limit=amount).flatten()
        if len(messages) < amount:
            amount = len(messages)
        await ctx.channel.purge(limit=amount + 1)
        embed.add_field(name="Clear", value=f"Cleared {amount} messages")
        msg=await ctx.send(embed=embed)
        await asyncio.sleep(5)
        await msg.delete()
        for i in ctx.guild.text_channels:
            if str(i) == "audit-log":
                await i.send(embed=embed)

    @commands.has_permissions(manage_guild=True)
    @commands.command()
    async def ReactionRole(self,ctx):
      with open('reactions.json','r') as f:
        data  = json.load(f)
      embed = discord.Embed(
        color = randcolor(),
        title = 'Reaction Role Message'
      )
      def check(waited_msg):
        return waited_msg.author == ctx.author and waited_msg.channel == ctx.channel
      msgData = {}
      msgDataRaw = []
      follow_up = [
        "Which all roles are to be added? Please mention them and send the message.",
        "What all reactions will be there? Please send emojis in the same order separated by a comma without space.",
        "Which channel is it to be posted in? Please mention the channel."

      ]
      await ctx.send("Please respond in 1 minute each for the questions that follow.")
      try:
        for question in follow_up:
          await ctx.send(question)
          msg = await Moderation.client.wait_for(
            "message",
            check = check,
            timeout = 60.0
            )
          msgDataRaw.append(msg)
        
      except asyncio.TimeoutError:
        await ctx.send('No response recieved')
        return
      """
      id : {reaction:role,reaction:role}
      """
      roles = msgDataRaw[0].role_mentions
      reactions = msgDataRaw[1].content.split(",")
      channel = msgDataRaw[2].channel_mentions[0]
      string = ""

      for index in range(len(roles)):
        string += f"{reactions[index]} : <@&{roles[index].id}>\n"
        msgData[reactions[index]] = roles[index].id

      embed.add_field(name= "React to get appropriate roles:", value = string)

      embed.set_thumbnail(
            url=
            'https://media.discordapp.net/attachments/785131571560185889/786577721689505822/unnamed.png'
        )
      message = await channel.send(embed = embed)
      for emoji in reactions:
        await message.add_reaction(emoji)
      data[str(message.id)] = msgData   

      with open('reactions.json','w') as f:
        json.dump(data,f) 



def setup(client):
    client.add_cog(Normal(client))
    client.add_cog(Giveaways(client))
    client.add_cog(Moderation(client))

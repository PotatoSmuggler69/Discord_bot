from webserver import keep_alive
import os

import asyncio
import discord
from discord import colour
import youtube_dl
import pafy
from discord.ext import commands
import Flirt_lines as fl
import time
intents = discord.Intents.default()
intents.members = True
import features as feat
bot = commands.Bot(command_prefix=">", intents=intents)


@bot.event
async def on_ready():
    print(f"{bot.user.name} is ready.")
    
    


class Player(commands.Cog):
  
    
    def __init__(self, bot):
        self.bot = bot 
        self.song_queue = {}
        self.setup()
  
    

    def setup(self):
        for guild in self.bot.guilds:
            self.song_queue[guild.id] = []

    async def check_queue(self, ctx):
        if len(self.song_queue[ctx.guild.id]) > 0:
            ctx.voice_client.stop()
            await self.play_song(ctx, self.song_queue[ctx.guild.id][0])
            self.song_queue[ctx.guild.id].pop(0)

    async def search_song(self, amount, song, get_url=False):
        info = await self.bot.loop.run_in_executor(None, lambda: youtube_dl.YoutubeDL({"format" : "bestaudio", "quiet" : True}).extract_info(f"ytsearch{amount}:{song}", download=False, ie_key="YoutubeSearch"))
        if len(info["entries"]) == 0: return None

        return [entry["webpage_url"] for entry in info["entries"]] if get_url else info

    async def play_song(self, ctx, song):
        ffmpeg_options = {
                        'options': '-vn',
                        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5"
                         }
        url = pafy.new(song).getbestaudio().url
        ctx.voice_client.play(discord.PCMVolumeTransformer(discord.FFmpegPCMAudio(url,**ffmpeg_options)), after=lambda error: self.bot.loop.create_task(self.check_queue(ctx)))
        ctx.voice_client.source.volume = 0.5
      

    
    @commands.command()
    async def greet(self, ctx):
        await ctx.send("```Hello It's me Shruti, don't you remember me```")
    

    @commands.command()
    async def join(self, ctx):
        if ctx.author.voice is None:
            return await ctx.send("You are not connected to a voice channel, please connect to the channel you want the bot to join.")

        if ctx.voice_client is not None:
            await ctx.voice_client.disconnect()

        await ctx.author.voice.channel.connect()

    @commands.command()
    async def leave(self, ctx):
        if ctx.voice_client is not None:
            return await ctx.voice_client.disconnect()

        await ctx.send("I am not connected to a voice channel.")

    @commands.command()
    async def play(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You must include a song to play.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send("Lemme join the voice channel to play a song.")
        else:
            await ctx.voice_client.move_to(voice_channel)    
        

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I could not find the given song, try using my search command.")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}.")


            else:
                return await ctx.send("Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")
        
        song_embed = discord.Embed(
            title = "Now Playing",
            description = str(ctx.author)+" has played the song : "+song,
            colour = discord.Colour.from_rgb(69, 0, 77)
        )
        song_embed.set_author(name='Shruti',icon_url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        song_embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        song_embed.set_footer(text='My little hands at your service')
        await ctx.send(embed=song_embed)

    @commands.command()
    async def p(self, ctx, *, song=None):
        if song is None:
            return await ctx.send("You must include a song to play.")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            await voice_channel.connect()
            await ctx.send("Lemme join the voice channel to play a song.")
        else:
            await ctx.voice_client.move_to(voice_channel)    
        

        # handle song where song isn't url
        if not ("youtube.com/watch?" in song or "https://youtu.be/" in song):
            await ctx.send("Searching for song, this may take a few seconds.")

            result = await self.search_song(1, song, get_url=True)

            if result is None:
                return await ctx.send("Sorry, I could not find the given song, try using my search command.")

            song = result[0]

        if ctx.voice_client.source is not None:
            queue_len = len(self.song_queue[ctx.guild.id])

            if queue_len < 10:
                self.song_queue[ctx.guild.id].append(song)
                return await ctx.send(f"I am currently playing a song, this song has been added to the queue at position: {queue_len+1}.")

            else:
                return await ctx.send("Sorry, I can only queue up to 10 songs, please wait for the current song to finish.")

        await self.play_song(ctx, song)
        await ctx.send(f"Now playing: {song}")
        
        song_embed = discord.Embed(
            title = "Now Playing",
            description = str(ctx.author)+" has played the song : "+song,
            colour = discord.Colour.from_rgb(69, 0, 77)
        )
        song_embed.set_author(name='Shruti',icon_url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        song_embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        song_embed.set_footer(text='My little hands at your service')
        await ctx.send(embed=song_embed)    


    @commands.command()
    async def search(self, ctx, *, song=None):
        if song is None: return await ctx.send("You forgot to include a song to search for.")

        await ctx.send("Searching for song, this may take a few seconds.")

        info = await self.search_song(5, song)

        embed = discord.Embed(title=f"Results for '{song}':", description="*You can use these URL's to play an exact song if the one you want isn't the first result.*\n", colour=discord.Colour.from_rgb(69, 0, 77))
        
        amount = 0
        for entry in info["entries"]:
            embed.description += f"[{entry['title']}]({entry['webpage_url']})\n"
            amount += 1

        embed.set_footer(text=f"Displaying the first {amount} results.")
        await ctx.send(embed=embed)

    @commands.command()
    async def queue(self, ctx): # display the current guilds queue
        if len(self.song_queue[ctx.guild.id]) == 0:
            return await ctx.send("There are currently no songs in the queue.")

        embed = discord.Embed(title="Song Queue", description="", colour=discord.Colour.from_rgb(69, 0, 77))
        i = 1
        for url in self.song_queue[ctx.guild.id]:
            embed.description += f"{i}) {url}\n"

            i += 1

        embed.set_footer(text="Thanks for using me!")
        await ctx.send(embed=embed)

    @commands.command()
    async def skip(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not playing any song.")

        if ctx.author.voice is None:
            return await ctx.send("You are not connected to any voice channel.")

        if ctx.author.voice.channel.id != ctx.voice_client.channel.id:
            return await ctx.send("I am not currently playing any songs for you.")

        poll = discord.Embed(title=f"Vote to Skip Song by - {ctx.author.name}#{ctx.author.discriminator}", description="**40% of the voice channel must vote to skip for it to pass.**", colour=discord.Colour.from_rgb(69, 0, 77))
        poll.set_thumbnail(url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        poll.set_author(name='Shruti',icon_url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        poll.add_field(name="Skip", value=":white_check_mark:")
        poll.add_field(name="Stay", value=":no_entry_sign:")
        poll.set_footer(text="Voting ends in 5 seconds.")

        poll_msg = await ctx.send(embed=poll) # only returns temporary message, we need to get the cached message to get the reactions
        poll_id = poll_msg.id

        await poll_msg.add_reaction(u"\u2705") # yes
        await poll_msg.add_reaction(u"\U0001F6AB") # no
        
        await asyncio.sleep(5) # 10 seconds to vote

        poll_msg = await ctx.channel.fetch_message(poll_id)
        
        votes = {u"\u2705": 1, u"\U0001F6AB": 0}
        reacted = []

        for reaction in poll_msg.reactions:
            if reaction.emoji in [u"\u2705", u"\U0001F6AB"]:
                async for user in reaction.users():
                    if user.voice.channel.id == ctx.voice_client.channel.id and user.id not in reacted and not user.bot:
                        votes[reaction.emoji] += 1

                        reacted.append(user.id)

        skip = False

        if votes[u"\u2705"] > 0:
            if votes[u"\U0001F6AB"] == 0 or votes[u"\u2705"] / (votes[u"\u2705"] + votes[u"\U0001F6AB"]) > 0.1: # 80% or higher
                skip = True
                embed = discord.Embed(title="Skip Successful", description="***Voting to skip the current song was succesful, skipping now.***", colour=discord.Colour.from_rgb(69, 0, 77))

        if not skip:
            embed = discord.Embed(title="Skip Failed", description="*Voting to skip the current song has failed.*\n\n**Voting failed, the vote requires at least 40% of the members to skip.**", colour=discord.Colour.from_rgb(69, 0, 77))

        embed.set_footer(text="Voting has ended.")

        await poll_msg.clear_reactions()
        await poll_msg.edit(embed=embed)

        if skip:
            ctx.voice_client.stop()
            await self.check_queue(ctx)


    @commands.command()
    async def pause(self, ctx):
        if ctx.voice_client.is_paused():
            return await ctx.send("I am already paused.")

        ctx.voice_client.pause()
        await ctx.send("The current song has been paused.")
    
    @commands.command()
    async def stop(self,ctx):
        ctx.voice_client.stop()
        await ctx.send("The song has been stopped.")


    @commands.command()
    async def resume(self, ctx):
        if ctx.voice_client is None:
            return await ctx.send("I am not connected to a voice channel.")

        if not ctx.voice_client.is_paused():
            return await ctx.send("I am already playing a song.")
        
        ctx.voice_client.resume()
        await ctx.send("The current song has been resumed.")
    
    @commands.command()
    async def ping(self, ctx: commands.Context):
        await ctx.send("Ping-ing the servers and getting the pong responses")
        start_time = time.time()
        await ctx.send("Testing Ping...")
        end_time = time.time()
        content=f"{round(self.bot.latency * 1000)} ms"
        APIping = str(round((end_time - start_time) * 1000))
        await ctx.send("```fix\nServer Pong = "+content+"\U0001F910\nAPI Response = "+APIping+" ms\U0001F910```")
        
    @commands.command()
    async def flirt(self,ctx):
        hash_name=str(ctx.author)
        only_name=hash_name.partition('#')
        only_name=str(only_name[0])

        flirt_line=str(fl.flirtl())

        flirt_embed = discord.Embed(
            title=only_name+"......\U0001F449 \U0001F448",
            description='Its a bit embarassing\nBut I wanna say that.....\U0001F61A\U0001F648\U0001F48B\U0001F648\n',
            colour= discord.Colour.from_rgb(69, 0, 77)
        )
        flirt_embed.set_footer(text=only_name+",See you later Sugar Daddy",icon_url='https://discord.com/api/oauth2/authorize?client_id=888296132046913536&permissions=0&scope=bot')
        flirt_embed.set_author(name='Shruti',
        icon_url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        flirt_embed.add_field(name="That "+only_name+" umm.....",value="\n```\U0001F5A4"+flirt_line+"\U0001F5A4```\n[Invite me Onichannn !!!!!](https://discord.com/api/oauth2/authorize?client_id=888296132046913536&permissions=0&scope=bot)",inline=True)
        flirt_embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        await ctx.send(embed=flirt_embed)


    @commands.command()
    async def helpme(self,ctx):
        hash_name=str(ctx.author)
        only_name=hash_name.partition('#')
        only_name=str(only_name[0])
        help_embed =discord.Embed(
            title="Shruti is there to help",
            description = "This 'help' window,\ndisplays all the commands\n and the corresponding action\nwhich one can perform.\n\n\nCatering to the needs of my Onichann!!\nis Shruti's first priority",
            colour = discord.Colour.from_rgb(69, 0, 77)
        )
        help_embed.set_author(name="Shruti",icon_url = 'https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        help_embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        help_embed.add_field(name='>helpme',value="```diff\n-Display all the commands\n-and description ```",inline=True)
        help_embed.add_field(name='>play',value="```diff\n-Play audio via Youtube API```",inline=True)
        help_embed.add_field(name='>pause',value="```diff\n-Pauses the song playing```",inline=True)
        help_embed.add_field(name='>resume',value="```diff\n-Resumes the paused video```",inline=True)
        help_embed.add_field(name='>skip',value="```diff\n-Skips the current\n-playing song to the next in queue```",inline=True)
        help_embed.add_field(name='>flirt',value="```diff\n+Shruti flirts with the author```",inline=True)
        help_embed.add_field(name='>stop',value="```diff\n-Stops the playing song```",inline=True)
        help_embed.add_field(name='>leave',value="```diff\n-Shruti leaves the channel```",inline=True)
        help_embed.add_field(name='>ping',value="```diff\n-Return the ping of the bot```",inline=True)
        help_embed.add_field(name="Click Here\U0001F447",value="[Invite me Onichannn !!!!!](https://discord.com/api/oauth2/authorize?client_id=888296132046913536&permissions=0&scope=bot)",inline=False)
        help_embed.set_footer(text=only_name+' Senpai called me for help  '+ '|   www.shrutibot.in ')
        await ctx.send(embed=help_embed)

    @commands.command()
    async def anal(self,ctx):
        anal_embed =discord.Embed(
            title="Oppa so you want to have Anal with me ?",
            description="But it will be my first time, please don't be rough ",
            colour=discord.Colour.from_rgb(69, 0, 77)
        )
        anal_embed.set_author(name="Shruti",icon_url = 'https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        anal_embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        await ctx.send(embed=anal_embed)

    @commands.command()
    async def intro(self,ctx):
        hash_name=str(ctx.author)
        only_name=hash_name.partition('#')
        only_name=str(only_name[0])
        intro_embed=discord.Embed(
            title = 'Shruti is Back',
            description = feat.diary_woven,
            colour=discord.Colour.from_rgb(69, 0, 77)
        )
        intro_embed.set_author(name="Shruti",icon_url = 'https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        intro_embed.set_thumbnail(url='https://cdn.discordapp.com/avatars/888296132046913536/1dd400abb8099c666ddf47073182aa24.webp?size=128')
        intro_embed.set_image(url='https://www.teahub.io/photos/full/288-2884967_anime-guitar-wallpaper-1080p.jpg')
        intro_embed.add_field(name='>helpme',value="```diff\n-Display all the commands\n-and description ```",inline=True)
        intro_embed.add_field(name='>play',value="```diff\n-Play audio via Youtube API```",inline=True)
        intro_embed.add_field(name='>pause',value="```diff\n-Pauses the song playing```",inline=True)
        intro_embed.add_field(name='>resume',value="```diff\n-Resumes the paused video```",inline=True)
        intro_embed.add_field(name='>skip',value="```diff\n-Skips the current\n-playing song to the next in queue```",inline=True)
        intro_embed.add_field(name='>flirt',value="```diff\n+Shruti flirts with the author```",inline=True)
        intro_embed.add_field(name='>stop',value="```diff\n-Stops the playing song```",inline=True)
        intro_embed.add_field(name='>leave',value="```diff\n-Shruti leaves the channel```",inline=True)
        intro_embed.add_field(name='>ping',value="```diff\n-Return the ping of the bot```",inline=True)
        intro_embed.add_field(name="Click Here\U0001F447",value="[Invite me Onichannn !!!!!](https://discord.com/api/oauth2/authorize?client_id=888296132046913536&permissions=0&scope=bot)",inline=False)
        intro_embed.set_footer(text=only_name+' Senpai called me for help  '+ '|   www.shrutibot.in ')
        await ctx.send(embed=intro_embed)
async def setup():
    await bot.wait_until_ready()
    bot.add_cog(Player(bot))

bot.loop.create_task(setup())


keep_alive()

my_secret = os.environ['DISCORD_SECRET']
bot.run(my_secret)
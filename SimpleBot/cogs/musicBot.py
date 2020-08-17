import discord
import youtube_dl
import asyncio
import os
from discord.ext import commands

ytdl_format_options2 = {
    'format': 'bestaudio/best',
    'outtmpl': '%(extractor)s-%(id)s-%(title)s.%(ext)s',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'auto',
    'source_address': '0.0.0.0'
}
ytdl_format_options1 = {
        'format': 'bestaudio/best',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '192',
        }],
    }

ffmpeg_options = {
    'options': '-vn'
}

ytdl1 = youtube_dl.YoutubeDL(ytdl_format_options1)
ytdl2 = youtube_dl.YoutubeDL(ytdl_format_options2)


players = {}


class YTDLSource(discord.PCMVolumeTransformer):
    def __init__(self, source, *, data, volume=0.5):
        super().__init__(source, volume)

        self.data = data
        self.title = data.get("title")
        self.url = data.get("url")

    @classmethod
    async def from_url(cls, url, *, loop = None, stream = False):
        loop = loop or asyncio.get_event_loop()
        data = await loop.run_in_executor(
            None, lambda: ytdl2.extract_info(url, download = not stream)
        )

        if "entries" in data:
            # take first item from a playlist
            data = data["entries"][0]

        filename = data["url"] if stream else ytdl2.prepare_filename(data)
        return cls(discord.FFmpegPCMAudio(filename, **ffmpeg_options), data = data)


class MusicBot(commands.Cog):
    def __init__(self, client):
        self.client = client
        self.nextSong = asyncio.Event()
        self.songs = asyncio.Queue()
        self.audioPlayer = self.client.loop.create_task(self.audio_player_task())

    @commands.Cog.listener()
    async def on_ready(self):
        print("MusicBot is online!")

    async def audio_player_task(self):
        while True:
            self.nextSong.clear()
            self.current = await self.songs.get()
            self.current.start()
            await self.nextSong.wait()

    def toggle_next(self):
        self.client.loop.call_soon_threadsafe(self.nextSong.set)

    """
    @commands.command()
    async def play(self, ctx, url):
        song = os.path.isfile("song" + count.str() + ".mp3")

        try:
            if song:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file but it is being played")
            await ctx.send("Music is already playing")
            
        await ctx.send("Getting Music Ready")

        with ytdl1 as youtube_dl:
            print("Downloading audio now")
            youtube_dl.download([url])

        for file in os.listdir("/Users/David/Desktop/My_Projects"):
            print(file)

        for file in os.listdir("/Users/David/Desktop/My_Projects"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")
    
        player = ctx.voice_client.play(discord.FFmpegPCMAudio("song.mp3"), after = self.toggle_next)
        ctx.voice_client.source = discord.PCMVolumeTransformer(ctx.voice_client.source, volume = 0.2)

        songName = name.rsplit("-", 2)
        await ctx.send(f"Playing: {songName}")
        print("Playing")
        await self.songs.put(player)
        """
    
    #play command with import OS
    @commands.command(aliases=["p", "pla"])
    async def play1(self, ctx, url: str):

        song = os.path.isfile("song.mp3")

        try:
            if song:
                os.remove("song.mp3")
                print("Removed old song file")
        except PermissionError:
            print("Trying to delete song file but it is being played")
            await ctx.send("Music is already playing")
            return

        await ctx.send("Getting Music Ready")

        with ytdl1 as youtube_dl:
            print("Downloading audio now")
            youtube_dl.download([url])

        for file in os.listdir("/Users/David/Desktop/My_Projects"):
            print(file)

        for file in os.listdir("/Users/David/Desktop/My_Projects"):
            if file.endswith(".mp3"):
                name = file
                print(f"Renamed File: {file}\n")
                os.rename(file, "song.mp3")

        ctx.voice_client.play(
            discord.FFmpegPCMAudio("song.mp3"), after = lambda e: print("Song is done!")
        )
        ctx.voice_client.source = discord.PCMVolumeTransformer(
            ctx.voice_client.source, volume=0.2
        )

        songName = name.rsplit("-", 2)
        await ctx.send(f"Playing: {songName}")
        print("Playing")

    @commands.command()
    async def play2(self, ctx, url: str):
        print(url)

        async with ctx.typing():
            player = await YTDLSource.from_url(url, loop = self.client.loop)
            
            ctx.voice_client.play(player, after=lambda e: print("Song is done!"))

        await ctx.send("Now playing: {}".format(player.title))



    # command to check if the voice is playing any music
    @commands.command()
    async def song(self, ctx):
        async with ctx.typing():
            if ctx.voice_client.is_playing():
                await ctx.send(f"A song is currently playing")
            else:
                await ctx.send(f"No song is currently playing")

    # command to pause the voice client
    @commands.command()
    async def pause(self, ctx):
        async with ctx.typing():
            if ctx.voice_client.is_paused():
                await ctx.send("The song is already paused")
            else:
                ctx.voice_client.pause()
                await ctx.send("The song is being paused")

    # command to resume the voice client
    @commands.command()
    async def resume(self, ctx):
        async with ctx.typing():
            if ctx.voice_client.is_playing():
                await ctx.send("The song is already playing")
            else:
                ctx.voice_client.resume()
                await ctx.send("The song is being paused")

    # command to make the bot join the voice channel
    @commands.command(aliases=["j", "joi"])
    async def join(self, ctx):
        channel = ctx.message.author.voice.channel

        if ctx.voice_client is not None:
            return await ctx.voice_client.move_to(channel)
        await channel.connect()

        print(f"The bot has connected to {channel}")

        async with ctx.message.channel.typing():
            await ctx.send(f"Joined {channel}")

    # command to disconnect the bot from the voice channel
    @commands.command()
    async def leave(self, ctx):
        channel = ctx.message.author.voice.channel  
        
        async with ctx.typing():
            if ctx.voice_client and ctx.voice_client.is_connected:
                await ctx.voice_client.disconnect()
                print(f"The bot has left {channel}")
                await ctx.send(f"Bot Left {channel}")
            else:
                print(f"Bot tried to leave voice channel, but was not in one")
                await ctx.send("I'm not in a channel!")

def setup(client):
    client.add_cog(musicBot(client))

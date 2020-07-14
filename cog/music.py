import discord
import asyncio
from discord.ext import commands
from YTDLSource import YTDLSource
from discord.ext import commands
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials

class Music(commands.Cog):
    def __init__(self,client):
        self.client = client
        self.playlist = None
        self.players = []
        self.next = asyncio.Event()
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status = discord.Status.idle, activity = discord.Game("Music Time!"))
        print('Music time.')
    @commands.command()
    async def kick(self,ctx,member: discord.Member,*, reason=None):
        await member.kick(reason= reason)
        await ctx.send("dang dude u kicked him.")
    @commands.command(pass_context = True, aliases = ['Hi','j', 'come'])
    async def join(self,ctx):
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("you are not in a voice channel")
            return
        await channel.connect()
    @commands.command(pass_context = True)
    async def create_playlist_from_spotify(self,ctx, url):
        spotify_uri = url
        x = spotifyy()
        x.from_uri(spotify_uri)
        if(self.playlist == None):
            await ctx.send('You created a playlist using spotify uri')
            self.playlist = x.playlist
        else:
            for i in x.playlist:
                self.playlist.append(i)
            await ctx.send('spotify playlist has now appended to your current playlist')  
    @commands.command(pass_context = True, aliases = ['bye','terminated'])
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()    
    @commands.command(pass_context = True, aliases = ['start'])
    async def play(self,ctx,url):
        print(url)
        just_url = url
        if(not await ctx.author.voice.channel.connect() ):
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()
        x = YTDLSource.from_url(just_url,loop = self.client.loop)
        while(True):
            async with ctx.typing():
           # player = await YTDLSource.from_url(url,loop = self.client.loop)
                player = await x
                self.players.append(player)
                ctx.voice_client.play(self.players.pop(), after= lambda _: ctx.bot.loop.call_soon_threadsafe(ctx.voice_client.play(self.players.pop())))
            await ctx.send('Now playing: {}'.format(player.title))
            await asyncio.sleep(30)
            if(len(self.players) == 0 ):
                break
    @commands.command(pass_context = True, aliases = ['add_to_queue'])
    async def add(self,ctx,url):
        print(url)
        just_url = url
        #x = YTDLSource.from_url(just_url,loop = self.client.loop)
        if(self.playlist == None):
            self.playlist = []
        self.playlist.append(url)
        x = YTDLSource.from_url(just_url,loop = self.client.loop)
        player = await x
        self.players.append(player)
        await ctx.send('the song added to the queue')
    @commands.command(pass_context = True, aliases = ['stop'])
    async def pause(self,ctx):
        async with ctx.typing():
            ctx.voice_client.pause()
            x = ctx.VoiceClient.name()
            await ctx.send('Y chu pause the music!'+ ' '+ x)
    @commands.command(pass_context = True)
    async def skip(self,ctx):
        if(len(self.playlist) == 0):
            await ctx.send('Niggah the queue is empty add music wtf?')
        async with ctx.typing():
            ctx.voice_client.pause()
            just_url = self.playlist.pop(0)
            x = YTDLSource.from_url(just_url,loop = self.client.loop)
            player = await x    
            ##ctx.voice_client.play(player, after = lambda e:print('Player error: %s' % e) if e else None)
            ctx.voice_client.play(self.players.pop(), after= lambda _: ctx.bot.loop.call_soon_threadsafe(ctx.voice_client.play(self.players.pop())))
        await ctx.send('Now playing: {}'.format(player.title))
    @commands.command(pass_context = True)
    async def play_next(self,ctx,url):
        old_playlist  = self.playlist
        new_playlist = []
        new_playlist.append(url)
        self.playlist = new_playlist.extend(old_playlist)
    @commands.command(pass_contex = True)
    async def delete_playlist(self,ctx):
        self.playlist = []
        await ctx.send('Bruh. Playlist deleted')
    @commands.command(pass_context = True, aliases = ['continue'])
    async def resume(self,ctx):
        async with ctx.typing():
            ctx.voice_client.resume()
            await ctx.send('being resume: ')
    @commands.command()
    async def ping(self,ctx):
        await ctx.send('stop')
    @commands.command()
    async def clear(self,ctx,amount = 5):
        await ctx.channel.purge(limit = amount +1)
    @commands.command(pass_context = True)
    async def my_playlist(self,ctx):
        embed = discord.Embed(
            title = 'My Music',
            description = 'current playlist',
            colour = discord.Colour.blue()
        )
        embed.set_footer(text = '-------------')
        embed.set_author(name = '-------------')
        if(len(self.playlist) < 10 ):
            for i in range(len(self.playlist)):
                embed.add_field(name = i+1, value = self.playlist[i], inline = True )
            await ctx.send(embed = embed)
        else:
            for i in range(10):
            ##embed.add_field(name = 'Field name', value = 'Field value', inline = False)
                embed.add_field(name = i+1, value = self.playlist[i], inline = True )
            await ctx.send(embed = embed)
            
        
def setup(client):
    client.add_cog(Music(client))

class spotifyy:
    def __init__(self, playlist= None):
        self.credential = SpotifyClientCredentials(client_id ='eec3539e31434c418de51f7c0fbc7d93' , client_secret = '4496307e3ee946f78a408a4165292086')
        self.playlist = playlist
    def create_playlist(self):
        self.playlist = []
    def from_uri(self,uri):
        if(self.playlist == None):
            create_a_playlist = self.create_playlist()
        spotify = spotipy.Spotify(client_credentials_manager = self.credential)
        s = 0
        l = 100
        i = ""
        while True:
            results = spotify.playlist_tracks(uri,offset = s,limit = l)['items']
            if(len(results) != 0):
                for j in results:
                    i =j['track']['name']
                    self.playlist.append(j['track']['name'])
            else:
                break
            s = s+l

    
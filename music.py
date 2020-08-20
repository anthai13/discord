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
        self.dic = {}
        for guild in self.client.guilds:
            print(guild.id)
            print(guild)
            self.dic[guild.id] = {}
            self.dic[guild.id]["music_queue"] = []
        print('dict for each server created')
        
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
    @commands.command(pass_context = True, aliases = ['spotify_playlist','spot'])
    async def create_playlist_from_spotify(self,ctx, url):
        spotify_uri = url
        x = spotifyy()
        x.from_uri(spotify_uri)
        ##self.playlist = x.playlist
        server_id = ctx.voice_client.guild.id
        listing =  []
        l = len(x.playlist)
        if(l > 10):
             l = 10
        for i in range(l):
            ##self.playlist.append(x.playlist[i])
            y = YTDLSource.from_url(x.playlist[i],loop = self.client.loop)
            player = await y
            listing.append(player)
            ##self.players.append(player)
            ##print(x.playlist[i]+ " :added to players")
            await ctx.send(player.title + ' :added to the queue')
        self.dic[server_id]["music_queue"].extend(listing)
    @commands.command(pass_context = True, aliases = ['bye','terminated'])
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()
        
    def playqueue(self,ctx):
            ##x = self.players.pop(0)
            ##ctx.voice_client.play(x, after = lambda _: self.playqueue(ctx))
            ##ctx.send('Now playing: {}'.format(x.title))
            
            server_id = ctx.voice_client.guild.id
            y = self.dic[server_id]["music_queue"].pop(0)
            ctx.send('Now playing: {}'.format(y.title))
            ctx.voice_client.play(y, after = lambda _: self.playqueue(ctx)) 
    @commands.command(pass_context = True, aliases = ['start'])
    async def play(self,ctx,url):
        print(url)
        
        just_url = url
        if(not await ctx.author.voice.channel.connect() ):
            voice_channel = ctx.author.voice.channel
            voice_client = await voice_channel.connect()
        x = YTDLSource.from_url(just_url,loop = self.client.loop)
        server_id = ctx.voice_client.guild.id
        while(True):
            async with ctx.typing():
                player = await x
                temp = []
                temp.append(player)
                self.dic[server_id]["music_queue"].extend(temp)
                ##self.players.append(player)
                ##ctx.voice_client.play(self.players.pop(0), after= lambda _: ctx.bot.loop.call_soon_threadsafe((self.playqueue(ctx))))
                ctx.voice_client.play(self.dic[server_id]["music_queue"].pop(0), after= lambda _: ctx.bot.loop.call_soon_threadsafe((self.playqueue(ctx))))
            await ctx.send('Now playing: {}'.format(player.title))

            if(len(self.players) == 0 ):
                break
    @commands.command(pass_context = True, aliases = ['add_to_queue'])
    async def add(self,ctx,url):
        server_id = ctx.voice_client.guild.id
        ##if(self.playlist == None):
          ##  self.playlist = []
        ##self.playlist.append(url)
        x = YTDLSource.from_url(url,loop = self.client.loop)
        player = await x
        ##self.players.append(player)
        self.dic[server_id]["music_queue"].append(player)
        await ctx.send('{} added to the queue'.format(player.title))
    @commands.command(pass_context = True, aliases = ['stop'])
    async def pause(self,ctx):
        async with ctx.typing():
            ctx.voice_client.pause()
            x = ctx.VoiceClient.name()
            await ctx.send('Y chu pause the music!'+ ' '+ x)
    @commands.command(pass_context = True)
    async def skip(self,ctx):
        server_id = ctx.voice_client.guild.id
        if(len(self.dic[server_id]["music_queue"]) == 0):
            await ctx.send('Niggah the queue is empty add music wtf?')
        async with ctx.typing():
            ctx.voice_client.pause()
            x = self.dic[server_id]["music_queue"].pop(0)
            
            ##ctx.voice_client.play(player, after = lambda e:print('Player error: %s' % e) if e else None)
            ctx.voice_client.play(x, after= lambda _: ctx.bot.loop.call_soon_threadsafe((self.playqueue(ctx))))
        await ctx.send('Now playing: {}'.format(x.title))
    @commands.command(pass_context = True, aliases = ['add_next','add_n'])
    async def play_next(self,ctx,url):
        server_id = ctx.voice_client.guild.id
        old_playlist  = self.dic[server_id]["music_queue"]
        new_playlist = []
        x = YTDLSource.from_url(url,loop = self.client.loop)
        player = await x
        new_playlist.append(player)
        new_playlist.extend(old_playlist)
        self.dic[server_id]["music_queue"] = new_playlist
        await ctx.send('{} added to the queue'.format(player.title))
    @commands.command(pass_contex = True)
    async def delete_playlist(self,ctx):
        server_id = ctx.voice_client.guild.id
        self.dic[server_id]["music_queue"] = []
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
        server_id = ctx.voice_client.guild.id
        embed = discord.Embed(
            title = 'Upcoming_queue',
            description = 'current playlist',
            colour = discord.Colour.blue()
        )
        embed.set_footer(text = '-------------')
        embed.set_author(name = '-------------')
        if(len(self.dic[server_id]["music_queue"]) < 10 ):
            for i in range(len(self.dic[server_id]["music_queue"])):
                embed.add_field(name = i+1, value = self.dic[server_id]["music_queue"][i].title, inline = True )
            await ctx.send(embed = embed)
        else:
            for i in range(10):
            ##embed.add_field(name = 'Field name', value = 'Field value', inline = False)
                embed.add_field(name = i+1, value = self.dic[server_id]["music_queue"][i].title, inline = True )
            await ctx.send(embed = embed)
    @commands.command(pass_context = True, aliases = ['checkingg'])
    async def checking(self, ctx):
        for guild in self.client.guilds:
            for member in guild.members:
                print (member)
        
        for guild in self.client.guilds:
            print(guild.id)
            print(guild.name)
        print(ctx.voice_client.guild.id, 'its in my current server')
        
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

    
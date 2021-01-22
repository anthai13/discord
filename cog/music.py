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
		## check for all the guild in guilds and for each guild create a another dic. key is the guild.id and value is an empty dictionary. Inside the empty dictionary create a key of music_queue and value as an empty list
		## data structure will now look like this {'guild_id':{'music_queue':[],{'music_played'}:[]},....}
        for guild in self.client.guilds:
            print(guild.id)
            print(guild)
            self.dic[guild.id] = {}
            self.dic[guild.id]["music_queue"] = []
			self.dic[guild.id]["music_played"] = []
        print('dic for each server created')
        
    @commands.Cog.listener()
    async def on_ready(self):
        await self.client.change_presence(status = discord.Status.idle, activity = discord.Game("Music Time!"))
        print('Music time.')
	##kick a member from a discord channel --> "need fix"--> must add priorities
    @commands.command()
    async def kick(self,ctx,member: discord.Member,*, reason=None):
        await member.kick(reason= reason)
        await ctx.send("dang dude u kicked him.")
	## add bot to the call from whoever in that channel. if the person is not in the channel return the reason
    @commands.command(pass_context = True, aliases = ['Hi','j', 'come'])
    async def join(self,ctx):
        channel = ctx.author.voice.channel
        if not channel:
            await ctx.send("you are not in a voice channel")
            return
		else:
			await channel.connect()
	## bot disconnect to the channel
	@commands.command(pass_context = True, aliases = ['bye','terminated'])
    async def leave(self,ctx):
        await ctx.voice_client.disconnect()
        
	## add spotify playlist into the queue using spotify URI
	## limit to only the first 10 songs in the playlist.
	## 10 or less songs will be added to the music_queue in a specific server
    @commands.command(pass_context = True, aliases = ['spotify_playlist','spot'])
    async def create_playlist_from_spotify(self,ctx, uri):
        spotify_uri = uri
        x = spotifyy()
        x.from_uri(spotify_uri)
        server_id = ctx.voice_client.guild.id
        listing =  []
        l = len(x.playlist)
        if(l > 10):
             l = 10
        for i in range(l):
            y = YTDLSource.from_url(x.playlist[i],loop = self.client.loop)
            player = await y
            listing.append(player)
            await ctx.send(player.title + ' :added to the queue')
        self.dic[server_id]["music_queue"].extend(listing)
##playing music based on the queue. 
## when music is done pop another.
##DISCLAMER this is not a async command
    def playqueue(self,ctx):
            server_id = ctx.voice_client.guild.id
            will_play = self.dic[server_id]["music_queue"].pop(0)
            ctx.send('Now playing: {}'.format(will_play.title))
            ctx.voice_client.play(will_play, after = lambda _: self.playqueue(ctx))
			self.dic[server_id]["music_played"].append(will_play.title)
##let the bot join the channel
##add the music to the last index of the queue.
##call playqueue function until music_queue length is 0
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
				will_play = self.dic[server_id]["music_queue"].pop(0)
                ctx.voice_client.play(will_play, after= lambda _: ctx.bot.loop.call_soon_threadsafe((self.playqueue(ctx))))
				self.dic[server_id]["music_played"].append(will_play.title)
            await ctx.send('Now playing: {}'.format(will_play.title))
            if(len(self.players) == 0 ):
                break
	## add music to the queue
    @commands.command(pass_context = True, aliases = ['add_to_queue'])
    async def add(self,ctx,url):
        server_id = ctx.voice_client.guild.id
        x = YTDLSource.from_url(url,loop = self.client.loop)
        player = await x
        self.dic[server_id]["music_queue"].append(player)
        await ctx.send('{} added to the queue'.format(player.title))
	## pause the music
    @commands.command(pass_context = True, aliases = ['stop'])
    async def pause(self,ctx):
        async with ctx.typing():
            ctx.voice_client.pause()
            x = ctx.VoiceClient.name()
            await ctx.send('Y chu pause the music!'+ ' '+ x)
	##pause music
	##pop music and then uses playqueue function
    @commands.command(pass_context = True)
    async def skip(self,ctx):
        server_id = ctx.voice_client.guild.id
        if(len(self.dic[server_id]["music_queue"]) == 0):
            await ctx.send('the queue is empty add music?')
        async with ctx.typing():
            ctx.voice_client.pause()
            x = self.dic[server_id]["music_queue"].pop(0)
            ctx.voice_client.play(x, after= lambda _: ctx.bot.loop.call_soon_threadsafe((self.playqueue(ctx))))
        await ctx.send('Now playing: {}'.format(x.title))
	#add a music and play next after the current music is complete
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
	#empty the music_queue
    @commands.command(pass_contex = True)
    async def delete_playlist(self,ctx):
        server_id = ctx.voice_client.guild.id
        self.dic[server_id]["music_queue"] = []
        await ctx.send('Bruh. Playlist deleted')
	#resume the current music
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
	## provide and Embed with the playlist.
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
		
	@commands.command(pass_context = True)
	async def recommendation(self, ctx , x):
		server_id = ctx.voice_client.guild.id
		if(x == 'played_the_most'):
			sorted =sorting(self.dic[server_id]['music_played'])
		elif(x == '')
	##create a set. Double for loops to count the number of times a music is played. add the object with (name and count). then sorted from low to high based on count with lambda expression
	def sorting(unsorted_list):
		set_of_unsorted_list = list(set(unsorted_list))
		count = []
		for i in set_of_unsorted_list:
			c = 0
			for j in unsorted_list:
			 if i == j:
				c++
			count.append(music_count(i,c))
		return sorted(count, key=lambda musicCount: musicCount.count)
class music_count:
	def __init__(self,name,count):
		self.name = name
		self.count = count
	def __repr__(self):
		return repr((self.name, self.count))
        
def setup(client):
    client.add_cog(Music(client))

class spotifyy:
    def __init__(self, playlist= None):
	clientID = ''
	clientSecret = ''
        self.credential = SpotifyClientCredentials(client_id =clientID , client_secret = clientSecret)
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

    
